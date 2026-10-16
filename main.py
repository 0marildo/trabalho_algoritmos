from parcer import criar_parser
import menu
import jogabilidade_e_regras.grid as grid
import jogabilidade_e_regras.movimento_player as player
import jogabilidade_e_regras.regras_jogo as regras
import file_handler.salva_carregar_jogo as save


TAMANHO_PADRAO = 6
FICHEIRO_SAVE = "game_save"


def criar_estado(puzzle, tendas=None, tamanho=TAMANHO_PADRAO):
    return {
        "puzzle": puzzle,
        "tendas": list(tendas or []),
        "tamanho_puzzle": tamanho,
        "jogadas": 0,
        "posicao_cursor": (0, 0)
    }


def salvar_estado(dados, nome_arquivo=FICHEIRO_SAVE):
    return save.salvar_jogo(dados, nome_arquivo)


def novo_jogo():
    arvores = grid.get_posicoes_arvores("jogabilidade_e_regras/db_arvores.txt")
    puzzle = grid.seletor_puzzle(arvores)
    return criar_estado(puzzle)


def carregar_estado(nome_arquivo=FICHEIRO_SAVE):
    return save.carregar_jogo(nome_arquivo)


def iniciar_jogo(dados, arquivo_autosave="autosave"):
    while True:
        menu.limpar_console()
        print("========== JOGO DAS ÁRVORES E TENDAS ==========")
        grid.draw_grid(
            dados["puzzle"],
            dados["tamanho_puzzle"],
            dados["tendas"]
        )
        print("\nUse as setas para mover | ENTER para tenda | Q para pausa")

        dados = player.cursor(dados, arquivo_autosave)

        if regras.win(dados["puzzle"], dados["tendas"], dados["tamanho_puzzle"]):
            menu.limpar_console()
            grid.draw_grid(
                dados["puzzle"],
                dados["tamanho_puzzle"],
                dados["tendas"]
            )
            print("\nParabéns! Você ganhou o jogo!")
            print(f"Total de jogadas: {dados['jogadas']}")
            menu.guardar_historico(f"Vitória | Jogadas: {dados['jogadas']}")
            input("\nPrima ENTER para voltar ao menu...")
            return "menu", dados

        opcao, nome = menu.menu_pause()
        if opcao == "1":
            continue
        elif opcao == "2":
            dados = novo_jogo()
        elif opcao == "3":
            if nome is not None:
                dados = carregar_estado(nome)
        elif opcao == "4":
            if nome is not None:
                salvar_estado(dados, nome)
                print("Partida salva com sucesso!")
                input("Prima ENTER para continuar...")
        elif opcao == "5":
            return "menu", dados
        elif opcao == "6":
            return "sair", dados


def executar_menu(args):
    while True:
        opcao = menu.menu_principal()

        if opcao == "1":
            dados = novo_jogo()
            acao, dados = iniciar_jogo(dados, args.autosave)
            if acao == "sair":
                return
        elif opcao == "2":
            nome = menu.menu_arquivos("carregar")
            if nome is not None:
                dados = carregar_estado(nome)
                acao, dados = iniciar_jogo(dados, args.autosave)
                if acao == "sair":
                    return
        elif opcao == "3":
            menu.mostrar_config()
        elif opcao == "4":
            menu.mostrar_regras()
        elif opcao == "5":
            menu.mostrar_historico()
        elif opcao == "6":
            print("Até à próxima!")
            return
        elif opcao == "7":
            menu.creditos()


def main():
    parser = criar_parser()
    args = parser.parse_args()

    if args.tamanho <= 0:
        parser.error("--tamanho deve ser um número positivo")
    if args.tamanho != TAMANHO_PADRAO:
        parser.error(
            "Os puzzles atuais são 6x6. "
            "A base precisa ser adaptada para outros tamanhos."
        )

    if args.novo:
        dados = novo_jogo()
        iniciar_jogo(dados, args.autosave)
    elif args.carregar:
        dados = carregar_estado(args.carregar)
        iniciar_jogo(dados, args.autosave)
    else:
        executar_menu(args)


if __name__ == "__main__":
    main()
