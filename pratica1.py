import os, queue
from random import shuffle, randrange

def cria_labirinto(larg = 8, alt = 3):
  vis = [[0] * larg + [1] for _ in range(alt)] + [[1] * (larg + 1)]
  sem_muros = []

  def quebra_muros(lin, col):
    vis[lin][col] = 1
    d = [(lin + 1, col), (lin - 1, col), (lin, col + 1), (lin, col - 1)]
    shuffle(d)

    for (l, c) in d:
      if vis[l][c] != 1:
        no = (lin, col)
        vizinho = (l, c)
        sem_muros.append((no, vizinho))
        quebra_muros(l, c)

  quebra_muros(randrange(alt), randrange(larg))
  return(sem_muros)


def desenha_labirinto(lab, larg = 8, alt = 3):
  ver = [['|  '] * larg + ['|'] for i in range(alt)] + [[]]
  hor = [['+--'] * larg + ['+'] for _ in range(alt + 1)]

  for ((l1, c1), (l2, c2)) in lab:
    if l1 == l2:
      ver[l1][max(c1, c2)] = '   '
    if c1 == c2:
      hor[max(l1, l2)][c1] = '+  '

  print('  '.format(), end= '')
  for i in range(larg):#coordenadas x
    print(' {} '.format(i), end= '')
  print()

  r = range(larg + 1)
  i = 0
  for (a, b) in zip(hor, ver):
    print(''.join(['  '] + a + ['\n'] + ['{} '.format(r[i] if i < larg else '')] + b))
    i += 1


def heuristica(no, objetivo):
    (xi, yi) = no["coordenadas"]
    (xf, yf) = objetivo
    return abs(xi - xf) + abs(yi - yf)

def folhas(lab, no):
    nos_folhas = []
    for (de,para) in filter(lambda caminho: no["coordenadas"] in caminho, lab):
        coordenada_folha = para if no["coordenadas"] == de else de
        custo_pai = no["custo"]
        nos_folhas.append(criar_no(coordenada_folha, pai = no, custo = custo_pai + 1))

    return nos_folhas

def a_estrela(lab, inicio, objetivo):
    fronteira = queue.PriorityQueue()
    #coloco o nó inicial
    no_inicio = criar_no(inicio)
    fronteira.put((0, id(no_inicio), no_inicio))
    visitados = []
    visitados.append(no_inicio)
    custo_ate_aqui = 0
    while not fronteira.empty():
        #pego o proximo elemento
        (_, _, no) = fronteira.get()

        #verifico se alcancei o objetivo
        if no["coordenadas"] == objetivo:
            #visitados.append(no)
            break

        for folha in folhas(lab, no):

            novo_custo = folha["custo"] #podemos melhorar esse custo
            if(folha["coordenadas"] in list(map(lambda x: x["coordenadas"], visitados))):
                continue

            custo_ate_aqui = novo_custo
            prioridade = heuristica(folha, objetivo) + novo_custo
            fronteira.put((prioridade, id(folha), folha))
            #registro como um caminho visitado
            visitados.append(folha)

    return visitados

def criar_no(coordenadas, pai = None, custo = 0):
  return {
    "pai": pai,
    "coordenadas": coordenadas,
    "custo": custo
  }

def limpar_caminho(visitados):
  caminho = []
  no = visitados[-1]
  while no is not None:
    caminho.append(no['coordenadas'])
    no = no['pai']
  return caminho[::-1]
def tratar_list_nos_visitados(visitados):
  nos = []
  for no in visitados:
    nos.append(no["coordenadas"])

  return nos

if __name__ == '__main__':
  os.system('cls' if os.name == 'nt' else 'clear')
  x = int(input('Digite a largura do seu labirinto:'))
  y = int(input('Digite a altura do seu labirinto:'))
  labirinto = cria_labirinto(x,y)
  desenha_labirinto(labirinto, x, y)

  i1 = input('Separando por virgula, digite as coordenadas x,y do ponto de início: ')
  (xi,yi) = tuple(int(x) for x in i1.split(","))
  i2 = input('Separando por virgula, digite as coordenadas x,y do objetivo: ')
  (xf,yf) = tuple(int(x) for x in i2.split(","))

  visitados = a_estrela(labirinto, (xi,yi), (xf,yf))
  print('Melhor caminho encontrado:')
  print(limpar_caminho(visitados))
  print('Nós Visitados:')
  print(tratar_list_nos_visitados(visitados))


