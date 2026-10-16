
FICHEIRO_SAVE = "game_save.txt"
FICHEIRO_HISTORICO = "historico.txt"


def limpar_console():
    print("\n" * 3)


def pedir_opcao(mensagem, opcoes):
    while True:
        opcao = input(mensagem).strip().upper()
        if opcao in opcoes:
            return opcao
        print(f"Opção inválida. Escolha: {', '.join(opcoes)}")


def menu_principal():
    limpar_console()
    print("========== JOGO DAS ÁRVORES E TENDAS ==========")
    print("1. Novo jogo")
    print("2. Carregar jogo")
    print("3. Configurações")
    print("4. Regras")
    print("5. Histórico")
    print("6. Sair")
    print("7. Créditos")

    return pedir_opcao("Escolha: ", ["1", "2", "3", "4", "5", "6","7"])


def menu_pause():
    print("\n========== MENU DE PAUSA ==========")
    print("1. Continuar partida")
    print("2. Salvar partida")
    print("3. Carregar partida")
    print("4. Voltar ao menu principal")
    print("5. Sair do jogo")

    opcao = pedir_opcao("Escolha: ", ["1", "2", "3", "4", "5"])

    if opcao in ("2", "3"):
        nome = input(f"Nome do arquivo [{FICHEIRO_SAVE}]: ").strip()

        if not nome:
            nome = FICHEIRO_SAVE

        return opcao, nome

    return opcao, None


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
    input("\nPrecione ENTER para voltar ao menu...")


def mostrar_config():
    limpar_console()
    print("========== CONFIGURAÇÕES ==========")
    print("Tamanho do tabuleiro: 6x6")
    print("O tamanho não pode ser alterado porque os")
    print("puzzles atuais foram preparados para tabuleiros 6x6.")
    input("\nPrima ENTER para voltar ao menu...")


def guardar_historico(resultado):
    arquivo = open(FICHEIRO_HISTORICO, "a")
    arquivo.write(resultado + "\n")
    arquivo.close()


def mostrar_historico():
    limpar_console()
    print("========== HISTÓRICO ==========")

    arquivo = open(FICHEIRO_HISTORICO, "a")
    arquivo.close()

    arquivo = open(FICHEIRO_HISTORICO, "r")
    conteudo = arquivo.read()
    arquivo.close()

    if conteudo.strip():
        print(conteudo)
    else:
        print("Ainda não existem partidas registadas.")

    input("\nPrima ENTER para voltar ao menu...")

def creditos():
    limpar_console()
    print('Criador: Omar Hamza')
    print('versão 0.0.0.0.0.0.0.0.1 sim eu vou fazer o gta eventualmente')
    print('futuramente você vai conseguir gerar puzzles proceduralmente de qualquer dimensão \n e ter challenges, como tempo limitado, tendas limitadas e etc ;)')
    input("\nPrecione ENTER para voltar ao menu...")