import glob, os
dir = r'../data_raw/prices/*'
fileMask = r'*_NASDAQ.csv'

s = set()
for pathAndFilename in glob.iglob(os.path.join(dir, fileMask)):
    name, ext = os.path.splitext(os.path.basename(pathAndFilename))
    newname = name.replace('_NASDAQ', '_DJIA')
    newPathAndFileName = os.path.join(os.path.dirname(pathAndFilename), newname + ext)
    print(pathAndFilename)
    print(newPathAndFileName)

    os.rename(pathAndFilename, newPathAndFileName)
