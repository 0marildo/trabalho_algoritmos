import file_handler.salva_carregar_jogo as salva_carregar_jogo
import jogabilidade_e_regras.grid as grid
import jogabilidade_e_regras.movimento_player as movimento_player
import os
import jogabilidade_e_regras.regras_jogo as regras_jogo

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    carregar_save = input('Gostaria de carregar um save? Caso sim coloque o nome do jogo salvado como "game save". Escreva "S" para sim ou "N" para um novo jogo: \n  ').strip()

    if carregar_save == 'S':
        arvores, tendas = salva_carregar_jogo.carregar_jogo('game save')

        puzzle_selecionado = arvores

    else:
        posicoes_arvores = grid.get_posicoes_arvores('db_arvores.txt')
        puzzle_selecionado = grid.seletor_puzzle(posicoes_arvores)
        tendas = []

    tamanho_puzzle = 6

    os.system('cls' if os.name == 'nt' else 'clear')
    grid.draw_grid(puzzle_selecionado, tamanho_puzzle, tendas)

    tendas = movimento_player.cursor(tamanho_puzzle)

    os.system('cls' if os.name == 'nt' else 'clear')


    if regras_jogo.win(puzzle_selecionado, tendas, tamanho_puzzle):
        print("Parabéns! Você ganhou o jogo!")

    grid.draw_grid(puzzle_selecionado, tamanho_puzzle, tendas)


    guardar = input('Gostaria de guardar o jogo? (S/N): ').strip().upper()
    tendas = movimento_player.cursor(tamanho_puzzle,puzzle_selecionado,tendas)
    if guardar == 'S':
        salva_carregar_jogo.salvar_jogo(puzzle_selecionado, tendas)
        print('Jogo guardado!')


if __name__ == '__main__':
    main()