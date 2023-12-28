import unittest
from t2g import T2GF
from pathlib import Path
from io import BytesIO


class Test(unittest.TestCase):
    def test(self):
        for name in Path('backup').glob('*.t2g'):
            t2g = T2GF(open(name, 'rb'))
            self.assertEqual(open(name, 'rb').read(), t2g.getvalue())


unittest.main()
