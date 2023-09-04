import time

ESPACO_LIVRE = '_'
JOGADA_X = 'X̲'
JOGADA_O = 'O̲'
VELHA = 'V'
OPERACOES = {"1": (0,0), "2": (0,1), "3": (0,2), "4": (1,0), "5": (1,1), "6": (1,2), "7": (2,0), "8": (2,1), "9": (2,2)}



def iniciar():
  return [[ESPACO_LIVRE] * 3 for _ in range(3)]

def desenhar(estado):
    print(' _ _ _ ')
    for i in range(3):
        print('|', end = '')
        for j in range(3):
            print('{}|'.format(estado[i][j]), end ='')
        print()
    print()

def conteudo(estado, x,y):
    return estado[x][y]

#retorna:
#'x' se x ganhou
#'o' se o ganhou
#'V' se empatou
#' ' se não acabou
def acabou(estado):
  #checando vitorias horizontais e verticais
  for i in range(3):
    if estado[i] == [JOGADA_X] * 3:
      return JOGADA_X
    if estado[i] == [JOGADA_O] * 3:
      return JOGADA_O
    if estado[0][i] != ESPACO_LIVRE and estado[0][i] == estado[1][i] and estado[1][i] == estado[2][i]:
      return estado[0][i]

  #checando a diagonal principal
  if estado[0][0] != ESPACO_LIVRE and estado[0][0] == estado[1][1] and estado[1][1] == estado[2][2]:
    return estado[0][0]

  #checando a diagonal invertida
  if estado[0][2] != ESPACO_LIVRE and estado[0][2] == estado[1][1] and estado[1][1] == estado[2][0]:
    return estado[0][2]

  if ESPACO_LIVRE in estado[0] + estado[1] + estado[2]:
    return ESPACO_LIVRE

  return VELHA


def jogada_final(estado_final):
  if estado_final == JOGADA_X:
    return(1, (-1, -1))
  if estado_final == JOGADA_O:
    return(-1, (-1, -1))
  if estado_final == VELHA:
    return(0, (-1, -1))

#retorna uma tupla sendo o:
#1o valor: pontuação do estado
#2o valor: posição da jogada que resulta na pontuação do 1o valor
def jog_max_alpha_beta(estado, alpha, beta):
  final = acabou(estado)

  if final != ESPACO_LIVRE:
      return jogada_final(final)


  maior = -2 #
  for i in range(3):
    for j in range(3):
      if estado[i][j] == ESPACO_LIVRE:
        estado[i][j] = JOGADA_X #
        (pontuacao, (jog_x, jog_y)) = jog_min_alpha_beta(estado, alpha, beta)
        estado[i][j] = ESPACO_LIVRE
        if pontuacao > maior: #
          maior = pontuacao
          melhor_jogada = (i, j)

        if maior > beta: return(maior, melhor_jogada)
        alpha = max(maior, alpha)
  return(maior, melhor_jogada)

#retorna uma tupla sendo o:
#1o valor: pontuação do estado
#2o valor: posição da jogada que resulta na pontuação do 1o valor
def jog_max(estado):
  final = acabou(estado)

  if final != ESPACO_LIVRE:
      return jogada_final(final)

  maior = -2 #
  for i in range(3):
    for j in range(3):
      if estado[i][j] == ESPACO_LIVRE:
        estado[i][j] = JOGADA_X #
        (pontuacao, (jog_x, jog_y)) = jog_min(estado)
        if pontuacao > maior: #
          maior = pontuacao
          melhor_jogada = (i, j)
        estado[i][j] = ESPACO_LIVRE

  return(maior, melhor_jogada)


def jog_min_alpha_beta(estado, alpha, beta):
  final = acabou(estado)

  if final != ESPACO_LIVRE:
      return jogada_final(final)

  menor = 2 #
  for i in range(3):
    for j in range(3):
      if estado[i][j] == ESPACO_LIVRE:
        estado[i][j] = JOGADA_O #
        (pontuacao, (jog_x, jog_y)) = jog_max_alpha_beta(estado, alpha, beta)
        estado[i][j] = ESPACO_LIVRE
        if pontuacao < menor: #
          menor = pontuacao
          melhor_jogada = (i, j)

        if menor < alpha: return (menor, melhor_jogada)
        beta = min(beta, menor)
  return (menor, melhor_jogada)

