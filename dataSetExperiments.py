import os
import glob
import individualModules as im
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import math
import pickle
from sklearn.decomposition import PCA
from algorithms import kMeans as kmeans

from sklearn.cluster import KMeans
from gensim.models.keyedvectors import KeyedVectors

style.use('ggplot')

trainingModelGoogle = KeyedVectors.load_word2vec_format("models/GoogleNews-vectors-negative300.bin",binary=True,limit=100000)
im.setModel(trainingModelGoogle)

def getDocumentsValues(listOfHandles):
    vectors=[]

    for handle in listOfHandles:
        vec=im.getDocVector(handle)
        if(len(vec)>0):
            vectors.append(vec)

    docArray=np.asarray(vectors,dtype=np.float32)
    #print(docArray)
    #print("Doc array shap",docArray.shape)
    pca= PCA(n_components=2)
    pcaOut=pca.fit_transform(docArray)
    #U, s, V = np.linalg.svd(A)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    values=[]
    """
    print("Pcaout")
    print(pcaOut)
    print(pcaOut.shape)
    print("components")
    print(pca.components_)
    print(pca.components_.shape)
    print("singular")
    print(pca.singular_values_)
    print(pca.singular_values_.shape)
"""

    for vec in vectors:
        sum=0
        values.append([vec[0],vec[1]])
    return pcaOut

def openListOfFiles(path):
    fileHandles = []
    for filename in glob.glob(os.path.join(path, '*.txt')):
        singleHandle = open(filename,"r")
        fileHandles.append(singleHandle)
    return fileHandles

def closeFileHandles(handleList):
    for i in handleList:
        i.close()

def plotReadyFunc(path):
    handles=openListOfFiles(path)
    values= getDocumentsValues(handles)
    #print(values)
    closeFileHandles(handles)
    return values

"""
DocumentWordVectorValues=im.plotDocumentWords(fileHandles[2])
print(DocumentWordVectorValues)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(DocumentWordVectorValues,"bo")
plt.title("Word Vectors")
plt.show()
fileHandles[2].seek(0)
"""



#reading files and storing first two values of each document

path1 = "datasets/bbc/politics"
path2 = "datasets/bbc/business"
path3 = "datasets/bbc/tech"
path4 = "datasets/bbc/entertainment"
path5 = "datasets/bbc/sport"

plot1=np.array(plotReadyFunc(path1))
plot2= np.array(plotReadyFunc(path2))
plot3=np.array(plotReadyFunc(path3))
plot4 = np.array(plotReadyFunc(path4))

total =[]
for d in plot1:
    total.append(d)
for d in plot2:
    total.append(d)

for d in plot3:
    total.append(d)
for d in plot4:
    total.append(d)
"""
valueDumpFile1 = open("datasets/bbc/politics.pickle","rb")
plot1=pickle.load(valueDumpFile1)

valueDumpFile1 = open("datasets/bbc/business.pickle","rb")
plot2=pickle.load(valueDumpFile1)

valueDumpFile1 = open("datasets/bbc/tech.pickle","rb")
plot3=pickle.load(valueDumpFile1)

valueDumpFile1 = open("datasets/bbc/entertainment.pickle","rb")
plot4=pickle.load(valueDumpFile1)
"""

fig = plt.figure()
ax = plt.subplot(111)
"""
clf= KMeans(n_clusters=4)
clf.fit(plot1)

clusters = clf.cluster_centers_
labels = clf.labels_
plt.scatter(clusters[:,0],clusters[:,1],marker='X',size=5)

"""
ax.scatter(plot1[:,0],plot1[:,1],s=5,linewidths=5)
line1=ax.plot(plot1[:,0],plot1[:,1],"bo",label="Politics")
line2=ax.plot(plot2[:,0],plot2[:,1],"ro",label='Business')
line3=ax.plot(plot3[:,0],plot3[:,1],"go",label="Tech")
line4=plt.plot(plot4[:,0],plot4[:,1],"yo",label="Entertainment")
ax.legend()
fig.add_subplot(ax)
#fig.add_subplot(aq)
plt.show()

temp=open("datasets/bbc/002.txt","r")
plotValue,correspondingWord=im.plotDocumentWords(temp)
plotValue= np.array(plotValue)

colors = 100*["r","g","b","c","k","l","p"]
(classifications,centroids)=kmeans.execute_kmeans(total,k=5,showPlot=True,plotRef=plt)
x=[]
y=[]
"""
count = 0
for centroid in centroids:
    plt.scatter(centroids[centroid][0], centroids[centroid][1], marker="o", color=colors[count], s=100,
                 linewidths=5)
    count = count + 1

for classification in classifications:
    color = colors[classification]
    if len(classifications[classification]) > 0:
        for featureSet in classifications[classification]:
            plt.scatter(featureSet[0], featureSet[1], marker="x", color=color, s=100, linewidths=5)

"""
for k in plotValue:
    x.append(k[0])
    y.append(k[1])
#plt.scatter(x,y,linewidths=2,s=5)
for i in range(len(correspondingWord)):
    xy=(x[i],y[i])
    plt.annotate(correspondingWord[i],xy)
plt.show()