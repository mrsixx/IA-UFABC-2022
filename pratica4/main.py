#https://archive.ics.uci.edu/ml/datasets/Heart+failure+clinical+records
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn import neighbors
from sklearn import cluster
from sklearn import metrics
from sklearn.model_selection import train_test_split
import math
import matplotlib.pyplot as plt
from scipy import stats

#plota o grafico do erro quadratico e da silhueta dos agrupamentos
def plotar_graficos(n_classes, max_grupos, erro_quadratico, silhueta):
  plt.plot(np.arange(n_classes - 1, max_grupos + 1), erro_quadratico)
  plt.savefig('erro_quadratico')
  plt.clf()

  plt.plot(np.arange(n_classes, max_grupos + 1), silhueta)
  plt.savefig('silhueta')
  plt.clf()

#retorna uma tupla na forma (erro_quadratico_i, silhueta_i)
def metricas_agrupamento(X, n_clusters):
  agrup = cluster.KMeans(n_clusters = n_clusters)
  agrup.fit(X)

  eq = agrup.inertia_

  if(n_clusters == 1):
    return (eq, 0)

  sil = metrics.silhouette_score(X, agrup.labels_)
  return (eq, sil)

#importa a base de base
base = np.loadtxt('heart.csv', dtype = float, delimiter = ',', skiprows = 1)
y = base[:, -1]
X_bruto = base[:, 0:-1]


#montagem do experimento
experimento = make_pipeline(preprocessing.StandardScaler(), neighbors.KNeighborsClassifier(3))
res = cross_val_score(experimento, X_bruto, y, cv = 10)
#print(np.mean(res))
#print(np.std(res))

#normalização da base
scl = preprocessing.StandardScaler()
scl.fit(X_bruto)
X_scl = scl.transform(X_bruto)

#separo a base de teste e a de treino
X_train, X_test, y_train, y_test = train_test_split(X_scl, y, test_size = 0.3)


#para escolher o melhor número de grupos, faremos o fit para cada número de grupos e pegaremos a maior silhueta

n_classes = np.unique(y_train).shape[0]
max_grupos = round(math.sqrt(y_train.shape[0]))

erro_quadratico = []
silhueta = []

# métricas para 1 grupo
(erro_quadratico_i, silhueta_i) = metricas_agrupamento(X_train, n_classes - 1)
erro_quadratico.append(erro_quadratico_i)

#calculo as métricas para cada n_grupos entre n_classes e max_grupos+1
for i in range(n_classes, max_grupos + 1):
  (erro_quadratico_i, silhueta_i) = metricas_agrupamento(X_train, i)
  erro_quadratico.append(erro_quadratico_i)
  silhueta.append(silhueta_i)


#ploto os graficos para facilitar a validação
plotar_graficos(n_classes, max_grupos, erro_quadratico, silhueta)

#obtenho o melhor numero de grupos a partir da análise acima e faço o agrupamento na base de treino
#melhor_n_grupos = 16
melhor_n_grupos = np.argmax(silhueta) + 1
print("melhor n de grupos: {}".format(melhor_n_grupos))

#faço o agrupamento na base de treino usando o melhor numero de grupos obtido
agrup = cluster.KMeans(n_clusters = melhor_n_grupos)
agrup.fit(X_train)
grupos = agrup.labels_

grupos_classes = []
for i in range(0, melhor_n_grupos):
  grupos_classes.append(stats.mode(y_train[grupos == i])[0][0])

# faço o predict na base de testes
y_predict = agrup.predict(X_test)

#obtenho as classes dos grupos do predict
y_predict_classes = []
for i in y_predict:
  y_predict_classes.append(grupos_classes[i])

#comparo o predict dos testes com os valores reais do teste
acertos = (y_predict_classes == y_test)
total = y_test.shape[0]
print("Acertou {} de {} ({}%)".format(acertos.sum(), total, (acertos.sum()/total)*100))
#print(y_predict_classes)
#print(y_test)
#print(acertos)


#Atividade:
#- Utilizar o agrupamento para classificar novos pacientes da seguinte forma:
#- 1. divida a base para treinamento e teste
#- 2. realize o agrupamento na base de treinamento
#- 3. utilize a função predict do agrupamento para classificar a base de teste (analisando a qual classe pertence o grupo indicado pelo predict)
#- 4. calcule a média de acerto
#- A divisão em treinamento e teste pode ser feita com o método holdout (como na  Prática 4), ou k-fold crossvalidation valendo bônus na nota.