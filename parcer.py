import argparse


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Jogo das Árvores e Tendas")

    inicio = parser.add_mutually_exclusive_group()

    inicio.add_argument("--novo",action="store_true",help="Inicia uma nova partida diretamente")

    inicio.add_argument("--carregar",metavar="ARQUIVO",help="Carrega uma partida diretamente de um arquivo")

    parser.add_argument("--autosave",metavar="ARQUIVO",default="autosave.txt",help="Arquivo de salvamento automático")

    parser.add_argument("--tamanho",type=int,default=6,help="Tamanho do tabuleiro (padrão: 6)")

    return parser

