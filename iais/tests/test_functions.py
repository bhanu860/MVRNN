'''
Created on Oct 21, 2013

@author: bhanu
'''
import unittest
from iais.data.rnn_data import RNNDataCorpus
from iais.data.params import Params
from nltk.tree import Tree
from unittest.case import SkipTest
import numpy as np
import scipy.io as sio
from iais.util.utils import getRelevantWords
from iais.io.read_corpus import read_srl, create_evalfile_srl, create_srl_data,\
    create_srl_data2
import iais.data.config as config
import os


class Test(unittest.TestCase):

    @SkipTest
    def testloadData(self):
        nExamples = 15
        train_data = '/home/bhanu/Downloads/relationClassification/dataCamera/allDataTrain.mat'
        pre_trained_weights = '/home/bhanu/Downloads/relationClassification/dataCamera/pretrainedWeights.mat'
        rnnData = RNNDataCorpus()
        rnnData.load_data(load_file=train_data, nExamples=nExamples)
        
        params = Params(data=rnnData, wordSize=50, rankWo=3)
        
#        n = params.wordSize; fanIn = params.fanIn; nWords = params.nWords; nLabels = params.categories; rank=params.rankWo
#        theta = np.random.normal(loc=0.0, scale=np.math.pow(10,-5)**2, size = n*(2*n+1) + n*2*n + nLabels*fanIn + n*nWords + (2*n*rank+n)*nWords)
#        
#        #init respective parameters with prior values
#        W, WO, Wcat, Wv, Wo =  unroll_theta(theta, params)
#        Wo[:n,:] = np.ones((n,Wo.shape[1]))  #init word matrices with Identity matrices + epsilon
        #load pre-trained weights here
        mats = sio.loadmat(pre_trained_weights)
        Wv = mats.get('Wv'); W = mats.get('W'); WO = mats.get('WO')
        Wo = np.ndarray(shape=(2*params.wordSize*params.rankWo + params.wordSize)*params.nWords, dtype='float64')
        sentencesIdx = np.arange(nExamples)
        [allSNum_batch, allSNN_batch, Wv_batch, Wo_batch, allWordInds] = getRelevantWords(rnnData, sentencesIdx, Wv,Wo,params) 
        
        print
        
    @SkipTest
    def test_nltk_trees(self):
        parsed_text =  """ (S
    (NP (PRP He))
    (VP (VBZ reckons)
      (SBAR
        (S
          (NP (DT the) (JJ current) (NN account) (NN deficit))
          (VP (MD will)
            (VP (VB narrow)
              (PP (TO to)
                (NP
                  (QP (RB only) (# #) (CD 1.8) (CD billion))))
              (PP (IN in)
                (NP (NNP September))))))))
    (. .)) """ 
#        parsed_text = """(S
#    (S
#      (NP
#        (NP (JJS Most))
#        (PP (IN of)
#          (NP (DT the) (NN commodity) (NN traffic))))
#      (VP (VBD was)
#        (ADJP (RP off))))
#    (, ,)
#    (NP (DT the) (NN company))
#    (VP (VBD said))
#    (. .)) """ 
#        """(S
#    (NP (DT The) (NN cat))
#    (VP (VBD sat)
#      (PP (IN on)
#        (NP (DT a) (NN mat))))
#    (. .))"""
        nltree = Tree.parse(parsed_text)
        nltree.chomsky_normal_form()
        nltree.draw()
    @SkipTest
    def test_loadMat(self):
        mat = sio.loadmat('/home/bhanu/workspace/MVRNN/data/corpus/FinalTestData_srl')
        print
    
    @SkipTest    
    def test_read_srl(self):
        filename = '/home/bhanu/workspace/MVRNN/data/corpus/srl_iob.dev'
        sentences_tags_verbs_ori = read_srl(filename)
        sentences_tags_verbs_pred = read_srl()
