'''
Created on Sep 22, 2015 8:12:21 PM
@author: cx

what I do:
    I simply merge multiple surface form file
what's my input:
    file names of surface form file, must be sorted
        surface form     object   score
what's my output:
    a merged file, score added

'''


import sys
import heapq



if len(sys.argv) < 4:
    print 'I merge multiple surface form file into one'
    print 'parameter [inputs]*n + output'
    sys.exit()
    

print "reading input: " + sys.argv[1:-1]    
lIn = [open(InName) for InName in sys.argv[:-1]]

CurrentText = ""
CurrentScore = 0
out = open(sys.argv[-1],'w')
for LineCnt,line in enumerate(heapq.merge(*lIn)):
    vCol = line.strip().split('\t')
    if len(vCol) < 3:
        print 'format error [%s]' %(line)
        break
    text = vCol[:2]
    score = float(vCol[2])
    
    if CurrentText == "":
        CurrentText = text
        CurrentScore = score
        
    if CurrentText != text:
        print >> out, CurrentText + '\t%f' %(CurrentScore)
        CurrentText = text
        CurrentScore = score
    else:
        CurrentScore += score
        
print >>out, CurrentText + '\t%f' %(CurrentScore)
out.close()
print 'finished'
        
    

