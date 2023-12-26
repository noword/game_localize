import sys

sys.path.append('../../libs')
from trans import Translation
import easyocr
from pathlib import Path


trans = Translation()
reader = easyocr.Reader(['ja', 'en'])

for name in Path('old').glob('*.png'):
    pure_name = str(name.name)
    result = reader.readtext(str(name), detail=0)
    print(pure_name, ''.join(result))
    trans.append(
        {
            'ImageName': pure_name.replace('.png', '.tga'),
            'Japanese': ''.join(result),
            'Chinese': '',
            'Function': '',
        }
    )

trans.save('Ginsei Igo Next Generation Images export.xlsx', index='Japanese')
