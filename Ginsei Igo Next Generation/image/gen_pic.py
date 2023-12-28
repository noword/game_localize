import sys

sys.path.append('../../libs')
from translation import Translation
from drawer import Drawer
from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
import os
import math


def check_size():
    for name in Path('.').glob('*.tga'):
        im = Image.open(name)
        _im = Image.open(f'old/{name.stem}.png')
        if im.size != _im.size:
            print(name, im.size, _im.size)
            raise TypeError


def gen_gxt():
    for name in Path('.').glob('*.tga'):
        print(name)
        os.system(f'psp2gxt -i {name} -o {name.stem}.gxt')


class MyDrawer(Drawer):
    def do_B1_gbtn(self, text, name):
        image = self.get_image('B1.png')
        size = 192, 40
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, color='#333333', stroke_width=1, blur=2)
        image.paste(im, mask=im)
        im = self.get_text_image(size, font, text)
        image.paste(im, mask=im)
        image.save(name)

    def do_B2_bn(self, text, name):
        image = self.get_image('B2.png')
        font = self.get_font('wqy-microhei.ttc', 30)
        size = 286, 54
        im = self.get_text_image(size, font, text, color='#363636', stroke_width=1, blur=2)
        image.paste(im, mask=im)
        im = self.get_text_image(size, font, text)
        image.paste(im, mask=im)
        image.save(name)

    def do_header(self, text, name):
        texts = text.split('|')
        image = self.get_image('header.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 40)

        size = 310, 50
        pos = 58, 16
        im = self.get_text_image(size, font, texts[0], color='#000000', stroke_width=4, italic=True, blur=2)
        image.paste(im, pos, mask=im)
        im = self.get_text_image(size, font, texts[0], italic=True)
        image.paste(im, pos, mask=im)

        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        size = 460, 40
        pos = 450, 10
        im = self.get_text_image(size, font, texts[1], color='#000000', halign='right', stroke_width=3, blur=2)
        image.paste(im, pos, mask=im)
        im = self.get_text_image(size, font, texts[1], halign='right')
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_note(self, text, name):
        image = self.get_image('CM_note.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image((936, 40), font, text)
        image.paste(im, (4, 5), mask=im)
        image.save(name)

    def do_mtex(self, text, name):
        size = 322, 42
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, halign='left', stroke_fill='#242424', stroke_width=4)
        image.paste(im, mask=im)
        image.save(name)

    def do_ptex(self, text, name):
        size = 150, 42
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, stroke_fill='#242424', stroke_width=4)
        image.paste(im, mask=im)
        image.save(name)

    def do_ptex_d(self, text, name):
        size = 150, 42
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, color='#aaaaaa', stroke_fill='#242424', stroke_width=4)
        image.paste(im, mask=im)
        image.save(name)

    def __do_btn2P_Com(self, image, text, name):
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        size = 290, 40
        pos = 0, 42
        im = self.get_text_image(size, font, text, stroke_fill='#363636', stroke_width=3)
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_btn2P(self, text, name):
        bg = self.get_image('C2_btn2P.png')
        self.__do_btn2P_Com(bg, text, name)

    def do_btnCom(self, text, name):
        bg = self.get_image('C2_btnCom.png')
        self.__do_btn2P_Com(bg, text, name)

    def do_btnL(self, text, name):
        texts = text.split('|')
        image = self.get_image('E1_btn.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 32)
        size = 148, 40
        pos = 0, 14
        im = self.get_text_image(size, font, texts[0], stroke_fill='#363636', stroke_width=4)
        image.paste(im, pos, mask=im)

        pos = 0, 55
        im = self.get_text_image(size, font, texts[1], color='#ffbebe', stroke_fill='#363636', stroke_width=4)
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_ltex(self, text, name):
        size = 103, 50
        image = self.get_image(size)
        font = self.get_font('演示春风楷.ttf', 45)
        im = self.get_text_image(size, font, text, stroke_fill='#242424', stroke_width=4)
        image.paste(im, mask=im)
        image.save(name)

    def do_dbtn(self, text, name):
        image = self.get_image('CM_dbtn.png')
        font = self.get_font('文鼎PL简中楷.ttf', 34)
        size = 236, 62
        im = self.get_text_image(size, font, text, stroke_fill='#000000', stroke_width=3)
        image.paste(im, mask=im)
        image.save(name)

    def do_texTitle(self, text, name):
        size = 204, 42
        image = self.get_image(size)
        font = self.get_font('文鼎PL简报宋.ttf', 32)
        im = self.get_text_image(size, font, text, color='#000000', stroke_width=4, italic=True, blur=2)
        image.paste(im, mask=im)

        im = self.get_text_image(size, font, text, color='#aaaaaa', stroke_width=1, italic=True)
        image.paste(im, mask=im)

        alpha = self.get_text_image(size, font, text, italic=True).convert('L')
        im = self.get_degrees_gradient_image(size, ('#ffffff', '#777777'), 90)
        im.putalpha(alpha)
        image.paste(im, mask=im)
        image.save(name)

    def __do_gbtn(self, image, text, name):
        size = 106, 40
        pos = 70, 0
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, color='#082030', stroke_width=1, blur=2)
        image.paste(im, pos, mask=im)
        im = self.get_text_image(size, font, text)
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_gbtnCircle(self, text, name):
        self.__do_gbtn(self.get_image('CM_gbtnA_Circle.png'), text, name)

    def do_gbtnCross(self, text, name):
        self.__do_gbtn(self.get_image('CM_gbtnA_Cross.png'), text, name)

    def do_gbtnStart(self, text, name):
        self.__do_gbtn(self.get_image('CM_gbtnA_Start.png'), text, name)

    def do_CM_gbtnA_L(self, text, name):
        texts = text.split('|')
        image = self.get_image('CM_gbtnA_L.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        size = 110, 36
        pos0 = 0, 55
        pos1 = 0, 82
        im = self.get_text_image(size, font, texts[0], color='#082030', stroke_width=1, blur=1)
        image.paste(im, pos0, mask=im)
        im = self.get_text_image(size, font, texts[0])
        image.paste(im, pos0, mask=im)

        im = self.get_text_image(size, font, texts[1], color='#082030', stroke_width=1, blur=1)
        image.paste(im, pos1, mask=im)
        im = self.get_text_image(size, font, texts[1])
        image.paste(im, pos1, mask=im)
        image.save(name)

    def do_CM_gbtnA_R(self, text, name):
        texts = text.split('|')
        image = self.get_image('CM_gbtnA_R.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        size = 110, 36
        pos0 = 0, 55
        pos1 = 0, 82
        im = self.get_text_image(size, font, texts[0], color='#082030', stroke_width=1, blur=1)
        image.paste(im, pos0, mask=im)
        im = self.get_text_image(size, font, texts[0])
        image.paste(im, pos0, mask=im)
        im = self.get_text_image(size, font, texts[1], color='#082030', stroke_width=1, blur=1)
        image.paste(im, pos1, mask=im)
        im = self.get_text_image(size, font, texts[1])
        image.paste(im, pos1, mask=im)
        image.save(name)

    def do_GM_win(self, text, name):
        size = (460, 60)
        image = self.get_image('GM_win.png')
        font = self.get_font('wqy-microhei.ttc', 30)
        im = self.get_text_image(size, font, text, stroke_width=2)
        image.paste(im, mask=im)
        alpha = self.get_text_image(size, font, text).convert('L')
        im = self.get_degrees_gradient_image(size, ('#a0a0a0', '#080808'), 90)
        im.putalpha(alpha)
        image.paste(im, mask=im)
        image.save(name)

    def do_texSeff(self, text, name):
        size = (176, 168)
        image = self.get_image(size)
        font = self.get_font('文鼎PL简中楷.ttf', 120)
        im = self.get_text_image((190, 168), font, text, color='#e5e5e5', italic=True, stroke_width=20, blur=10)
        image.paste(im, (10, 0), mask=im)

        pos = (20, 0)
        im = self.get_text_image(size, font, text, italic=True)
        image.paste(im, pos, mask=im)

        image.save(name)

    def __do_GK_gtn(self, image, text, name):
        size = (100, 32)
        pos = (0, 58)
        font = self.get_font('SourceHanSansCN-Bold.otf', 22)
        im = self.get_text_image(size, font, text, color='#104050', stroke_width=1, blur=2)
        image.paste(im, pos, mask=im)
        im = self.get_text_image(size, font, text)
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_GK_gbtn1back(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtn1back.png'), text, name)

    def do_GK_gbtn1go(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtn1go.png'), text, name)

    def do_GK_gbtnEndgo(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnEndgo.png'), text, name)

    def do_GK_gbtnFirst(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnFirst.png'), text, name)

    def do_GK_gbtnCircle(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnCircle.png'), text, name)

    def do_GK_gbtnCross(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnCross.png'), text, name)

    def do_GK_gbtnTriangle(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnTriangle.png'), text, name)

    def do_GK_gbtnSquare(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnSquare.png'), text, name)

    def do_GK_gbtnHint(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnHint.png'), text, name)

    def do_GK_gbtnEndcon(self, text, name):
        self.__do_GK_gtn(self.get_image('GK_gbtnEndcon.png'), text, name)

    def do_GK_0texS_01(self, text, name):
        size = 524, 172
        letter_space = 1
        image = self.get_image(size)
        font = self.get_font('文鼎PL简中楷.ttf', 120)

        im = self.get_text_image((700, 172), font, text, color='#333333', stroke_width=3, letter_space=letter_space)
        im = im.resize((700, 86))
        im = im.transform(im.size, Image.AFFINE, (1, 0.8, 0, 0, 1, 0), resample=Image.Resampling.BICUBIC)
        image.paste(im, (-60, 60), mask=im)

        im = self.get_text_image(
            size, font, text, color='#646464', italic=True, stroke_width=5, letter_space=letter_space
        )
        image.paste(im, mask=im)

        alpha = self.get_text_image(size, font, text, italic=True, letter_space=letter_space, blur=0.5).convert('L')
        im = self.get_degrees_gradient_image(size, ('white', '#999999'), 90)
        im.putalpha(alpha)
        image.paste(im, mask=im)

        image.save(name)

    def do_GK_winSetting(self, text, name):
        texts = text.split('|')
        image = self.get_image('GK_winSetting.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 18)
        im = self.get_text_image((58, 24), font, texts[0], italic=True)
        image.paste(im, mask=im)

        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image((100, 30), font, texts[1], color='#040404', stroke_width=2, stroke_fill='#a0a0a0')
        image.paste(im, (0, 28), mask=im)
        im = self.get_text_image((100, 30), font, texts[2], color='#040404', stroke_width=2, stroke_fill='#a0a0a0')
        image.paste(im, (0, 55), mask=im)
        image.save(name)

    def do_GK_winMs(self, text, name):
        image = self.get_image('GK_winMs.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 18)
        im = self.get_text_image((90, 24), font, text, italic=True)
        image.paste(im, mask=im)
        image.save(name)

    def do_GK_winKifu(self, text, name):
        image = self.get_image('GK_winKifu.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 18)
        im = self.get_text_image((90, 28), font, text, italic=True)
        image.paste(im, mask=im)
        image.save(name)

    def __do_GK_winPlayer(self, image, text, name):
        texts = text.split('|')
        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image(
            (100, 30), font, texts[0], color='#040404', stroke_width=2, stroke_fill='#a0a0a0', halign='right'
        )
        image.paste(im, (0, 41), mask=im)
        im = self.get_text_image(
            (100, 30), font, texts[1], color='#040404', stroke_width=2, stroke_fill='#a0a0a0', halign='right'
        )
        image.paste(im, (0, 68), mask=im)
        image.save(name)

    def do_GK_winPlayerB(self, text, name):
        self.__do_GK_winPlayer(self.get_image('GK_winPlayerB.png'), text, name)

    def do_GK_winPlayerW(self, text, name):
        self.__do_GK_winPlayer(self.get_image('GK_winPlayerW.png'), text, name)

    def do_GK_msPlayer(self, text, name):
        size = 388, 48
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, color='#303030', stroke_width=5, blur=5)
        image.paste(im, mask=im)
        im = self.get_text_image(size, font, text)
        image.paste(im, mask=im)
        image.save(name)

    def do_D1_winB(self, text, name):
        texts = text.split('|')
        size = 120, 24
        x = 5
        image = self.get_image('D1_winB.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image(size, font, texts[0], italic=True, halign='left')
        image.paste(im, (x, 0), mask=im)
        im = self.get_text_image(size, font, texts[1], italic=True, halign='left')
        image.paste(im, (x, 95), mask=im)
        im = self.get_text_image(size, font, texts[2], italic=True, halign='left')
        image.paste(im, (x, 220), mask=im)
        im = self.get_text_image(size, font, texts[3], italic=True, halign='left')
        image.paste(im, (560, 0), mask=im)
        im = self.get_text_image(size, font, texts[4], italic=True, halign='left')
        image.paste(im, (690, 0), mask=im)
        im = self.get_text_image(size, font, texts[5], italic=True, halign='left')
        image.paste(im, (856, 0), mask=im)

        size = 150, 32
        x = 22
        font = self.get_font('wqy-microhei.ttc', 25)
        im = self.get_text_image(size, font, texts[6], halign='right', stroke_width=3, stroke_fill='#363636')
        image.paste(im, (x, 130), mask=im)
        im = self.get_text_image(size, font, texts[7], halign='right', stroke_width=3, stroke_fill='#363636')
        image.paste(im, (x, 170), mask=im)
        im = self.get_text_image(size, font, texts[8], halign='right', stroke_width=3, stroke_fill='#363636')
        image.paste(im, (x, 255), mask=im)
        im = self.get_text_image(size, font, texts[9], halign='right', stroke_width=3, stroke_fill='#363636')
        image.paste(im, (x, 295), mask=im)
        image.save(name)

    def do_F1_win2(self, text, name):
        texts = text.split('|')
        image = self.get_image('F1_win2.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image((180, 24), font, texts[0], italic=True, halign='left')
        image.paste(im, (3, 0), mask=im)

        font = self.get_font('wqy-microhei.ttc', 25)
        size = 70, 40
        start_x, start_y = 12, 42
        w = 210
        h = 50
        for y in range(4):
            for x in range(3):
                im = self.get_text_image(
                    size, font, texts[y * 3 + x + 1], halign='right', stroke_width=3, stroke_fill='#363636'
                )
                image.paste(im, (start_x + x * w, start_y + y * h), mask=im)

        image.save(name)

    def do_F1_win1(self, text, name):
        texts = text.split('|')
        image = self.get_image('F1_win1.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image((180, 24), font, texts[0], italic=True, halign='left')
        image.paste(im, (8, 0), mask=im)

        font = self.get_font('wqy-microhei.ttc', 25)
        size = 170, 40
        start_x, start_y = 15, 40
        h = 40
        for i in range(5):
            im = self.get_text_image(size, font, texts[i + 1], halign='right', stroke_width=3, stroke_fill='#363636')
            image.paste(im, (start_x, start_y + i * h), mask=im)

        image.save(name)

    def do_GK_0texD_01(self, text, name):
        size = 524, 172
        image = self.get_image(size)
        font = self.get_font('文鼎PL简中楷.ttf', 120)
        im = self.get_text_image(size, font, text, color='#008000', italic=True, stroke_width=10, blur=5)
        image.paste(im, mask=im)

        im = self.get_text_image(size, font, text, color='#24a800', italic=True, stroke_width=3)
        image.paste(im, mask=im)

        alpha = self.get_text_image(size, font, text, italic=True, blur=1).convert('L')
        im = self.get_degrees_gradient_image(size, ('#00ff00', 'white', '#00ff00'), degrees=90)
        im.putalpha(alpha)
        image.paste(im, mask=im)

        image.save(name)

    def do_GK_0texL_01(self, text, name):
        size = 524, 172
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 100)

        im = self.get_text_image(size, font, text, color='#158080', italic=True, stroke_width=6, blur=2)
        image.paste(im, mask=im)

        im = self.get_text_image(size, font, text, italic=True, stroke_width=3)
        image.paste(im, mask=im)

        alpha = self.get_text_image(size, font, text, italic=True, blur=1).convert('L')
        im = self.get_degrees_gradient_image(size, ('#47a8c4', '#236769'), degrees=90)
        im.putalpha(alpha)
        image.paste(im, mask=im)

        image.save(name)

    def do_GK_0texV_01(self, text, name):
        size = 524, 172
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 100)

        im = self.get_text_image(size, font, text, color='#403000', italic=True, stroke_width=10, blur=10)
        image.paste(im, (8, 8), mask=im)

        im = self.get_text_image(size, font, text, italic=True, stroke_width=3)
        image.paste(im, mask=im)

        alpha = self.get_text_image(size, font, text, italic=True, blur=1).convert('L')
        im = self.get_degrees_gradient_image(size, ('#ff3000', '#ffcc00'), degrees=90)
        im.putalpha(alpha)
        image.paste(im, mask=im)
        image.save(name)

    def do_GK_0texV_02(self, text, name):
        size = 524, 172
        image = self.get_image(size)
        font = self.get_font('SourceHanSansCN-Bold.otf', 100)

        im = self.get_text_image(size, font, text, color='#b0b0b0', italic=True, stroke_width=20, blur=4)
        image.paste(im, mask=im)

        im = self.get_text_image(size, font, text, italic=True, color='#d8c87c')
        image.paste(im, mask=im)

        font = self.get_font('SourceHanSansCN-Bold.otf', 100)
        image.save(name)

    def do_GK_msOperat(self, text, name):
        pos = (50, 0)
        image = self.get_image('GK_msOperat.png')
        size = image.size
        font = self.get_font('SourceHanSansCN-Bold.otf', 25)
        im = self.get_text_image(size, font, text, color='#303030', halign='left', stroke_width=5, blur=5)
        image.paste(im, pos, mask=im)
        im = self.get_text_image(size, font, text, halign='left')
        image.paste(im, pos, mask=im)
        image.save(name)

    def do_B1_gamelogo(self, text, name):
        texts = text.split('|')
        image = self.get_image('B1_gamelogo.png')
        font = self.get_font('SourceHanSansCN-Bold.otf', 30)
        im = self.get_text_image(
            (100, 44), font, texts[0], color='#cccccc', stroke_width=3, stroke_fill='#333333', halign='left'
        )
        image.paste(im, (60, 310), mask=im)

        font = self.get_font('SourceHanSansCN-Bold.otf', 20)
        im = self.get_text_image((884, 44), font, texts[1], color='#cccccc', stroke_width=3, stroke_fill='#333333')
        image.paste(im, (0, 315), mask=im)
        image.save(name)


if __name__ == '__main__':
    drawer = MyDrawer()
    trans = Translation('Ginsei Igo Next Generation Images.xlsx')
    for name, t in trans.get_trans(index='ImageName').items():
        if len(t['Function']) > 0:
            drawer.do(t['Function'], t['Chinese'], name)
    check_size()
    gen_gxt()
