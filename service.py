from flask import Flask, jsonify, request
import json
import requests
from business.chatbot.const import API_KEY
from classifier import classify

classificacao = None

class BackendManager:
    respostas_usuario = []

    def __init__(self):
        self.app = Flask(__name__)
        self.setup_endpoints()
        self.conversation_history = []
        self.classificacao = []

    def setup_endpoints(self):
        self.add_cors_headers(self.app)
        self.app.route('/api/data', methods=['POST'])(self.pegar_respostas)
        self.app.route('/api/save_questions', methods=['POST'])(self.post_data)
        self.app.route('/api/conversation_chat', methods=['POST'])(self.chatgpt)

    @staticmethod
    def add_cors_headers(app):
        @app.after_request
        def add_cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

    def usar_assistente(self):
        global classificacao
        print("Valor de classificacao:", classificacao)
        if classificacao is not None and len(classificacao) > 0:
            if classificacao[0] == 'Leve':
                return "A pessoa que você vai conversar respondeu a um questionário antes de iniciar a conversa com 16 questões, e através da IA treinada pelo randomforest com base em suas respostas classificou que ele possui depressão LEVE, converse com ele com base nisso e não passe de 150 caracteres"
            elif classificacao[0] == 'Moderado':
                return "A pessoa que você vai conversar respondeu a um questionário antes de iniciar a conversa com 16 questões, e através da IA treinada pelo randomforest com base em suas respostas classificou que ele possui depressão MODERADA, converse com ele suscintamente com base nisso e não passe de 150 caracteres"
        return "A pessoa que você vai conversar respondeu a um questionário antes de iniciar a conversa com 16 questões, e através da IA treinada pelo randomforest com base em suas respostas classificou que ele possui depressão GRAVE, converse com ele suscintamente com base nisso e não passe de 150 caracteres"


    def chatgpt(self):
        headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
        link = 'https://api.openai.com/v1/chat/completions'
        id_modelo = 'gpt-3.5-turbo'
        mensagem_usuario = ''

        request_data = request.get_json()

        if 'mensagemUsuario' in request_data:
            mensagem_usuario = request_data['mensagemUsuario']

        conversation = self.conversation_history + [
            {"role": "system", "content": self.usar_assistente()},
            {"role": "user", "content": mensagem_usuario}
        ]

        mensagem_adicional = """
                            Não responda sobre outros assuntos, diga que foi projetado apenas para lidar com assuntos relacionados à depressão.
                            Lembre-se de que as pessoas que sofrem de depressão podem ter dificuldade para ler textos longos.
                            Por favor, forneça respostas curtas e objetivas para melhor atender às suas necessidades.
                            Responda de forma amigavel, e carinhosa não seja seco.
                            Se ele demonstrar vontade de se suicidar, ou morrer, sugira ele entrar em contato com o CVV 188.
                            Se ele demonstrar gratidao, não comece uma nova conversa, apenas diga que está la para ajuda-lo.
                            Não cumprimente novamente, apenas continue a conversa, com base no contexto
                            """

        partes_mensagem_adicional = mensagem_adicional.split('\n')

        for parte in partes_mensagem_adicional:
            conversation.append({"role": "system", "content": parte})

        body = {
            "model": id_modelo,
            "messages": conversation  
        }
        body = json.dumps(body)

        requisicao = requests.post(link, headers=headers, data=body)
        resposta = requisicao.json()

        print(resposta)

        mensagem = resposta['choices'][0]['message']['content']

        self.conversation_history.append({"role": "assistant", "content": mensagem})

        return mensagem

    def pegar_respostas(self):
        content = request.get_json()

        respostas = content.get('respostas')
        if respostas is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        self.respostas_usuario = []

        for coluna in respostas:
            int_coluna = []
            for linha in coluna:
                valor = ord(linha) - ord('0')
                int_coluna.append(valor)

            self.respostas_usuario.append(int_coluna)

        print(self.respostas_usuario)

        global classificacao
        classificacao = classify.pegar_classificacao(self.respostas_usuario)

        print(self.usar_assistente())

        response_data = {'message': f'POST request successful. Received message: {respostas}'}
        return jsonify(response_data)

    def post_data(self):
        content = request.get_json()
        if content is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        message = content.get('message')
        if message is None:
            return jsonify({'error': 'Message not found in JSON'}), 400

        response_data = {'message': f'POST request successful. Received message: {message}'}
        return jsonify(response_data)

    def run(self, host='localhost', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    api = BackendManager()
    api.run()