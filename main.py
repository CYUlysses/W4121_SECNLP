from senti_scoring import *
import pickle

os.chdir('redata')

filedict = {}
for fileind, onefile in enumerate(os.listdir()):
    if fileind >= 5:
        break
    alltxt = read_bulk(onefile)
    testlist = get_candidates(alltxt)
    docscore = find_scores(testlist)
    filedict[onefile[0:-4]] = docscore

with open('somedata.pickle','wb') as handle:
    pickle.dump(filedict, handle, protocol=pickle.HIGHEST_PROTOCOL)

os.chdir('..')