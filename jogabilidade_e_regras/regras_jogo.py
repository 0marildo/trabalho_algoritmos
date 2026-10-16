def tenda_valida(posicao, arvores, tendas, tamanho_grid):
    linha, coluna = posicao
    if not (0 <= linha < tamanho_grid and 0 <= coluna < tamanho_grid):
        return False

    
    if coluna + 1 in arvores[linha]:
        return False

    
    if posicao in tendas:
        return False

    
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dl == 0 and dc == 0:
                continue

            vizinho = (linha + dl, coluna + dc)

            if vizinho in tendas:
                return False

    
    adjacentes = [(linha - 1, coluna),(linha + 1, coluna),(linha, coluna - 1),(linha, coluna + 1)]

    for l, c in adjacentes:
        if 0 <= l < tamanho_grid and 0 <= c < tamanho_grid:
            if c + 1 in arvores[l]:
                return True

    return False


def win(arvores: list, tendas: list, tamanho_grid: int = 6) -> bool:
    numero_arvores = sum(len(linha) for linha in arvores)

    if len(tendas) != numero_arvores:
        return False
    if len(set(tendas)) != len(tendas):
        return False
    for linha, coluna in tendas:
        if not (0 <= linha < tamanho_grid and
                0 <= coluna < tamanho_grid):
            return False

        if coluna + 1 in arvores[linha]:
            return False

    for i, (linha, coluna) in enumerate(tendas):
        for outra_linha, outra_coluna in tendas[i + 1:]:
            if (abs(linha - outra_linha) <= 1 and
                    abs(coluna - outra_coluna) <= 1):
                return False

    posicoes_arvores = set()

    for linha, colunas in enumerate(arvores):
        for coluna in colunas:
            posicoes_arvores.add((linha, coluna - 1))

    for linha_arvore, coluna_arvore in posicoes_arvores:
        tendas_adjacentes = [(linha_arvore - 1, coluna_arvore),(linha_arvore + 1, coluna_arvore),(linha_arvore, coluna_arvore - 1),(linha_arvore, coluna_arvore + 1)]

        if not any(tenda in tendas for tenda in tendas_adjacentes):
            return False

    # Cada tenda tem de estar adjacente a uma árvore
    for linha, coluna in tendas:
        adjacentes = [
            (linha - 1, coluna),
            (linha + 1, coluna),
            (linha, coluna - 1),
            (linha, coluna + 1)
        ]

        if not any(arvore in posicoes_arvores for arvore in adjacentes):
            return False

    return True