#        with open('/home/bhanu/workspace/MVRNN/data/corpus/rawSentences_srl.test', 'w') as wf:
#            for s_ts_vs in sentences_tags_verbs:
#                sentence, tags, verbs = s_ts_vs
#                sentStr = " ".join(sentence) + '\n'
#                wf.write(sentStr); wf.flush()
    @SkipTest             
    def test_create_srleval(self):
        create_evalfile_srl()
    
    @SkipTest
    def test_create_srl_data(self):
        create_srl_data2()
    
    @SkipTest        
    def test_load_srl_data(self):
        rnndata = RNNDataCorpus()
        rnndata.load_data_srl(config.test_data_srl, nExamples=-1)
#        save_dict = {'allSStr':[], 'allSNum':rnndata.allSNum, 'allSTree':rnndata.allSTree, 'sentenceLabels':rnndata.sentenceLabels, 
#                         'allIndicies':rnndata.allIndicies, 'allSKids':rnndata.allSKids, 'categories':rnndata.categories, 'verbIndices':rnndata.verbIndices}
#        sio.savemat('/home/bhanu/workspace/RNTNSocher/data/corpus/srlalldata.test', mdict=save_dict) 
#        print 'saved rnndata..'
    
    @SkipTest
    def test_write_srl_trees(self):
        filenames = [config.corpus_path+'allTrainData_srl.mat', config.corpus_path+'allTestData_srl.mat', config.corpus_path+'allDevData_srl.mat']
        outfilenames = [config.corpus_path+'srl_trees.train', config.corpus_path+'srl_trees.test', config.corpus_path+'srl_trees.dev']
        for infilename, outfilename in zip(filenames, outfilenames):
            data = sio.loadmat(infilename)
            allSTrees = data.get('allSTree').flatten()
            allSStr = data.get('allSStr').flatten()
            for i in range(len(allSTrees)):
                allSTrees[i] = allSTrees[i].flatten()
                allSStr[i] = allSStr[i].flatten()
            
            with open(outfilename+'str', 'w') as wfstr:    
                with open(outfilename, 'w') as wf:
                    for i in range(len(allSTrees)):
                        if(len(allSTrees[i]) == 0):
                            continue
                        stree = allSTrees[i]; sstr = allSStr[i]
                        streeStr = [str(x) for x in stree]
                        sstrnew = [str(x[0]) if len(x)>0 else "" for x in sstr ]
                        wf.write("|".join(streeStr)+'\n')
                        wfstr.write("|".join(sstrnew)+'\n')
                        wf.flush(); wfstr.flush()

    @SkipTest
    def test_write_wiki_trees(self):
        files  = os.listdir(config.corpus_path+'wiki_trees')
        outfilename = config.corpus_path+'wikiRNTN_200K.trees'
        
        wfstr =  open(outfilename+'str', 'w')    
        wf =    open(outfilename, 'w') 
        nuse = 5
        for nf, infilename in enumerate(files):
            print "processing file ", nf
            data = sio.loadmat(config.corpus_path+'wiki_trees/'+infilename)
            allSTrees = data.get('allSTree').flatten()
            allSStr = data.get('allSStr').flatten()
            for i in range(len(allSTrees)):
                allSTrees[i] = allSTrees[i].flatten()
                allSStr[i] = allSStr[i].flatten()            
            
            for i in range(len(allSTrees)):
                if(len(allSTrees[i]) == 0):
                    continue
                stree = allSTrees[i]; sstr = allSStr[i]
                streeStr = [str(x) for x in stree]
                sstrnew = [str(x[0]) if len(x)>0 else "" for x in sstr ]
                wf.write("|".join(streeStr)+'\n')
                wfstr.write("|".join(sstrnew)+'\n')
                
        wf.flush() 
        wfstr.flush()
        wf.close()
        wfstr.close()
        
    @SkipTest
    def test_write_srl_verbIndices(self):
        infilenames = [config.train_data_srl, config.test_data_srl, config.dev_data_srl]
        outfilenames = [config.corpus_path+'srl_vids.train', config.corpus_path+'srl_vids.test', config.corpus_path+'srl_vids.dev']   
        for infilename, outfilename in zip(infilenames, outfilenames):
            rnndata = RNNDataCorpus()
            rnndata.load_data_srl(infilename, nExamples=100) 
            allVerbIndices = rnndata.verbIndices 
            with open(outfilename, 'w') as wf:
                for i in range(len(allVerbIndices)) :
                    verbids = allVerbIndices[i].flatten()
                    verbidsStr = [str(x) for x in verbids]
                    wf.write("|".join(verbidsStr)+"\n")
                    wf.flush()
    @SkipTest
    def test_write_srl_labels(self):
        infilenames = [config.corpus_path+'srl_iob.train', config.corpus_path+'srl_iob.dev', config.corpus_path+'srl_iob.test']
        outfilenames = [config.corpus_path+'srl_labels.train', config.corpus_path+'srl_labels.dev', config.corpus_path+'srl_labels.test'] 
        
        #create categories file, remove infrequent categories
        categories = set() 
        cat_count = dict()     
        for filename in infilenames:  
            sentences_tags_verbs = read_srl(filename)        
            for stv in sentences_tags_verbs:
                _,tagslist,_ = stv
                for tags in tagslist:
                    for tag in tags:
                        tag = tag.strip()
                        categories.add(tag)
                        if(cat_count.has_key(tag)):
                            cat_count[tag] += 1
                        else:
                            cat_count[tag] = 1
        sorted_cat_dict = sorted(cat_count, key=cat_count.get, reverse=True)
        
            
        with open(config.corpus_path+"srl_Freqwithcount.categories", 'w') as wf:
            for i,w in enumerate(sorted_cat_dict):
                print w, cat_count.get(w)
                wf.write(w+" "+str(cat_count.get(w))+'\n')
                
