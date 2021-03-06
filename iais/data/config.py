'''
Created on Oct 30, 2013

@author: bhanu
'''
import socket

computerName = socket.gethostname()
if(computerName.startswith('kd')):
    PROJECT_HOME = '/home/bpratap/workspace/MVRNN'
else:
    PROJECT_HOME = '/home/bhanu/git/MVRNN/MVRNN'

parsed_file =           PROJECT_HOME+'/data/corpus/parsed.txt' 
cw_embeddings_file =    PROJECT_HOME+'/data/corpus/CW_embedddings.mat' 
train_data =            PROJECT_HOME+'/data/corpus/allDataTrain.mat' 
pre_trained_weights =   PROJECT_HOME+'/data/corpus/pretrainedWeights.mat' 
saved_params_file =     PROJECT_HOME+'/data/models/tuned_params'
test_data  =            PROJECT_HOME+'/data/corpus/allDataTest.mat' 
test_labels_output =    PROJECT_HOME+'/data/results/test_predictions.txt' 
results_path        =   PROJECT_HOME+'/data/results/'
semeval_testKeys    =   PROJECT_HOME+'/data/results/TEST_FILE_KEY.TXT'
test_data_srl       =   PROJECT_HOME+'/data/corpus/FinalTestData_srl2.mat'
dev_data_srl       =   PROJECT_HOME+'/data/corpus/FinalDevData_srl2.mat'
train_data_srl       =   PROJECT_HOME+'/data/corpus/FinalTrainData_srl2.mat' 
model_path          =   PROJECT_HOME+'/data/models/'
corpus_path         =   PROJECT_HOME+'/data/corpus/'
