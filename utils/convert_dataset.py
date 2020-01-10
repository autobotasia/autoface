import os
import pandas as pd
import shutil 

dataset = {}
dataset['train'] = []
dataset['test'] = []
dataset['testcam'] = []
for mset in ['train', 'test', 'testcam']:
    for _, clsdirs, _ in os.walk('./datasets/nccfaces/%s'%mset):
        for index, clsdir in enumerate(clsdirs):
            dirpath = './datasets/nccfaces/%s/%s/'%(mset,clsdir)
            for file in os.listdir(dirpath):
                if file == '.' or file == '..':
                    continue

                imgname = '%s_%s'%(clsdir, file)
                dest = shutil.copyfile(os.path.join(dirpath, file), './datasets/%s/%s'%(mset,imgname)) 
                dataset[mset].append({
                    'image':imgname,
                    'label':index
                })
                        
    df = pd.DataFrame(dataset[mset])
    df.to_csv('./datasets/%s.csv'%mset, index=False)