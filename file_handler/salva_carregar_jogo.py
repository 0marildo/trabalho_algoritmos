from jogabilidade_e_regras.grid import puzzle_selecionado,tamanho_puzzle


def salvar_jogo(tendas,puzzle_selecionado= puzzle_selecionado, nome_arquivo="game_save.txt", posicao_cursor = (0,0), jogadas =0):
    
    dados = {"puzzle": puzzle_selecionado,"tendas": tendas,"tamanho_puzzle": tamanho_puzzle,"jogadas": jogadas,"posicao_cursor": posicao_cursor}
    
    arquivo = open(nome_arquivo, "w")
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


def salvar_automatico(puzzle_selecionado,tendas,tamanho_puzzle,nome_arquivo_autosave,jogadas=0,posicao_cursor=(0, 0)):
    dados = salvar_jogo(puzzle_selecionado,tendas,tamanho_puzzle,jogadas,posicao_cursor,nome_arquivo=nome_arquivo_autosave)
    return dados

def carregar_jogo(nome_arquivo="game_save.txt"):
    arquivo = open(nome_arquivo, "r")
    linhas_arquivo = arquivo.readlines()
    arquivo.close()

    dados = {"puzzle": [],"tendas": [],"tamanho_puzzle": 0,"jogadas": 0,"posicao_cursor": (0, 0)}

    secao_atual = ""

    for linha in linhas_arquivo:
        linha = linha.strip()

        if linha in ("PUZZLE", "TENDAS", "TAMANHO", "JOGADAS", "CURSOR"):
            secao_atual = linha
            continue

        if secao_atual == "PUZZLE":
            if linha == "-":
                dados["puzzle"].append(())
            else:
                dados["puzzle"].append(tuple(int(x) for x in linha.split(",")))

        elif secao_atual == "TENDAS":
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