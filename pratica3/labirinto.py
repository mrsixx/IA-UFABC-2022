from random import shuffle, randrange

def cria_labirinto(larg = 8, alt = 3):
  vis = [[0] * larg + [1] for _ in range(alt)] + [[1] * (larg + 1)] 
  sem_muros = []

  def quebra_muros(lin, col):
    vis[lin][col] = 1
    d = [(lin, col + 1), (lin, col - 1), (lin - 1, col), (lin + 1, col)]
    shuffle(d)

    for (l, c) in d:
      if vis[l][c] != 1:
        sem_muros.append((lin, col, l, c))
        quebra_muros(l, c)

  quebra_muros(randrange(alt), randrange(larg))
  return(sem_muros)

def desenha_labirinto(lab, larg = 8, alt = 3):
  ver = [['|  '] * larg + ['|'] for _ in range(alt)] + [[]]
  hor = [['+--'] * larg + ['+'] for _ in range(alt + 1)]

  for (l1, c1, l2, c2) in lab:
    if l1 == l2:
      ver[l1][max(c1, c2)] = '   '
    if c1 == c2:
      hor[max(l1, l2)][c1] = '+  '

  for (a, b) in zip(hor, ver):
    print(''.join(a + ['\n'] + b))