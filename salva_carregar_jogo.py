from grid import puzzle_selecionado,tamanho_puzzle
from movimento_player import cursor





def salvar_jogo()-> None:
    tendas = cursor(tamanho_puzzle)

    arquivo = open('jogo salvo', 'w')
    arquivo.write("PUZZLE\n")

    for linha in puzzle_selecionado:
        if not linha:
            arquivo.write("-\n")
        else:
            arquivo.write(",".join(map(str, linha)) + "\n")

    arquivo.write("TENDAS\n")

    for linha, coluna in tendas:
        arquivo.write(f"{linha},{coluna}\n")

    arquivo.close()

def carregar_jogo(nome_arquivo: str):
    arquivo_carregado = open(nome_arquivo,'r')
    puzzle =[]
    tenda = []
    secao_atual = None
    for linha in arquivo_carregado:
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
            tenda.append((linha, coluna))

    return puzzle,tenda


    
    