#                            
#        categories = list(categories)
#        catIds = range(len(categories))
#        cat_dict = dict(zip(categories, catIds))   
#        
#        for infilename, outfilename in zip(infilenames, outfilenames):
#            sentences_tags_verbs = read_srl(infilename)
#            with open(outfilename, 'w') as wf:
#                for _, s_ts_vs in enumerate(sentences_tags_verbs): 
#                        _, tagslists, _ = s_ts_vs
#                        rowelements = []
#                        for tagslist in tagslists:
#                            tags = " ".join(tagslist)
#                            rowelements.append(tags)
#                        wf.write("|".join(rowelements)+'\n')
#                        wf.flush()

    @SkipTest
    def test_create_rae_words_file(self):
        print "creating rae words"
        mats = sio.loadmat(config.corpus_path+'vars.normalized.100.mat')    
#        We_orig = mats.get('We')
        words = mats.get('words')
        
        words = words.flatten()
        keys = [str(words[i][0]).strip() for i in range(len(words))]
        with open(config.corpus_path+"rae_words.txt", 'w') as wf:
            for key in keys:
                wf.write(key+"\n")
    
    #@SkipTest
    def test_write_srl_pos(self):
        infilenames = [config.corpus_path+'synt.train.gold', config.corpus_path+'synt.dev.gold', config.corpus_path+'synt.test.pred']
        outfilenames = [config.corpus_path+'srl_pos.train', config.corpus_path+'srl_pos.dev', config.corpus_path+'srl_pos.test'] 
        
        #create categories file, remove infrequent categories
        posSet = set()
        for infilename, outfilename in zip(infilenames, outfilenames):  
            pos = []            
            with open(infilename, 'r') as f:
                tags = [] 
                for line in f:
                    line = unicode(line, 'utf-8').strip()                    
                    if line == '':
                        # last sentence ended
                        pos.append(tags)                                       
                        tags = []
                        continue    
                    parts = line.split()
                    tags.append(parts[0].strip())
                    posSet.add(parts[0].strip())        
            with open(outfilename, 'w') as wf:
                for postags in pos:
                    row = "|".join(postags)
                    wf.write(row+'\n')
        with open(config.corpus_path+"pos_tags.txt", 'w') as wf:
            for tag in posSet:
                wf.write(tag+'\n')
                    
           
                    
                    
            
                
    
        
                        
                
       
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testloadData']
    unittest.main()