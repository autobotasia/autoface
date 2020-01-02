import os
import pandas as pd
import shutil 

trainset = []
testset = []
for mset in ['train', 'test']:
    for _, clsdirs, _ in os.walk('../datasets/nccfaces/%s'%mset):
        for index, clsdir in enumerate(clsdirs):
            dirpath = '../datasets/nccfaces/%s/%s/'%(mset,clsdir)
            for file in os.listdir(dirpath):
                if '.png' not in file:
                    continue

                imgname = '%s_%s'%(clsdir, file)
                dest = shutil.copyfile(os.path.join(dirpath, file), '../datasets/%s/%s'%(mset,imgname)) 
                if mset == 'train':
                    trainset.append({
                        'image':imgname,
                        'label':index
                    })
                else:
                    testset.append({
                        'image':imgname,
                        'label':index
                    })        
df = pd.DataFrame(trainset)
df.to_csv('../datasets/train.csv', index=False)