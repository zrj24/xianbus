import os
import datetime
from natsort import os_sorted

def filelist2md():
    datapath = r'E:\xianbus\241129\diagram'
    filelist = os.listdir(datapath)
    filelist = [file for file in filelist if file != 'index.md']
    filelist = os_sorted(filelist)
    filenames_without_ext = [os.path.splitext(filename)[0] for filename in filelist]
    # print(filenames_without_ext)
    with open(r'E:\xianbus\241129\diagram\index.md', 'w', encoding='utf-8') as f:
        f.write('# 运行图 241129\n')
        for i in range(0, len(filelist)):
            f.write(f'### [{filenames_without_ext[i]}]({filelist[i]})\n')

if __name__ == '__main__':
    filelist2md()