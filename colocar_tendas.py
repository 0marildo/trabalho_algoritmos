"""Tendas no terminal, v2: interface em regioes com curses.

Setas movem | Enter coloca/remove tenda | u desfaz | ? ajuda | q sai.
Texto sem acentos de proposito (evita problemas de locale no curses).
Convencao interna: (linha, coluna) a partir de 0. O db usa colunas a partir de 1.
"""
import curses

ORTOGONAIS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MOVE = {curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
        curses.KEY_LEFT: (0, -1), curses.KEY_RIGHT: (0, 1)}
ENTER = (curses.KEY_ENTER, 10, 13)
PUZZLE_DEMO = [(2,), (5,), (1, 3), (6,), (2,), (4,)]  # formato do seletor_puzzle
Y0, X0 = 1, 1          # canto superior esquerdo do grid
LARGURA_PAINEL = 24


# ---------- logica (sem curses, testavel isoladamente) ----------

def converter_puzzle(puzzle):
    """[(2, 5), (1,), ...] (base 1, uma tupla por linha) -> {(r, c)} base 0."""
    return {(r, c - 1) for r, cols in enumerate(puzzle) for c in cols}


def mover(r, c, tecla, linhas, colunas):
    dr, dc = MOVE[tecla]
    return min(max(r + dr, 0), linhas - 1), min(max(c + dc, 0), colunas - 1)


def alternar_tenda(tendas, arvores, r, c):
    """Coloca ou remove tenda em (r, c). Devolve False se a celula e uma arvore."""
    if (r, c) in arvores:
        return False
    tendas ^= {(r, c)}
    return True


def motivo_invalido(t, tendas, arvores):
    """None se a tenda t esta ok; senao o motivo (regras locais, sem dicas)."""
    r, c = t
    if any((r + a, c + b) in tendas
           for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)):
        return "Tenda encostando em outra tenda"
    if not any((r + dr, c + dc) in arvores for dr, dc in ORTOGONAIS):
        return "Tenda sem arvore ao lado"
    return None


def tendas_invalidas(tendas, arvores):
    return {t for t in tendas if motivo_invalido(t, tendas, arvores)}


# ---------- interface ----------

def escrever(tela, y, x, texto, atributo=0):
    """addstr que ignora escrita fora da janela (inclui o canto inferior direito)."""
    try:
        tela.addstr(y, x, texto, atributo)
    except curses.error:
        pass


def iniciar_cores():
    if not curses.has_colors():  # sem cor: o simbolo ('!' para invalida) ainda diferencia
        return {"arvore": curses.A_BOLD, "tenda": curses.A_BOLD,
                "invalida": curses.A_UNDERLINE, "titulo": curses.A_BOLD}
    curses.start_color()
    try:
        curses.use_default_colors()
        fundo = -1
    except curses.error:
        fundo = curses.COLOR_BLACK
    curses.init_pair(1, curses.COLOR_GREEN, fundo)
    curses.init_pair(2, curses.COLOR_YELLOW, fundo)
    curses.init_pair(3, curses.COLOR_RED, fundo)
    curses.init_pair(4, curses.COLOR_CYAN, fundo)
    return {"arvore": curses.color_pair(1) | curses.A_BOLD,
            "tenda": curses.color_pair(2) | curses.A_BOLD,
            "invalida": curses.color_pair(3) | curses.A_BOLD,
            "titulo": curses.color_pair(4) | curses.A_BOLD}


def tamanho_minimo(linhas, colunas):
    return Y0 + 2 * linhas + 4, X0 + 4 * colunas + 1 + 3 + LARGURA_PAINEL


