from t2g import T2GF
from pathlib import Path
import os

if __name__ == '__main__':
    for t2g_name in Path('backup').glob('*.t2g'):
        print(t2g_name)
        t2g = T2GF(open(t2g_name, 'rb'))
        need_update = False
        for name in t2g.keys():
            if os.path.exists(name):
                print(' ', name)
                need_update = True
                t2g.replace(name, open(name, 'rb').read())

        if need_update:
            t2g.save(open(t2g_name.name, 'wb'))
