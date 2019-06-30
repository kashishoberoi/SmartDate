import gensim.downloader as api
import numpy as np 
import pandas as pd
import re
import multiprocessing as mp
import os, json


def get_vects(start):
    list_of_dicts=[]
    list_of_vectors=[]
    mean_of_def_vectors=[]
    #iterate through the definitions and make them a list of words
    for i in range(start,start+5000):
        #print(words[i]," ",all_def[i]," ",i,"\n")
        list_of_words = all_def[i].split(" ")
        #iterate through each word and get the vector
        if(len(list_of_words)>0):
            for j in list_of_words:
                if j in fasttext_model300.wv.vocab:
                    list_of_vectors.append(fasttext_model300.wv.word_vec(j))
            two_dim = np.vstack(tuple(list_of_vectors))
            #get mean across cols
            #dicti={}
            filename = "Documents/SmartDate/src/embeddings/w2voutput.txt"
            if os.path.exists(filename):
                append = 'a'
            else:
                append = 'w'
            with open(filename, append) as fp:
                fp.write(str(words[i])+str("\t")+str(all_def[i])+str("\t")+str(np.mean(two_dim, axis = 0))+str("\n"))

            #dicti["word"]=words[i]
            #dicti["definition"]=all_def[i]
            #dicti["vector"]=np.mean(two_dim, axis = 0)
            #list_of_dicts.append(dicti)
    print("yo this means one batch of 10k is doneeee")
    #return mean_of_def_vectors
    return 0


#download the model
fasttext_model300 = api.load('fasttext-wiki-news-subwords-300')

#read dataset and drop definitions that are not present
df = pd.read_csv("urbandic.csv",
        header=0,
        usecols=["word", "definition"])
df = df.dropna(subset=['definition'])
    
#clean up the definitions and append to the list of definitons
all_def=[]
for defn in df['definition']:
    defn=re.sub(r' \n','\n',defn)#remove redundant spaces before \n
    defn=re.sub(r'\t+',' ',defn)#remove \t 
    defn=re.sub(r'\n+',' ',defn)#replace \n with \s
    defn=re.sub(r'[?!;,.]+',' ',defn)#replace ?,!,; and their combinations with \s
    defn=re.sub(r'\s+',' ',defn)#remove multiple \s
    defn = defn.strip() #remove redundant spaces
    all_def.append(defn)


words = df['word'].tolist()

pool = mp.Pool(processes=(mp.cpu_count()-1))
results=pool.map(get_vects,[0,5000,10000,15000,20000,25000,30000,35000,40000,45000]) #get vectors in batches of 50k
pool.close()
pool.join()