def desenhar(tela, cores, linhas, colunas, arvores, tendas, invalidas, r, c, mensagem):
    tela.erase()
    altura, largura = tela.getmaxyx()
    h_min, w_min = tamanho_minimo(linhas, colunas)
    if altura < h_min or largura < w_min:
        escrever(tela, 0, 0, f"Terminal pequeno demais (minimo {w_min}x{h_min})")
        tela.refresh()
        return
    escrever(tela, 0, X0, "TENDAS", cores["titulo"])
    # grade com bordas, no estilo do seu draw_grid original
    for i in range(linhas):
        y = Y0 + 2 * i
        escrever(tela, y, X0, "+---" * colunas + "+")
        escrever(tela, y + 1, X0, "|")
        for j in range(colunas):
            x = X0 + 4 * j
            if (i, j) in arvores:
                simbolo, attr = "A", cores["arvore"]
            elif (i, j) in invalidas:
                simbolo, attr = "!", cores["invalida"]
            elif (i, j) in tendas:
                simbolo, attr = "T", cores["tenda"]
            else:
                simbolo, attr = " ", 0
            if (i, j) == (r, c):
                attr |= curses.A_REVERSE
            escrever(tela, y + 1, x + 1, f" {simbolo} ", attr)
            escrever(tela, y + 1, x + 4, "|")
    escrever(tela, Y0 + 2 * linhas, X0, "+---" * colunas + "+")
    # painel lateral
    xp = X0 + 4 * colunas + 1 + 3
    escrever(tela, Y0, xp, f"Tendas:    {len(tendas)}/{len(arvores)}")
    escrever(tela, Y0 + 1, xp, f"Invalidas: {len(invalidas)}",
             cores["invalida"] if invalidas else 0)
    escrever(tela, Y0 + 2, xp, f"Cursor:    ({r + 1},{c + 1})")
    escrever(tela, Y0 + 4, xp, "A  arvore", cores["arvore"])
    escrever(tela, Y0 + 5, xp, "T  tenda", cores["tenda"])
    escrever(tela, Y0 + 6, xp, "!  tenda invalida", cores["invalida"])
    # mensagem e barra de atalhos
    texto, chave = mensagem
    escrever(tela, Y0 + 2 * linhas + 2, X0, texto, cores[chave])
    barra = " setas: mover | Enter: tenda | u: desfazer | ?: ajuda | q: sair "
    escrever(tela, altura - 1, 0, barra.ljust(largura - 1), curses.A_REVERSE)
    tela.refresh()


def caixa_modal(tela, linhas_texto):
    """Desenha uma caixa centralizada por cima da tela e espera uma tecla."""
    altura, largura = tela.getmaxyx()
    w = max(len(t) for t in linhas_texto) + 4
    h = len(linhas_texto) + 2
    y0, x0 = max((altura - h) // 2, 0), max((largura - w) // 2, 0)
    escrever(tela, y0, x0, "+" + "-" * (w - 2) + "+")
    for i, t in enumerate(linhas_texto):
        escrever(tela, y0 + 1 + i, x0, "| " + t.ljust(w - 4) + " |")
    escrever(tela, y0 + h - 1, x0, "+" + "-" * (w - 2) + "+")
    tela.refresh()
    return tela.getch()


def confirmar(tela, pergunta):
    return caixa_modal(tela, [pergunta, "", "s = sim   qualquer outra = nao"]) in (ord("s"), ord("S"))


AJUDA = ["AJUDA", "",
         "setas   mover o cursor",
         "Enter   colocar ou remover tenda",
         "u       desfazer a ultima acao",
         "?       esta ajuda",
         "q       sair", "",
         "Regras: 1 tenda por arvore (ao lado, na",
         "vertical ou horizontal); tendas nao se",
         "tocam, nem na diagonal.", "",
         "Qualquer tecla fecha."]


def jogar(tela, linhas, colunas, arvores):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    cores = iniciar_cores()
    tendas, historico = set(), []
    r = c = 0
    mensagem = ("", "titulo")
    while True:
        invalidas = tendas_invalidas(tendas, arvores)
        desenhar(tela, cores, linhas, colunas, arvores, tendas, invalidas, r, c, mensagem)
        tecla = tela.getch()
        mensagem = ("", "titulo")
        if tecla in MOVE:
            r, c = mover(r, c, tecla, linhas, colunas)
        elif tecla in ENTER:
            if not alternar_tenda(tendas, arvores, r, c):
                mensagem = ("Arvore: nao da para colocar tenda aqui", "invalida")
            else:
                historico.append((r, c))
                motivo = motivo_invalido((r, c), tendas, arvores) if (r, c) in tendas else None
                if motivo:
                    mensagem = (motivo, "invalida")
        elif tecla in (ord("u"), ord("U")):
            if historico:
                alternar_tenda(tendas, arvores, *historico.pop())
                mensagem = ("Desfeito", "titulo")
            else:
                mensagem = ("Nada para desfazer", "titulo")
        elif tecla == ord("?"):
            caixa_modal(tela, AJUDA)
        elif tecla in (ord("q"), ord("Q")):
            if not tendas or confirmar(tela, "Sair do jogo?"):
                return tendas
        # KEY_RESIZE e outras teclas: o laco apenas redesenha.


def main():
    # Para usar o seu db, troque a linha abaixo por:
    #   puzzle = seletor_puzzle(get_posicoes_arvores("db_arvores.txt"))
    puzzle = PUZZLE_DEMO
    linhas, colunas = len(puzzle), 6
    arvores = converter_puzzle(puzzle)
    tendas = curses.wrapper(jogar, linhas, colunas, arvores)
    print(f"Tendas colocadas: {len(tendas)}/{len(arvores)}")
    print(sorted((r + 1, c + 1) for r, c in tendas))


if __name__ == "__main__":
    main()


