import os
import pandas as pd
import shutil

dataset = {}
dataset['train'] = []
dataset['test'] = []
dataset['testcam'] = []

classname = []
for _, clsdirs, _ in os.walk('./datasets/nccfaces/train/'):
    for index, clsdir in enumerate(clsdirs):
        classname.append(clsdir)


for mset in ['train', 'test', 'testcam']:
    for _, clsdirs, _ in os.walk('./datasets/nccfaces/%s'%mset):
        for i, clsdir in enumerate(clsdirs):
            dirpath = './datasets/nccfaces/%s/%s/'%(mset,clsdir)
            for file in os.listdir(dirpath):
                if file == '.' or file == '..':
                    continue

                imgname = '%s_%s'%(clsdir, file)
                dest = shutil.copyfile(os.path.join(dirpath, file), './datasets/nccfaces/%s/%s'%(mset,imgname))
                if mset == 'train':
                    #print("clsidx %d, %s" % (i, clsdir))
                    dataset[mset].append({
                        'image':imgname,
                        'label':i
                    })
                else:
                    dataset[mset].append({
                        'image':imgname,
                        'label':classname.index(clsdir)
                    })
                    #print("clsidx %d, %s" % (classname.index(clsdir), clsdir))

    df = pd.DataFrame(dataset[mset])
    df.to_csv('./datasets/%s.csv'%mset, index=False)
