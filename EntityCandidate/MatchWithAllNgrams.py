'''
Created on Sep 22, 2015 7:20:13 PM
@author: cx

what I do:
    I match all surface form-> obj pair in given data, if surface form
        appears in given query list's ngrams
    For now it is case insensitive
what's my input:
    surface form -> obj -> score triple file
    query
what's my output:
    surface form -> obj -> score file, filtered to only those useful ones

'''

import sys


def EnumerateNgram(s):
    lTerm = s.split()
    lNgram = []
    for i in range(len(lTerm)):
        for j in range(i + 1,len(lTerm) + 1):
            lNgram.append(' '.join(lTerm[i:j]))
    return lNgram
            

def GetNgramForQuery(QIn):
    lQuery = [line.split('\t')[-1] for line in open(QIn).read().splitlines()]
    
    llNgram = [EnumerateNgram(query.lower()) for query in lQuery]
    sNgram = set(sum(llNgram,[]))
    return sNgram


def FindTargetNgram(SurfaceIn,sNgram,OutName):
    
    out = open(OutName,'w')
    
    for cnt,line in enumerate(open(SurfaceIn)):
        line = line.strip()
        key = line.split('\t')[0].lower()
        if key in sNgram:
            print >>out, line
        if 0 == (cnt % 10000):
            print "processed [%d] lines" %(cnt)
    
    out.close()
    print 'target ngram matched'
    return


if 4 != len(sys.argv):
    print 'surface form data + query + out'
    sys.exit()
    
sNgram = GetNgramForQuery(sys.argv[2])

FindTargetNgram(sys.argv[1], sNgram, sys.argv[2])
        
        
    
    
    
    
    
    
    
