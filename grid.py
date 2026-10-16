#criação de um grid, a parte mais importante e fundamento de tudo
def get_posicoes_arvores(nome_arquivo_db):
    arquivo_db = open(nome_arquivo_db)
    posicoes_raw = []
    posicoes = []
    elementos_tratado = ""
    for i in arquivo_db:
        if str(arquivo_db).strip() !=  "\n":
            posicoes_raw.append(i.strip())

    for j in posicoes_raw:
        if "," in j:
            elementos_tratado = tuple(int(x) for x in j.split(",") if x.strip().isdigit())
            posicoes.append(elementos_tratado)
        elif j == '':
            elementos_tratado = ''
            posicoes.append(j)
        else:
            elementos_tratado = tuple(int(x) for x in j.split(",") if x.strip().isdigit())
            posicoes.append(elementos_tratado)

    return posicoes

import random

def seletor_puzzle(posicoes_arvores: list):
    num_puzzles = 1
    puzzle_atual = []
    puzzles = {}
    for i in posicoes_arvores:
        if i == '':
            if puzzle_atual:
                puzzles[num_puzzles] = puzzle_atual
                num_puzzles +=1
                puzzle_atual = []
        else:
            puzzle_atual.append(i)
    
    if puzzle_atual:
        puzzles[num_puzzles] = puzzle_atual
    else:
        num_puzzles -=1

    selecao_puzzle = random.randint(1,num_puzzles)

    return puzzles[selecao_puzzle]            

from movimento_player import cursor

def draw_grid(posicoes_arvores: list,linhas: int,posicoes_tendas):
    if posicoes_tendas is None:
        posicoes_tendas=[]
    linhas_puzzle = []
    for i, colunas_ocupadas in enumerate(posicoes_arvores):
        linha_atual = []

        for c in range(1, linhas + 1):
            if (i, c - 1) in posicoes_tendas:
                linha_atual.append('T')
            elif c in colunas_ocupadas:
                linha_atual.append('A')
            else:
                linha_atual.append('-')

        linhas_puzzle.extend(linha_atual)
        print("".join(linha_atual))

    return linhas_puzzle


tamanho_puzzle = 6

if __name__=="__main__":
    posicoes_arvores = get_posicoes_arvores('db_arvores.txt')
    puzzle_selecionado = seletor_puzzle(posicoes_arvores)
    draw_grid(puzzle_selecionado,6,[(1,2)])


