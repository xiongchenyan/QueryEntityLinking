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
        
    return ResStr



def Process(QIn, GroundTruthIn,AnaIn,OutName):
    hTrueQAna = EntityAnaEvaluatorC.LoadQAnaResult(GroundTruthIn)
    hPredQAna = EntityAnaEvaluatorC.LoadQAnaResult(AnaIn)
    
    lvCol = [line.strip().split('\t') for line in open(QIn)]
    lQidQuery = [vCol[1:3] for vCol in lvCol]
    
    out = open(OutName,'w')
    for qid,query in lQidQuery:
        res = ProcessOneQ(qid, query, hTrueQAna, hPredQAna)
        if "" != res:
            print >>out, res
    out.close()
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


    
    
