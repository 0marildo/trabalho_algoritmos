from jogabilidade_e_regras.grid import puzzle_selecionado,tamanho_puzzle
from jogabilidade_e_regras.movimento_player import cursor





def salvar_jogo(puzzle_selecionado, tendas, nome_arquivo="game save"):
    arquivo = open(nome_arquivo, "w")

    arquivo.write("PUZZLE\n")

    for linha in puzzle_selecionado:
        if not linha:
            arquivo.write("-\n")
        else:
            arquivo.write(",".join(map(str, linha)) + "\n")

    arquivo.write("TENDAS\n")

    for linha, coluna in tendas:
        arquivo.write(f"{linha},{coluna}\n")

    dicionario_pertinente = {'puzzle':puzzle_selecionado, 'posicao tendas': tendas}
    arquivo.close()
    return dicionario_pertinente

def salvar_automatico(puzzle_selecionado, tendas):
    salvar_jogo(puzzle_selecionado, tendas, "autosave.txt")


def carregar_jogo(nome_arquivo):
    arquivo = open(nome_arquivo, "r")

    puzzle = []
    tendas = []
    secao_atual = None

    for linha in arquivo:
        linha = linha.strip()

        if linha == "PUZZLE":
            secao_atual = "puzzle"
            continue

        elif linha == "TENDAS":
            secao_atual = "tendas"
            continue

        if secao_atual == "puzzle":
            if linha == "-":
                puzzle.append(())
            else:
                puzzle.append(
                    tuple(int(x) for x in linha.split(","))
                )

        elif secao_atual == "tendas":
            linha, coluna = map(int, linha.split(","))
            tendas.append((linha, coluna))

    arquivo.close()

    return puzzle, tendas
