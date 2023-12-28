from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from pathlib import Path
import os
import math


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def rot_x(self, degrees):
        radians = math.radians(degrees)
        return self.x * math.cos(radians) + self.y * math.sin(radians)


class Rect(object):
    def __init__(self, x1, y1, x2, y2):
        minx, maxx = (x1, x2) if x1 < x2 else (x2, x1)
        miny, maxy = (y1, y2) if y1 < y2 else (y2, y1)
        self.min = Point(minx, miny)
        self.max = Point(maxx, maxy)

    def min_max_rot_x(self, degrees):
        first = True
        for x in [self.min.x, self.max.x]:
            for y in [self.min.y, self.max.y]:
                p = Point(x, y)
                rot_d = p.rot_x(degrees)
                if first:
                    min_d = rot_d
                    max_d = rot_d
                else:
                    min_d = min(min_d, rot_d)
                    max_d = max(max_d, rot_d)
                first = False
        return min_d, max_d

    width = property(lambda self: self.max.x - self.min.x)
    height = property(lambda self: self.max.y - self.min.y)


def gradient_color(minval, maxval, val, color_palette):
    """Computes intermediate RGB color of a value in the range of minval
    to maxval (inclusive) based on a color_palette representing the range.
    """
    max_index = len(color_palette) - 1
    delta = maxval - minval
    if delta == 0:
        delta = 1
    v = float(val - minval) / delta * max_index
    i1, i2 = int(v), min(int(v) + 1, max_index)
    (r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
    f = v - i1
    return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))


FONT_PATHS = (
    os.environ['USERPROFILE'] + '/AppData/Local/Microsoft/Windows/Fonts/',
    os.environ['WINDIR'] + '/Fonts/',
    './',
    './fonts/',
)

IMAGE_PATHS = ('./bg/',)


class Drawer:
    def __init__(self, font_paths=[], image_paths=[]):
        self.__font_paths = font_paths
        self.__font_paths.extend(FONT_PATHS)
        self.__image_paths = image_paths
        self.__image_paths.extend(IMAGE_PATHS)
        self.__font_cache = {}
        self.__image_cache = {}

    def __try_to_get_file(self, paths, name):
        for path in paths:
            n = path + name
            if os.path.exists(n):
                return n
        raise TypeError(f'{name} does not exist')

    def get_font(self, name, size):
        key = f'{name}_{size}'
        if key not in self.__font_cache:
            path = self.__try_to_get_file(self.__font_paths, name)
            self.__font_cache.__setitem__(key, ImageFont.truetype(path, size))
        return self.__font_cache[key]

    def __get_image_by_name(self, name):
        if name not in self.__image_cache:
            path = self.__try_to_get_file(self.__image_paths, name)
            self.__image_cache.__setitem__(name, Image.open(path))
        return self.__image_cache[name].copy()

    def __get_image_by_size(self, size):
        key = f'{size[0]}x{size[1]}'
        if key not in self.__image_cache:
            self.__image_cache[key] = Image.new('RGBA', size)
        return self.__image_cache[key].copy()

    def get_image(self, name_or_size):
        if isinstance(name_or_size, str):
            return self.__get_image_by_name(name_or_size)
        else:
            return self.__get_image_by_size(name_or_size)

    def get_text_image(
        self,
        size,  # 图片大小
        font,  # ImageFont 字体
        text,  # 文本
        halign='center',  # 横向对齐方式，合法值： left, right, center
        valign='center',  # 纵向对齐方式，合法值：top, bottom, center
        italic=False,  # 倾斜
        color='white',  # 文字颜色
        letter_space=1.0,  # 字符间距的比例，合法值 0 - 1
        blur=-1,  # 高斯模糊滤镜的参数，小于 0 无效，数值越大越模糊，建议从 2 开始调整
        stroke_width=0,  # 字体描边宽度
        stroke_fill=None,  # 描边颜色
        shear=None,  # 仿射变换参数，控制倾斜率，如设置了italic=True，则固定为0.2
    ):
        im = Image.new('RGBA', size)
        draw = ImageDraw.Draw(im)

        width, height = size
        (left, top, right, bottom) = draw.textbbox((0, 0), text, font=font)
        w = (right - left) * letter_space
        h = bottom - top
        if halign == 'left':
            x = 0 + h // 2
        elif halign == 'right':
            x = width - w - h // 2
        else:  # center
            x = (width - w) // 2

        if valign == 'top':
            y = 0
        elif valign == 'bottom':
            y = height - h
        else:  # center
            y = (height - h) // 2

        if letter_space == 1:
            draw.text(
                (x, y), text, font=font, fill=color, anchor='lt', stroke_width=stroke_width, stroke_fill=stroke_fill
            )
        else:
            for t in text:
                w = draw.textlength(t, font=font)
                draw.text(
                    (x, y), t, font=font, fill=color, anchor='lt', stroke_width=stroke_width, stroke_fill=stroke_fill
                )
                x += w * letter_space

        if blur > 0:
            im = im.filter(ImageFilter.GaussianBlur(blur))

        if italic:
            shear = 0.2
        if shear is not None:
            im = im.transform(im.size, Image.AFFINE, (1, shear, 0, 0, 1, 0), resample=Image.Resampling.BICUBIC)

        return im

    def get_degrees_gradient_image(
        self,
        size,  # 图片大小
        color_palette,  # 颜色枚举
        degrees=0,  # 渐变角度
    ):
        p = []
        for c in color_palette:
            if isinstance(c, str):
                c = ImageColor.getrgb(c)
            p.append(c)
        color_palette = p

        im = Image.new('RGBA', size)
        width, height = size
        rect = Rect(0, 0, width - 1, height - 1)
        minval, maxval = 1, len(color_palette)
        delta = maxval - minval
        min_d, max_d = rect.min_max_rot_x(degrees)
        range_d = max_d - min_d
        for x in range(rect.min.x, rect.max.x + 1):
            for y in range(rect.min.y, rect.max.y + 1):
                p = Point(x, y)
                f = (p.rot_x(degrees) - min_d) / range_d
                val = minval + f * delta
                color = gradient_color(minval, maxval, val, color_palette)
                im.putpixel((x, y), color)
        return im

    def do(self, func, text, name):
        getattr(self, func)(text, name)
