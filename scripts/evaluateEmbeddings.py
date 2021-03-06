import sys
import math
from operator import itemgetter
import numpy

def visualize(wordEmbeddings):
    """
    Visualize a set of examples using t-SNE.
    """
    PERPLEXITY=30

    titles = wordEmbeddings.keys()
    titlesStr = ["_".join(y.strip().split()) for y in titles]
    x = numpy.vstack(wordEmbeddings.values())    

    filename = "embeddings.png"
    try:
        #from textSNE.calc_tsne import tsne
        from tsne import tsne
        out = tsne(x, no_dims = 2,perplexity=PERPLEXITY)
        #from textSNE.render import render
        #render([(title, point[0], point[1]) for title, point in zip(titles, out)], filename)
    except IOError:
        print "ERROR visualizing", filename

    data = numpy.column_stack((titlesStr,out))
    numpy.savetxt("/home/bhanu/workspace/RNTN/data/results/embeddings2d_phrase_vis.txt", data, "%s")
    
    #command to plot
    #gnuplot -e plot "./embeddings2d.txt" using 2:3:1 with labels


def euclDistance(vec1, vec2):
    dist = 0
    
    if len(vec1) != len(vec2):
        raise ValueError('len(Vec1)!=len(Vec2) '+str(len(vec1))+"!="+str(len(vec2)))
    for i in range(len(vec1)):
        dist += (vec1[i] - vec2[i]) ** 2
        
    return math.sqrt(dist)

def distance(vec1, vec2):
    return euclDistance(vec1, vec2)

def nNearestNeighbours(word, n, wordEmbeddings):
    distances = []
    
    for key in wordEmbeddings.keys():
        dist = distance(wordEmbeddings[word],wordEmbeddings[key])
        word_dist_pair = (key,dist)
        distances.append(word_dist_pair)
  
    return sorted(distances,key=itemgetter(1))[:n]    

def readEmbeddingsfromFile(file,nRows=-1):
    """
    nRows: no of rows to read
    """
    embeddingsDict = {}
    f = open(file)
    iRow = 0
    for row in f:
        values = row.split('\t')
        phrase = values[0]
        embStr = [x.strip() for x in values[1].split()]
        embeddings = map(float, embStr)
#        sumE = sum(embeddings)
        #if not (sumE > 0.999 and sumE<1.001):
        #    print "Not Normalised Embeddings. sum=" + str(sumE) + " for " + phrase
        embeddingsDict[phrase] = embeddings
        iRow += 1
        if (nRows != -1) and (iRow > nRows):
            break
    f.close()
    print "loaded embeddings of size: " + str(iRow)
    return embeddingsDict    

def main():
#    file = sys.argv[1]
    file = '/home/bhanu/workspace/MVRNN/data/results/phrases_vectors_srl.txt'
#    nuse = sys.argv[2]
    #nwords = sys.argv[2]
    phrase = sys.argv[1]
    n = 10
    
    phraseEmbDict = readEmbeddingsfromFile(file, nRows=-1)
    
    nearPhrases =  nNearestNeighbours(phrase, n, phraseEmbDict)   
#    print "dimensions of embeddigns", len(phraseEmbDict["."])
    for phrase in nearPhrases:
        print phrase[0]
    
#    visualize(phraseEmbDict)

if __name__ == "__main__":
    main()
