#criação de um grid, a parte mais importante e fundamento de tudo






#cria a estrutura principal do grid
def cria_grid_n_m(colunas,linhas):
    grid = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(" ")
        grid.append(linha)
    return grid


#desenha cada célula do grid
def draw_grid(grid):
    linhas = len(grid)
    print("+"+"---+"*linhas)
    for i in grid:
        print("|"+"   |"*linhas)
        print("+"+"---+"*linhas)




if __name__  =="__main__":
    grid = cria_grid_n_m(2,3)
    print(grid)