import numpy as np
import pandas as pd
from scipy.cluster.vq import vq, kmeans, whiten
import time

def PCA(matrix):
    A = matrix
    M = (A-np.mean(A.T,axis=1)).T # subtract the mean (along columns)
    [latent,coeff] = np.linalg.eig(np.cov(M)) # attention:not always sorted
    score = np.dot(coeff.T,M) # projection of the data in the new space
    return coeff,score,latent

def process():
    data = pd.read_csv('scraper/data.csv')

    links = list(set(list(data['link'])))
    users = list(set(list(data['Facebook user id'])))

    print "Links"
    print links[:5]
    print "Users"
    print users[:5]

    matrix = pd.DataFrame(np.zeros((len(links), len(users))))
    matrix.index = links
    matrix.columns = users

    print "matrix_size:",
    print matrix.shape

    for i in data.iterrows():
        matrix.loc[i[1][0], i[1][2]] = 1

    start = time.time()
    for count, i in enumerate(matrix):
        if count % (len(matrix)/10) == 0:
            print 'Count = %r/%r' %(count,len(matrix))
        if sum(matrix[i]) == 1:
            matrix.drop(i, 1, inplace=True)
    print 'Time for drop = %r' %(time.time() - start)

    matrix = matrix.T
    coef, score, eigenvalues = PCA(matrix)

    principal_components = coef[:,:2]
    print "Principal Components"
    print principal_components
    print "Eigenvalues"
    print eigenvalues
    compressed = np.dot(matrix, principal_components)

    # we might want to choose something better than just 10 here
    principal_components = coef[:,:10]
    compressed = np.array(np.dot(matrix, principal_components), dtype=float)

    # hard coded in number of clusters
    compressed_centroids = kmeans(compressed, 15)
    centroids = []
    for centroid in compressed_centroids[0]:
        centroids.append(np.dot(principal_components, centroid))

    return centroids, links, users
