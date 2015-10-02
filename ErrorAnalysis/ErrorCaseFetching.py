'''
Created on Oct 2, 2015 6:55:07 PM
@author: cx

what I do:
    fetch the results that is different with qrel
what's my input:
    queries
    annotated query ground truth
    annotated results
what's my output:
    the failed ones

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryEntityLinking')
import sys
from cxBase.Conf import cxConfC
from EvaluateLinking.EntityAnaEvaluator import EntityAnaEvaluatorC


def ProcessOneQ(qid,query,hTrueQAna,hPredQAna):
    
    lTrueAna = []
    lPredAna = []
    
    if qid in hTrueQAna:
        lTrueAna = hTrueQAna[qid]
    if qid in hPredQAna:
        lPredAna = hPredQAna[qid]
    lTrueAna = ['\t'.join(item[0]) for item in lTrueAna]
    lPredAna = ['\t'.join(item[0]) for item in lPredAna]    
    lTrueAna.sort()
    lPredAna.sort()
    
    ResStr = ""
    if lTrueAna != lPredAna:
        ResStr += qid + '\t' + query + '\n\n'
        ResStr += 'GroundTruth\n'
        ResStr += '\n'.join(lTrueAna) + '\n\n'
        ResStr += 'Predicted\n'
        ResStr += '\n'.join(lPredAna) + '\n'
        ResStr += '\n\n'
    
        
    return ResStr,len(lTrueAna),len(lPredAna)



def Process(QIn, GroundTruthIn,AnaIn,OutName):
    hTrueQAna = EntityAnaEvaluatorC.LoadQAnaResult(GroundTruthIn)
    hPredQAna = EntityAnaEvaluatorC.LoadQAnaResult(AnaIn)
    
    lQidQuery = [line.strip().split('\t') for line in open(QIn)]
    
    OutAdd = open(OutName + '_Add','w')
    OutMiss = open(OutName + '_Miss','w')
    OutMistake = open(OutName + '_Error','w')
    for qid,query in lQidQuery:
        res,CntTrue,CntAna = ProcessOneQ(qid, query, hTrueQAna, hPredQAna)
        if "" != res:
            if CntTrue == 0:
                print >>OutAdd, res
                continue
            if CntAna == 0:
                print >> OutMiss,res
                continue
            print >>OutMistake, res
            
    OutAdd.close()
    OutMiss.close()
    OutMistake.close()
    print 'finished'
    return True


if 2 != len(sys.argv):
    print 'I find error annotated queries'
    print 'conf:\nqin\ngroundtruthana\ntargetana\nout'
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])
QIn = conf.GetConf('qin')
GroundTruthIn = conf.GetConf('groundtruthana')
AnaIn = conf.GetConf('targetana')
OutName = conf.GetConf('out')
Process(QIn,GroundTruthIn,AnaIn,OutName)


    
    
