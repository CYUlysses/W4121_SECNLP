# from senti_scoring import *
import shutil

datafolder = 'data_nlp'
validfiles = pd.read_csv('valid_file.csv')
filelist = validfiles['file_name']

#os.chdir('redata')
os.chdir(datafolder)
#filelist = os.listdir()
attrlist = ['Tic', 'Date','Type'] + LM_Selected + Harvard_Selected
entries = np.array(np.zeros((1,len(attrlist))))

for fileind, onefile in enumerate(filelist):
    print('Processing file #%s, file name "%s"' % (str(fileind), onefile))
    alltxt = read_bulk(onefile)
    testlist = get_candidates(alltxt)
    docscore = find_scores(testlist)
    ids = np.array([onefile[:-4].split('-')])
    docentry = np.concatenate((ids, docscore), axis=1)
    entries = np.append(entries, docentry, axis=0)
    if fileind % 10 == 5:
        shutil.copy2('tempsave.csv','tempreadable.csv')
        tblsave = pd.DataFrame(entries[1:,:], columns=attrlist)
        tblsave.to_csv('tempsave.csv', sep=',',
                      encoding='utf-8', mode='w')
os.chdir('..')
tblout = pd.DataFrame(entries, columns=attrlist)
tblout.to_csv('NLPed.csv', sep=',', encoding='utf-8', mode='w')

print('The end is the beginning is the end')