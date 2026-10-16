
FICHEIRO_SAVE = "game_save.txt"
FICHEIRO_HISTORICO = "historico.txt"
import file_handler.salva_carregar_jogo as arquivos_save


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
    print("2. Iniciar novo jogo")
    print("3. Carregar partida")
    print("4. Salvar partida")
    print("5. Voltar ao menu principal")
    print("6. Sair do jogo")

    opcao = pedir_opcao("Escolha: ", ["1", "2", "3", "4", "5", "6"])

    if opcao in ("3", "4"):
        nome = menu_arquivos("carregar" if opcao == "3" else "salvar")
        return opcao, nome

    return opcao, None


def menu_arquivos(acao):
    while True:
        limpar_console()
        print("========== ARQUIVOS DE JOGO ==========")
        saves = arquivos_save.listar_saves()
        if saves:
            for indice, nome in enumerate(saves, 1):
                print(f"{indice}. {nome}")
        else:
            print("Nenhum save encontrado.")

        if acao == "salvar":
            print("N. Criar save com outro nome")
        print("0. Voltar")
        escolha = input("Escolha um save ou ação: ").strip()

        if escolha == "0":
            return None

        if acao == "carregar":
            if escolha.isdigit() and 1 <= int(escolha) <= len(saves):
                return saves[int(escolha) - 1]
            print("Escolha inválida.")
            input("Prima ENTER para continuar...")
        else:
            if escolha.upper() == "N":
                nome = input("Nome do novo save, sem extensão: ").strip()
            elif escolha.isdigit() and 1 <= int(escolha) <= len(saves):
                nome = saves[int(escolha) - 1]
            else:
                print("Escolha inválida.")
                input("Prima ENTER para continuar...")
                continue

            if not nome:
                continue
            if arquivos_save.save_existe(nome):
                confirmar = input(
                    "Esse arquivo existe e será sobrescrito. Confirmar? (S/N): "
                ).strip().upper()
                if confirmar != "S":
                    continue
            return nome


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
