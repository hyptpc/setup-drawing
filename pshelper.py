import datetime
import os

import config as cfg

#______________________________________________________________________________
def gsave():
  print('gsave')

#______________________________________________________________________________
def grestore():
  print('grestore')

#______________________________________________________________________________
def header(experiment):
  xmax = int(cfg.paper_width / 10 * cfg.cm_to_point)
  ymax = int(cfg.paper_height / 10 * cfg.cm_to_point)
  print('%!PS-Adobe-3.0 EPSF-3.0')
  print(f'%%Creator: {os.getlogin()}')
  print(f'%%CreationTime: {datetime.datetime.now()}')
  print(f'%%Description: J-PARC E{experiment} experiment setup ' +
        'in K1.8BR beam line')
  print('%%Pages: 1')
  print(f'%%BoundingBox: 0 0 {xmax} {ymax}')
  print('%%EndComments')
  print('%%Page: 1 1')
  set_font()

#______________________________________________________________________________
def rotate(degree):
  print(f'{degree} rotate')

#______________________________________________________________________________
def scale(scale_x, scale_y):
  print(f'{scale_x} {scale_y} scale')

#______________________________________________________________________________
def set_color(color):
  '''
  color values:
    color >= 0: grayscale
    color <  0: rgb color

  rgb color:
    color = - (R*1000000 + G*1000 + B)
    000 <= R,G,B <= 255
  '''
  if color is None:
    return
  if color >= 0:
    print(f'{color} setgray')
  else:
    color = int(abs(color))
    ir = int(color / 1000000)
    ig = int((color % 1000000) / 1000)
    ib = int(color) % 1000
    r = ir / 255.
    g = ig / 255.
    b = ib / 255.
    print(f'{r} {g} {b} setrgbcolor')

#______________________________________________________________________________
def set_font(font=cfg.font, font_size=cfg.font_size):
  print(f'{font} findfont {font_size} scalefont setfont')

#______________________________________________________________________________
# def set_line_style(width, color):
#   if color < 0

#______________________________________________________________________________
def translate_xy(x, y):
  print(f'{x} mm {y} mm translate')

#______________________________________________________________________________
def translate_rtheta(r, theta):
  print(f'{r} {theta} cos mul mm ' +
        f'{r} {theta} sin mul mm translate')
