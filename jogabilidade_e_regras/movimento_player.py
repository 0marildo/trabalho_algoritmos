import msvcrt
from file_handler.salva_carregar_jogo import salvar_automatico
def movimento_cursor(posicao_atual:tuple, tamanho_grid) -> tuple:

    tecla_especial = msvcrt.getwch()
    posicao_atual_x, posicao_atual_y = posicao_atual

    posicao_x = 0
    posicao_y = 0

    if tecla_especial in ('\x00', '\xe0'):
        tecla = msvcrt.getwch()

        if tecla == 'H':
            posicao_y = -1
        elif tecla == 'P':
            posicao_y = 1
        elif tecla == 'K':
            posicao_x = -1
        elif tecla == 'M':
            posicao_x = 1
        else:
            print("Use as setas do teclado!")
            return posicao_atual
    else:
        print("Use as setas do teclado!")
        return posicao_atual

    nova_posicao_x = posicao_atual_x + posicao_x
    nova_posicao_y = posicao_atual_y + posicao_y

    if (0 <= nova_posicao_x < tamanho_grid and 0 <= nova_posicao_y < tamanho_grid):
            return (nova_posicao_x, nova_posicao_y)

    return posicao_atual

def colocar_tenda(tecla: str) -> bool:    
    return tecla == '\r'

import jogabilidade_e_regras.regras_jogo as regras_jogo
def cursor(arvores,tamanho_grid: int, tendas_iniciais=None) -> list:
    posicao_cursor = (0, 0)
    tendas = list(tendas_iniciais or [])
    jogadas = 0
    while True:
        tecla = msvcrt.getwch()

        if tecla in ('q', 'Q'):
            break

        if tecla in ('\x00', '\xe0'):
            tecla = msvcrt.getwch()

            posicao_cursor = movimento_cursor(posicao_cursor,tamanho_grid)
            jogadas+=1
        elif colocar_tenda(tecla):
            if posicao_cursor not in tendas:
                tendas.append(posicao_cursor)
            else:
                tendas.remove(posicao_cursor)
        elif regras_jogo.tenda_valida(posicao_cursor,arvores,tendas,tamanho_grid):
            tendas.append(posicao_cursor)
            salvar_automatico(arvores,tendas,tamanho_grid,jogadas,posicao_cursor,"autosave.txt")
        else:
            print('nao pode colocar uma tenda aqui')
    return tendas,jogadas