import glob, os
dir = r'../data_raw/reports_pdf/FTSE/RRS'
fileMask = r'*.pdf'

s = set()
for pathAndFilename in glob.iglob(os.path.join(dir, fileMask)):
    print(pathAndFilename)
    name, ext = os.path.splitext(os.path.basename(pathAndFilename))
    newname = name.replace('PRS_', 'RRS_')
    newPathAndFileName = os.path.join(dir, newname + ext)
    os.rename(pathAndFilename, newPathAndFileName)
