import curses

movimentos = {curses.KEY_UP: (-1,0), curses.KEY_DOWN: (1,0), curses.KEY_LEFT: (0,-1), curses.KEY_RIGHT: (0,1)}
ENTER = (curses.KEY_ENTER,10,13)


def movimentacao(tecla,posicao_atual: tuple,lado):
    movimentacao_y,movimentacao_x=movimentos[tecla] 
    x,y = posicao_atual
    nova_x,nova_y = movimentacao_x+x,movimentacao_y+y
    if 0<=nova_x<lado and 0<=nova_y<lado:
        return (nova_x,nova_y)
    else:
        return posicao_atual