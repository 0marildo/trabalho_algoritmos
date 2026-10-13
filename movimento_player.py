import msvcrt

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

    if (0 <= nova_posicao_x < tamanho_grid
            and 0 <= nova_posicao_y < tamanho_grid):
        return (nova_posicao_x, nova_posicao_y)

    return posicao_atual

def colocar_tenda(posicao_atual):
    tecla = msvcrt.getwch()
    tenda_colocada = False

    if tecla == '\r':
        tenda_colocada = True
        return tenda_colocada
    else:
        return False

def cursor(posicao_atual):
    pass