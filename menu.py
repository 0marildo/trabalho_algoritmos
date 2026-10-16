
import argparse
import jogabilidade_e_regras.grid
import jogabilidade_e_regras.movimento_player
import file_handler.salva_carregar_jogo


TAMANHO_PADRAO = 6
FICHEIRO_SAVE = "game save"
FICHEIRO_HISTORICO = "historico.txt"


def limpar_console():

    print("\n" * 3)


def pedir_opcao(mensagem, opcoes):
    while True:
        opcao = input(mensagem).strip().upper()
        if opcao in opcoes:
            return opcao

        print(f"Erro: opção inválida. Escolhe: {', '.join(opcoes)}")


def mostrar_regras():
    limpar_console()
    print("========== REGRAS DO JOGO ==========")
    print("1. Cada árvore deve ter uma tenda associada.")
    print("2. Cada tenda deve ficar junto de uma árvore,")
    print("   na horizontal ou na vertical.")
    print("3. Duas tendas não podem ficar adjacentes,")
    print("   nem na diagonal.")
    print("4. As tendas não podem ocupar casas com árvores.")
    print("5. O objetivo é cumprir todas as regras.")
    input("\nPrima ENTER para voltar ao menu...")


def mostrar_config(config):
    while True:
        limpar_console()
        print("========== CONFIGURAÇÕES ==========")
        print(f"1. Tamanho do tabuleiro: {config['tamanho']}")
        print("2. Voltar")

        opcao = pedir_opcao("Escolha: ", ["1", "2"])

        if opcao == "1":
            print("A base de dados atual foi preparada para puzzles 6x6.")
            print("O tamanho só pode ser alterado quando existirem")
            print("puzzles compatíveis com outra dimensão.")
            input("\nPrima ENTER para continuar.")

        elif opcao == "2":
            return


def guardar_historico(resultado):
    arquivo = open(FICHEIRO_HISTORICO, 'a')
    arquivo.write(resultado + "\n")
    arquivo.close()

def mostrar_historico():
    limpar_console()
    print("========== HISTÓRICO ==========")

    arquivo = open(FICHEIRO_HISTORICO)
    conteudo = arquivo.read()

    if conteudo.strip():
        print(conteudo)
    else:
        print("Ainda não existem partidas registadas.")


    input("\n Aperte ENTER para voltar ao menu...")


def menu_salvar_carregar(puzzle, tendas):
    while True:
        limpar_console()
        print("========== SALVAR / CARREGAR ==========")
        print("1. Guardar partida")
        print("2. Carregar partida")
        print("3. Voltar")

        opcao = pedir_opcao("Escolha: ", ["1", "2", "3"])

        if opcao == "1":
            file_handler.salva_carregar_jogo.salvar_jogo(puzzle, tendas)
            print("Partida guardada.")
            input("Prima ENTER para continuar.")

        elif opcao == "2":
            nome = input(
                "Nome do ficheiro de save [game save]: "
            ).strip() or FICHEIRO_SAVE

            try:
                novo_puzzle, novas_tendas = (
                    file_handler.salva_carregar_jogo.carregar_jogo(nome)
                )
                print("Partida carregada.")
                input("Prima ENTER para continuar.")
                return novo_puzzle, novas_tendas

            except (OSError, ValueError) as erro:
                print(f"Erro ao carregar a partida: {erro}")
                input("Prima ENTER para continuar.")

        else:
            return puzzle, tendas


def menu_pause(puzzle, tendas, config):
    while True:
        print("\n========== MENU DE PAUSA ==========")
        print("1. Iniciar jogo")
        print("2. Carregar partida")
        print("3. Salvar partida em arquivo")
        print("4. Voltar para o jogo")
        print("5. Voltar ao menu principal")
        print("6. Sair do jogo")

        opcao = pedir_opcao(
            "Escolha uma opção: ",
            ["1", "2", "3", "4", "5", "6"]
        )

        if opcao == "1":
            dados = jogabilidade_e_regras.grid.get_posicoes_arvores("db_arvores.txt")
            puzzle = jogabilidade_e_regras.grid.seletor_puzzle(dados)
            tendas = []

            return "iniciar", puzzle, tendas

        elif opcao == "2":
            nome = input(
                "Nome do arquivo a carregar [game save]: "
            ).strip()

            if nome == "":
                nome = "game save"

            puzzle, tendas = file_handler.salva_carregar_jogo.carregar_jogo(nome)

            print("Partida carregada com sucesso!")

            return "continuar", puzzle, tendas

        elif opcao == "3":
            nome = input(
                "Nome do arquivo para salvar [game save]: "
            ).strip()

            if nome == "":
                nome = "game save"

            file_handler.salva_carregar_jogo.salvar_jogo(puzzle, tendas)

            print("Partida salva com sucesso!")

        elif opcao == "4":
            return "continuar", puzzle, tendas

        elif opcao == "5":
            return "menu", puzzle, tendas

        elif opcao == "6":
            return "sair", puzzle, tendas


def iniciar_jogo(puzzle, tendas, config):
    while True:
        limpar_console()
        print("========== ESTADO ATUAL DO JOGO ==========")
        jogabilidade_e_regras.grid.draw_grid(puzzle, config["tamanho"], tendas)

        print("\nControlos: setas para mover, ENTER para colocar/remover")
        print("Prima Q para sair do controlo e abrir o menu de pausa.")

        tendas = jogabilidade_e_regras.movimento_player.cursor(
            config["tamanho"], puzzle, tendas
        )

        # Ao sair do controlo, o jogador pode pausar ou voltar ao menu.
        acao, puzzle, tendas = menu_pause(puzzle, tendas, config)

        if acao == "menu":
            return puzzle, tendas

        # Se escolheu continuar, o ciclo volta a mostrar o tabuleiro.


def main():
    parser = argparse.ArgumentParser( description="Jogo das Árvores e Tendas")
    parser.add_argument("--save",help="Carregar uma partida a partir de um ficheiro")
    args = parser.parse_args()

    config = {"tamanho": TAMANHO_PADRAO}
    puzzle = None
    tendas = []

    while True:
        limpar_console()
        print("========== JOGO DAS ÁRVORES E TENDAS ==========")
        print("1. Novo jogo")
        print("2. Carregar jogo")
        print("3. Configurações")
        print("4. Regras")
        print("5. Histórico")
        print("6. Sair")

        opcao = pedir_opcao("Escolha: ", ["1", "2", "3", "4", "5", "6"])

        if opcao == "1":
            dados = jogabilidade_e_regras.grid.get_posicoes_arvores("db_arvores.txt")
            puzzle = jogabilidade_e_regras.grid.seletor_puzzle(dados)
            tendas = []
            puzzle, tendas = iniciar_jogo(puzzle, tendas, config)

        elif opcao == "2":
            puzzle, tendas = menu_salvar_carregar(puzzle, tendas)

            if puzzle is not None:
                puzzle, tendas = iniciar_jogo(puzzle, tendas, config)

        elif opcao == "3":
            mostrar_config(config)

        elif opcao == "4":
            mostrar_regras()

        elif opcao == "5":
            mostrar_historico()

        elif opcao == "6":
            print("Até à próxima!")
            break


if __name__ == "__main__":
    main()
