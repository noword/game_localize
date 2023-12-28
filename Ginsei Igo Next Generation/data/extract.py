from t2g import T2GF
from pathlib import Path
import os


for name in Path('backup').glob('*.t2g'):
    print(name)
    t2g = T2GF(open(name, 'rb'))
    out = 'data/' + name.stem
    try:
        os.mkdir(out)
    except:
        pass
    os.chdir(out)
    t2g.dump_all()
    os.chdir('../..')
