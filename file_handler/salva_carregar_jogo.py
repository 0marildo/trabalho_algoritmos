import os


PASTA_SAVES = "saves"


def caminho_save(nome_arquivo):
    if nome_arquivo.endswith(".save"):
        nome_arquivo = nome_arquivo[:-5]
    return os.path.join(PASTA_SAVES, nome_arquivo + ".save")


def listar_saves():
    if not os.path.exists(PASTA_SAVES):
        return []

    arquivos = os.listdir(PASTA_SAVES)
    saves = []
    for arquivo in arquivos:
        if arquivo.endswith(".save"):
            saves.append(arquivo[:-5])
    return saves


def save_existe(nome_arquivo):
    return os.path.exists(caminho_save(nome_arquivo))


def salvar_jogo(dados, nome_arquivo="game_save"):
    if not os.path.exists(PASTA_SAVES):
        os.makedirs(PASTA_SAVES)

    arquivo = open(caminho_save(nome_arquivo), "w")
    arquivo.write("PUZZLE\n")
    for linha in dados["puzzle"]:
        if not linha:
            arquivo.write("-\n")
        else:
            arquivo.write(",".join(map(str, linha)) + "\n")

    arquivo.write("TENDAS\n")
    for linha, coluna in dados["tendas"]:
        arquivo.write(f"{linha},{coluna}\n")

    arquivo.write("TAMANHO\n")
    arquivo.write(str(dados["tamanho_puzzle"]) + "\n")
    arquivo.write("JOGADAS\n")
    arquivo.write(str(dados["jogadas"]) + "\n")
    arquivo.write("CURSOR\n")
    arquivo.write(f"{dados['posicao_cursor'][0]},{dados['posicao_cursor'][1]}\n")
    arquivo.close()
    return dados


def salvar_automatico(dados, nome_arquivo="autosave"):
    return salvar_jogo(dados, nome_arquivo)


def carregar_jogo(nome_arquivo="game_save"):
    arquivo = open(caminho_save(nome_arquivo), "r")
    linhas_arquivo = arquivo.readlines()
    arquivo.close()

    dados = {"puzzle": [],"tendas": [],"tamanho_puzzle": 0,"jogadas": 0,"posicao_cursor": (0, 0)}
    secao_atual = ""

    for linha in linhas_arquivo:
        linha = linha.strip()
        if linha in ("PUZZLE", "TENDAS", "TAMANHO", "JOGADAS", "CURSOR"):
            secao_atual = linha
        elif secao_atual == "PUZZLE":
            if linha == "-":
                dados["puzzle"].append(())
            else:
                dados["puzzle"].append(tuple(int(x) for x in linha.split(",")))
        elif secao_atual == "TENDAS" and linha:
            linha, coluna = map(int, linha.split(","))
            dados["tendas"].append((linha, coluna))
        elif secao_atual == "TAMANHO":
            dados["tamanho_puzzle"] = int(linha)
        elif secao_atual == "JOGADAS":
            dados["jogadas"] = int(linha)
        elif secao_atual == "CURSOR":
            linha, coluna = map(int, linha.split(","))
            dados["posicao_cursor"] = (linha, coluna)

    return dados
