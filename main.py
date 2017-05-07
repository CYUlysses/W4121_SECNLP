from senti_scoring import *
import shutil

datafolder = 'data_nlp'
validfiles = pd.read_csv('valid_file.csv')
filelist = validfiles['file_name']

#os.chdir('redata')
os.chdir(datafolder)
#filelist = os.listdir()
attrlist = ['Tic', 'Date','Type'] + LM_Selected + Harvard_Selected
entries = np.array(np.zeros((1,len(attrlist))))

writeind = 0
for fileind, onefile in enumerate(filelist):
    print('Processing file #%s, file name "%s"' % (str(fileind), onefile))
    alltxt = read_bulk(onefile)
    testlist = get_candidates(alltxt)
    docscore = find_scores(testlist)
    ids = np.array([onefile[:-4].split('-')])
    docentry = np.concatenate((ids, docscore), axis=1)
    entries = np.append(entries, docentry, axis=0)
    if fileind % 10 == 9:
        try:
            shutil.copy2('autosave.csv','tempread.csv')
        except:
            pass
        tblsave = pd.DataFrame(entries[1:,:], columns=attrlist)
        tblsave.to_csv('autosave.csv', sep=',',
                      encoding='utf-8', mode='w')
        print('Autosaved')
    if fileind % 30 == 29:
        tblsave.to_csv('batch%s.csv' % str(writeind), sep=',',
                      encoding='utf-8', mode='w')
        print('Saved 30 entries to file batch%s.csv' % writeind)
        tblsave = []
        writeind += 1
        entries = np.array(np.zeros((1,len(attrlist))))
        
writeind = 0
alltb = save_combiner()
os.chdir('..')
# tblout = pd.DataFrame(entries, columns=attrlist)
alltb.to_csv('NLPcombined.csv', sep=',', encoding='utf-8', mode='w')

print('The end is the beginning is the end')