def jog_min(estado):
  final = acabou(estado)

  if final != ESPACO_LIVRE:
      return jogada_final(final)

  menor = 2 #
  for i in range(3):
    for j in range(3):
      if estado[i][j] == ESPACO_LIVRE:
        estado[i][j] = JOGADA_O #
        (pontuacao, (jog_x, jog_y)) = jog_max(estado)
        if pontuacao < menor: #
          menor = pontuacao
          melhor_jogada = (i, j)
        estado[i][j] = ESPACO_LIVRE

  return(menor, melhor_jogada)



def receber_jogada(estado):
    while True:
        i = input('LACUNA: ');
        (x,y) = OPERACOES.get(i, (-1,-1))
        if(x == -1 and y == -1):
            print('JOGADA INVÁLIDA!')
        elif(conteudo(estado,x,y) != ESPACO_LIVRE):
            print('JOGUE NUMA LACUNA VAZIA!')
        else:
            return (x,y)



def jogar_ia_vs_ia():
    tabuleiro = iniciar()
    print('########### JOGO DA VELHA ###########')

    while acabou(tabuleiro) == ESPACO_LIVRE:
        print('ULTRON:')
        #(tabuleiro)
        (previsao, (x,y)) = jog_min(tabuleiro)
        tabuleiro[x][y] = JOGADA_O
        desenhar(tabuleiro)
        if(acabou(tabuleiro) != ESPACO_LIVRE):
            break
        print('SKYNET:')
        (previsao, (x,y)) = jog_max(tabuleiro)
        tabuleiro[x][y] = JOGADA_X
        desenhar(tabuleiro)

    resultado = acabou(tabuleiro)
    if(resultado == VELHA):
        print('DEU VELHA!!!!!!!')
    elif(resultado == JOGADA_O):
        print('ULTRON VENCEU!')
    elif(resultado == JOGADA_X):
        print('SKYNET VENCEU!')

def jogar_ia_vs_ia_alpha_beta():
    tabuleiro = iniciar()
    print('########### JOGO DA VELHA (C/ PODA ALPHA-BETA)###########')

    while acabou(tabuleiro) == ESPACO_LIVRE:
        print('HAL 9000:')
        #(tabuleiro)
        (previsao, (x,y)) = jog_min_alpha_beta(tabuleiro, -100000, 100000)
        tabuleiro[x][y] = JOGADA_O
        desenhar(tabuleiro)
        if(acabou(tabuleiro) != ESPACO_LIVRE):
            break
        print('C-3PO:')
        (previsao, (x,y)) = jog_max_alpha_beta(tabuleiro, -100000, 100000)
        tabuleiro[x][y] = JOGADA_X
        desenhar(tabuleiro)

    resultado = acabou(tabuleiro)
    if(resultado == VELHA):
        print('DEU VELHA!!!!!!!')
    elif(resultado == JOGADA_O):
        print('HAL 9000 VENCEU!')
    elif(resultado == JOGADA_X):
        print('C-3PO VENCEU!')

def jogar_ia_vs_humano():
    tabuleiro = iniciar()
    print('########### JOGO DA VELHA ###########')
    print('De 1 à 9 (esquerda para a direita e de cima para baixo), escolha a lacuna onde você deseja jogar.')

    while acabou(tabuleiro) == ESPACO_LIVRE:
        print('VOCÊ:')
        desenhar(tabuleiro)
        (x,y) = receber_jogada(tabuleiro)
        tabuleiro[x][y] = JOGADA_O
        desenhar(tabuleiro)
        if(acabou(tabuleiro) != ESPACO_LIVRE):
            break
        print('I.A:')
        (previsao, (x,y)) = jog_max(tabuleiro)
        tabuleiro[x][y] = JOGADA_X
        desenhar(tabuleiro)

    resultado = acabou(tabuleiro)
    if(resultado == VELHA):
        print('DEU VELHA!!!!!!!')
    elif(resultado == JOGADA_X):
        print('I.A VENCEU!')
    elif(resultado == JOGADA_O):
        print('VOCÊ VENCEU!')



if __name__ == '__main__':
    #jogar_ia_vs_humano()

    t0 = time.time()
    jogar_ia_vs_ia()
    delta1 = time.time()-t0

    t1 = time.time()
    jogar_ia_vs_ia_alpha_beta()
    delta2 = time.time()-t1



    print('MINIMAX FINALIZADO EM {}s'.format(delta1))
    print('MINIMAX + PODA ALPHA-BETA FINALIZADO EM {}s'.format(delta2))
    #print('hello world')