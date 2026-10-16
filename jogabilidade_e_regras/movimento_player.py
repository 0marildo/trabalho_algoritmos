import msvcrt

import jogabilidade_e_regras.regras_jogo as regras_jogo
from file_handler.salva_carregar_jogo import salvar_automatico


def movimento_cursor(posicao_atual, tamanho_grid, tecla):
    linha, coluna = posicao_atual

    if tecla == "H":
        linha -= 1
    elif tecla == "P":
        linha += 1
    elif tecla == "K":
        coluna -= 1
    elif tecla == "M":
        coluna += 1

    if 0 <= linha < tamanho_grid and 0 <= coluna < tamanho_grid:
        return linha, coluna
    return posicao_atual


def cursor(dados, nome_arquivo_autosave):
    while True:
        tecla = msvcrt.getwch()

        if tecla in ("\x00", "\xe0"):
            tecla = msvcrt.getwch()
            dados["posicao_cursor"] = movimento_cursor(
                dados["posicao_cursor"], dados["tamanho_puzzle"], tecla
            )
        elif tecla in ("q", "Q"):
            return dados
        elif tecla == "\r":
            posicao = dados["posicao_cursor"]
            if posicao in dados["tendas"]:
                dados["tendas"].remove(posicao)
                dados["jogadas"] += 1
                salvar_automatico(dados, nome_arquivo_autosave)
                if regras_jogo.win(
                    dados["puzzle"], dados["tendas"], dados["tamanho_puzzle"]
                ):
                    return dados
            elif regras_jogo.tenda_valida(
                posicao,
                dados["puzzle"],
                dados["tendas"],
                dados["tamanho_puzzle"]
            ):
                dados["tendas"].append(posicao)
                dados["jogadas"] += 1
                salvar_automatico(dados, nome_arquivo_autosave)
                if regras_jogo.win(
                    dados["puzzle"], dados["tendas"], dados["tamanho_puzzle"]
                ):
                    return dados
            else:
                print("Não é possível colocar uma tenda nessa posição.")
