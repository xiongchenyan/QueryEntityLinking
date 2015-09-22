'''
Created on Sep 11, 2015 4:17:13 PM
@author: cx

what I do:
    I collect surface form from FACC1 or Fakba annotations
what's my input:
    FACC1/Fakba data dir
what's my output:
    a file of 
    obj id \t surface form \t count


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from collections import Counter
from cxBase.WalkDirectory import WalkDir
from cxBase.Conf import cxConfC
import logging
import os
import heapq

MaxKeyPerFile = 100000
InType = 'facc'

def ReadAllPairs(InName):
    lvCol = [line.split('\t') for line in open(InName).read().splitlines()]
    global InType
    if 'facc' == InType:
        lPair = [vCol[2] + '\t' + vCol[7] for vCol in lvCol if len(vCol) >= 8]
    else:
        lPair = [vCol[0] + '\t' + vCol[-1] for vCol in lvCol if len(vCol) > 5]

    return Counter(lPair)



def CountObjSurfacePairs(InDir,OutDir):
    lFName = WalkDir(InDir)
    
    global MaxKeyPerFile
    
    OutCnt = 0
    TotalCount = Counter()
    for FName in lFName:
        logging.info('working on file [%s]',FName)
        OneCount = ReadAllPairs(FName)
        logging.info('%d pair',len(OneCount))
        TotalCount.update(OneCount)
        
        if len(TotalCount) >=  MaxKeyPerFile:
            OutName = OutDir + '/%d' %(OutCnt)
            logging.info('counter too large [%d], dumpping to [%s]', len(TotalCount), OutName)
            out = open(OutName,'w')
            l = TotalCount.items()
            l.sort(key=lambda item:item[0])
            logging.info('sorted')
            for item in l:
                print >>out, '%s\t%d' %(item[0],item[1])
                
            out.close()
            logging.info('dumpped')
            TotalCount.clear()
            OutCnt += 1
    
    logging.info('counted, total [%d] tmp file',OutCnt)        
    return OutCnt


def MergeToFinalOut(TempDir,TempCnt,OutName):
    out = open(OutName,'w')
    lIn = [open(TempDir + '/%d' %(i)) for i in range(TempCnt)]
    
    CurrentKeyCnt = ['',0]
    TotalPairCnt = 0
    for LineCnt,line in enumerate(heapq.merge(*lIn)):
        vCol = line.strip().split('\t')
        key = '\t'.join(vCol[:2])
        cnt = int(vCol[2])
        
        if CurrentKeyCnt[0] == "":
            CurrentKeyCnt = [key,cnt]
            continue
        
        if CurrentKeyCnt[0] != key:
            print >>out, '%s\t%d' %(CurrentKeyCnt[0],CurrentKeyCnt[1])
            TotalPairCnt += 1
            CurrentKeyCnt = [key,cnt]
        else:
            CurrentKeyCnt[1] += cnt
            
        if 0 == (LineCnt % 10000):
            logging.info('merged [%d] lines [%d] pair',LineCnt,TotalPairCnt)
            
    print >>out, '%s\t%d' %(CurrentKeyCnt[0],CurrentKeyCnt[1])
    out.close()
    logging.info('merged, total get %d pair',TotalPairCnt)
    return True
        
        
        
    
            
        
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I collect all obj id surface form pairs'
        print 'conf\n'
        print 'anain\nintype facc|fakba\nout\nmaxlinepertmp'
        sys.exit()
    conf = cxConfC(sys.argv[1])
    
    LogLevel = logging.INFO
    if conf.GetConf('loglevel') == 'debug':
        LogLevel = logging.DEBUG
        
    root = logging.getLogger()
    root.setLevel(LogLevel)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(LogLevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)  
    
    AnaInDir = conf.GetConf('anain')
    InType = conf.GetConf('intype')
    OutName = conf.GetConf('out')
    MaxKeyPerFile = conf.GetConf('maxlinepertmp',MaxKeyPerFile)
    
    TempDir = OutName + '_tmp/'
    if not os.path.exists(TempDir):
        os.mkdir(TempDir)
        
    
    TempCnt = CountObjSurfacePairs(AnaInDir,TempDir)
    MergeToFinalOut(TempDir, TempCnt, OutName)
    
      