'''
Created on Oct 2, 2015 7:00:57 PM
@author: cx

what I do:
    I provide basic class for evaluation
        part of the credit goes to Faegheh Hasibi as I will use her code 
            for consistency
what's my input:
    
what's my output:


'''

import logging

class EntityAnaEvaluatorC(object):
    
    
    @classmethod
    def LoadQAnaResult(cls,InName):
        hQAna = {}
        lLines = open(InName).read().splitlines()
        lvCol = [line.split('\t') for line in lLines]
        lvCol = [vCol for vCol in lvCol if len(vCol) >= 3]
        
        for vCol in lvCol:
            key = vCol[0]
            score = float(vCol[1])
            lMention = vCol[1:]
            if not key in hQAna:
                hQAna[key] = [[lMention,score]]
            else:
                hQAna[key].append([lMention,score])
        logging.info('qana from %s loaded',InName)
        return hQAna
                
        
