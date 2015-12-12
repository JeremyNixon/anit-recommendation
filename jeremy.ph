import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data_jeremy = pd.read_csv('scraper/data.csv')

links = list(set(list(data_jeremy['link'])))
users = list(set(list(data_jeremy['Facebook user id'])))

matrix = pd.DataFrame(np.zeros((len(links), len(users))))
matrix.index = links
matrix.columns = users

for i in data_jeremy.iterrows():
    matrix.loc[i[1][0], i[1][2]] = 1

for i in matrix:
    if sum(matrix[i]) == 1:
        matrix.drop(i, 1, inplace=True)

        
def PCA(matrix):
    A = matrix
    M = (A-np.mean(A.T,axis=1)).T # subtract the mean (along columns)
    [latent,coeff] = np.linalg.eig(np.cov(M)) # attention:not always sorted
    score = np.dot(coeff.T,M) # projection of the data in the new space
    return coeff,score,latent

matrix = matrix.T
coef, score, eigenvalues = PCA(matrix)

principal_components = coef[:,:2]
compressed = np.dot(matrix, principal_components)

principal_components = coef[:,:2]
compressed = np.dot(matrix, principal_components)
plt.scatter(compressed[:,0], compressed[:,1])
plt.show()