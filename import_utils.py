import glob
import os.path
from os import path
def get_csv_from_dir(directory, filename=''):
    if filename == '':
        file_list = glob.glob(directory+'/*.csv')
        return file_list
    else:
        if path.exists(directory+'/'+filename+'.csv'):
            return [directory+'/'+filename+'.csv']
    