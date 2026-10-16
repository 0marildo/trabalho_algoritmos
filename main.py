import salva_carregar_jogo, grid, movimento_player
import os



def main(grid_jogo,posicao_tendas):
    os.system('clear')

    carregar_save = input('Gostaria de carregar um save? Se sim escreva "S" no terminal e coloque o arquivo a ser carregado como "game save"')
    if carregar_save == 'S':
        arvores, tendas=salva_carregar_jogo.carregar_jogo('game save')
        grid.draw_grid(arvores,6)
        
    else:
        posicoes_arvores = grid.get_posicoes_arvores('db_arvores.txt')
        puzzle_selecionado = grid.seletor_puzzle(posicoes_arvores)
        grid.draw_grid(puzzle_selecionado)

        
