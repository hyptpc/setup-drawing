from contextlib import contextmanager
import datetime
import os

import config as cfg

#______________________________________________________________________________
@contextmanager
def saved_state():
  print("gsave")
  try:
    yield
  finally:
    print("grestore")

#______________________________________________________________________________
@contextmanager
def transform(x=0, y=0, angle=0):
  print("gsave")
  if x != 0 or y != 0:
    translate_xy(x, y)
  if angle != 0:
    rotate(angle)
  try:
    yield
  finally:
    print("grestore")

#______________________________________________________________________________
def closepath():
  print('closepath')

#______________________________________________________________________________
def comment(arg):
  print(f'% {arg}')

#______________________________________________________________________________
def define_command():
  print('/stringtop { gsave newpath 0 0 moveto false charpath flattenpath ' +
        'pathbbox 4 1 roll pop pop pop grestore } def')
  print('/stringbottom { gsave newpath 0 0 moveto false charpath ' +
        'flattenpath pathbbox pop pop exch pop grestore } def')

#______________________________________________________________________________
def define_length():
  print('/mm { ' + f'{0.1*cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')
  print('/cm { ' + f'{cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')
  print('/m { ' + f'{100*cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')

#______________________________________________________________________________
def grestore():
  print('grestore')

#______________________________________________________________________________
def gsave():
  print('gsave')

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

#______________________________________________________________________________
def initialize(experiment):
  header(experiment)
  set_font()
  define_length()
  define_command()
  print('%%EndProlog')
  translate_xy(cfg.paper_width / cfg.scale_factor / 2,
               cfg.paper_height / cfg.scale_factor / 2)
  rotate(cfg.global_rotation_angle)
  set_line_style(cfg.line_width, cfg.color_black)

#______________________________________________________________________________
def line_to_xy(x, y):
  print(f'{x} mm {y} mm lineto')

#______________________________________________________________________________
def line_to_rtheta(r, theta):
  print(f'{r} {theta} cos mul mm {r} {theta} sin mul mm lineto')

#______________________________________________________________________________
def move_to_xy(x, y):
  print(f'{x} mm {y} mm moveto')

#______________________________________________________________________________
def move_to_rtheta(r, theta):
  print(f'{r} {theta} cos mul mm {r} {theta} sin mul mm moveto')

#______________________________________________________________________________
def newpath():
  print('newpath')

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
def set_line_style(width, color):
  if color < 0 or color is None:
    color = 1.0 # black
  print(f'{width} mm setlinewidth {color} setgray')

#______________________________________________________________________________
def stroke():
  print('stroke')

#______________________________________________________________________________
def draw_text(text, angle, align):
  '''
  Align:
    1: left align
    0: center align, y higher
   10: center align, y lower
   -1: right align
  '''
  with saved_state():
    move_to_xy(0, 0)
    rotate(-cfg.global_rotation_angle + angle)
    if align == 1:
      print(f'({text}) (A) stringtop 2.0 div neg 0. exch rmoveto show')
    elif align == -1:
      print(f'({text}) dup stringwidth pop neg' +
            f'(A) stringtop 2.0 div neg rmoveto show')
    elif align == 0:
      print(f'({text}) dup stringwidth pop 2.0 div neg' +
            f'(A) stringbottom neg rmoveto show')
    elif align == 10:
      print(f'({text}) dup stringwidth pop 2.0 div neg' +
            f'(A) stringtop neg rmoveto show')

#______________________________________________________________________________
def translate_xy(x, y):
  print(f'{x} mm {y} mm translate')

#______________________________________________________________________________
def translate_rtheta(r, theta):
  print(f'{r} {theta} cos mul mm ' +
        f'{r} {theta} sin mul mm translate')
