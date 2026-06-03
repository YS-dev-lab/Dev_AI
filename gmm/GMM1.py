from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


iris = load_iris()
features_names = ['sl','sw', 'pl', 'pw']

irisDF = pd.DataFrame(data=iris.data,\
                        columns = features_names)
irisDF['target'] = iris.target
gmm = GaussianMixture(n_components=3,\
    random_state=17).fit(iris.data)

gmm_labels = gmm.predict(iris.data)

irisDF['gmm_cluster'] = gmm_labels
print(\
    irisDF.groupby('target')['gmm_cluster'].value_counts())
xynew = gmm.sample(10)

'''

.groupby('target')	실제 정답 레이블 기준으로 그룹 분리	그룹 기준 열 이름
['gmm_cluster']	그 그룹 안에서 군집 열만 선택	열 이름
.value_counts()	각 군집 번호가 몇 번 나왔는지 카운트	없음 → GMM이 실제 종류와 얼마나 일치하는지 확인

'''




n_c = np.arange(1,21)
models=[GaussianMixture(n,\
    random_state=17).fit(iris.data) for n in n_c]

plt.plot(\
    n_c , [m.bic(iris.data) for m in models], label = 'BIC')

plt.plot(\
    n_c, [m.aic(iris.data) for m in models], label = 'AIC')

plt.legend()
plt.xlabel('n_components')
plt.savefig('iris_gmm.png')


