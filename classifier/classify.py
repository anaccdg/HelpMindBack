from pickle import load
import os
import sklearn

nome_arquivo = os.getcwd() + "\classifier\modelo_treino_helpmind.pkl"

def pegar_classificacao(respostas):
    with open(nome_arquivo, 'rb') as arquivo:
        modelo_treino = load(arquivo)
        classificacao = modelo_treino.predict(respostas)

        return classificacao