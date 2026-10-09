#gera uma solução, testa se é uma solução única, e coloca os valores das arvores


ORTOGONAIS = ((-1,0), (1,0),(0,-1),(0,1))



def validador_solucao(grid):
    for linha in range(len(grid)):
        for elemento in range(len(grid[linha])-1):
            if grid[linha][elemento] != "" and grid[linha][elemento+1] != "": #verifica as linhas para ver se as tentas não se tocam
                return False



def contar_solucoes(linhas,colunas,dica_l,dica_c,arvores,limite=2):

    #caso os numero de "dicas" de colunas e linhas forem diferentes do numero de aravores, isso não caracteristica do jogo, logo é invalido
    if not (sum(dica_l)==sum(dica_c)==sum(arvores)):
        return 0,None

    #a linha candidata é uma linha onde tem pelo menos uma arvore ortonal
    linha_candidata = [[coluna for coluna in range(colunas)
                       if (linha,coluna) not in arvores and any((linha+dlinha,coluna+dcoluna) in arvores for dlinha,dcoluna in ORTOGONAIS)]
                       for linha in range(linhas)]
    set_linha_candidata = [set(x) for x in linha_candidata] 

            
