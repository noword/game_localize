from pathlib import Path
import os

ENCODINGS = ('utf-8', 'utf-16le', 'utf-16be', 'shift-jis', 'euc_jp', 'cp932', 'gbk')
BUF_SIZE = 0x1000 * 0x1000 * 0x50


def get_text_bytes(text, encoding=None):
    if encoding:
        return [(text.encode(encoding), encoding)]

    texts = {}
    for encoding in ENCODINGS:
        try:
            t = text.encode(encoding)
        except UnicodeEncodeError:
            continue
        if t in texts:
            texts[t] += '/' + encoding
        else:
            texts[t] = encoding
    return list(texts.items())


def search(path, texts):
    result = []
    try:
        fp = open(path, 'rb')
    except FileNotFoundError:
        return result

    back_size = max([len(t[0]) for t in texts])
    buf = b''
    while len(result) < len(texts):
        _buf_pos = fp.tell()
        _buf = fp.read(BUF_SIZE)

        if len(_buf) == 0:
            break

        if len(buf) > 0:
            buf = buf[-back_size:] + _buf
            _buf_pos -= back_size
        else:
            buf = _buf

        for text, encoding in texts:
            pos = buf.find(text)
            if pos != -1:
                result.append((_buf_pos + pos, encoding))

    return result


def search_all(ext, texts):
    for path in Path('.').rglob(ext):
        if path.is_file():
            for offset, encoding in search(path, texts):
                print(f'Found! {offset:08x} {encoding:9s} {path}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('text', action='store', nargs=1)
    parser.add_argument('--encoding', action='store', nargs='?')
    parser.add_argument('--ignore_case', action='store_true', default=False)
    parser.add_argument("--hex", action="store_true", default=False)
    parser.add_argument('--ext', action='store', nargs='?')
    args = parser.parse_args()

    ext = args.ext
    if ext is None:
        ext = '*'
    elif not ext.startswith('*'):
        ext = '*' + ext

    texts = get_text_bytes(args.text[0])
    for t, encoding in texts:
        print(t.hex(), encoding)
    print()
    search_all(ext, texts)
