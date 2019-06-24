import gensim.downloader as api
import numpy as np 
import pandas as pd
import re
import multiprocessing as mp
import os

def get_vects(start):
    list_of_dicts=[]
    list_of_vectors=[]
    mean_of_def_vectors=[]
    #iterate through the definitions and make them a list of words
    for i in range(start,start+1000):
        print(words[i]," ",all_def[i]," ",i,"\n")
        list_of_words = all_def[i].split(" ")
        #iterate through each word and get the vector
        for j in list_of_words:
            if j in fasttext_model300.wv.vocab:
                list_of_vectors.append(fasttext_model300.wv.word_vec(j))
        two_dim = np.vstack(tuple(list_of_vectors))
        #get mean across cols
        dicti={}
        dicti["word"]=words[i]
        dicti["definition"]=all_def[i]
        dicti["vector"]=np.mean(two_dim, axis = 0)
        list_of_dicts.append(dicti)
    print("yo this means one batch of 10k is doneeee")
    #return mean_of_def_vectors
    return list_of_dicts
    
#download the model
fasttext_model300 = api.load('fasttext-wiki-news-subwords-300')

#read dataset and drop definitions that are not present
df = pd.read_csv("Downloads/urbandic.csv",
        header=0,
        usecols=["word", "definition"])
df = df.dropna(subset=['definition'])

#clean up the definitions and append to the list of definitons
for defn in df['definition']:
    defn=re.sub(r' \n','\n',defn)#remove redundant spaces before \n
    defn=re.sub(r'\t+',' ',defn)#remove \t 
    defn=re.sub(r'\n+',' ',defn)#replace \n with \s
    defn=re.sub(r'[?!;,.]+',' ',defn)#replace ?,!,; and their combinations with \s
    defn=re.sub(r'\s+',' ',defn)#remove multiple \s
    defn = defn.strip() #remove redundant spaces
    all_def.append(defn)

#make a list of words
words = df['word'].tolist()

#Make vectors in batches of 10000 (mnanually), where each 1000 records are processed parallely
pool = mp.Pool(processes=(mp.cpu_count()-1))
results=pool.map(get_vects,[0,1000,20000,3000,4000,5000,6000,7000,8000,9000])  #this will run till 200000
pool.close()
pool.join()

joined_results=[]
for i in results:
    joined_results+=i
print(len(joined_results))
import os, json
joined_results=[]
for i in results:
    joined_results+=i
print(len(joined_results))

filename = "w2voutput.txt"
if os.path.exists(filename):
    append = 'a'
else:
    append = 'w'
with open(filename, append) as fp:
    fp.write(str(joined_results))
