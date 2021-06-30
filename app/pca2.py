import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# O PCA é uma ferramenta muito flexível e permite a análise de conjuntos de dados que podem conter, por exemplo, multicolinearidade, valores ausentes,
# dados categóricos e medições imprecisas. O objetivo é extrair as informações importantes dos dados e expressar essas informações como um conjunto 
# de índices resumidos chamados de componentes principais .

# Estatisticamente, o PCA encontra linhas, planos e hiperplanos no espaço dimensional K que se aproximam dos dados o melhor possível no sentido 
# de mínimos quadrados. Uma linha ou plano que é a aproximação de mínimos quadrados de um conjunto de pontos de dados torna a variação das 
# coordenadas na linha ou plano o maior possível.

# Uma maneira mais comum de acelerar um algoritmo de aprendizado de máquina é usando a Análise de Componentes Principais (PCA)
# Se seu algoritmo de aprendizado for muito lento porque a dimensão de entrada é muito alta, usar o PCA para acelerá-lo pode ser uma escolha razoável

# Dataset utilizado
df = pd.read_csv('datasets/BITSTAMP_BTCUSD_1D.csv')

# Features utilizadas do Dataset, exclui Date e Close (target)
features = ['open', 'high', 'low', 'Volume', 'Volume MA', 'RSI']

# Separando as features
x = df.loc[:, features].values

# Separando o target
y = df.loc[:,['close']].values

# O StandardScaler ajuda a padronizar os recursos do conjunto de dados em escala de unidade (média = 0 e variância = 1)
x = StandardScaler().fit_transform(x)

# Devo observar que, após a redução da dimensionalidade, geralmente não há um significado particular atribuído a cada componente principal. 
# Os novos componentes são apenas as duas principais dimensões de variação.

# Escolhe o número mínimo de componentes principais, de forma que 95% da variação seja retida.
pca = PCA(.95)
principalComponents = pca.fit_transform(x)

array = []; 
for i in range(0, pca.n_components_, 1) : 
  array.append('Principal Component ' + str(i))

principalDf = pd.DataFrame(data = principalComponents
             , columns = array)

finalDf = pd.concat([principalDf, df[['close']]], axis = 1)

# Importante ressaltar que podemos escolher quantas dimensões queremos ou então o grau de variância

print(finalDf)

print(pca.explained_variance_ratio_)

# A variação explicada informa quanta informação (variação) pode ser atribuída a cada um dos componentes principais. Isso é 
# importante, porque embora você possa converter espaço de 4 dimensões em espaço de 2 dimensões, você perde parte da variância (informações) ao fazer isso. 
