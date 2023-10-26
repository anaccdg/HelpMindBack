from pickle import load
import os

nome_arquivo = os.getcwd() + "\\business\\classifier\\modelo_treino_helpmind.pkl"


def pegar_classificacao(respostas):
    with open(nome_arquivo, 'rb') as arquivo:
        modelo_treino = load(arquivo)
        classificacao = modelo_treino.predict(respostas)

        return classificacao