from contextlib import contextmanager
import datetime
import math
import os

from . import config as cfg

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
def arc(r, theta1, theta2):
  print(f'0 0 {r} mm {theta1} {theta2} arc')

#______________________________________________________________________________
def arc_xy(x, y, r, theta1, theta2):
  print(f'{x} mm {y} mm {r} mm {theta1} {theta2} arc')

#______________________________________________________________________________
def arcn(r, theta1, theta2):
  print(f'0 0 {r} mm {theta1} {theta2} arcn')

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
  if not cfg.rgb_color:
    print('/setrgbcolor { /b exch def /g exch def /r exch def ' +
          'r 0.30 mul g 0.59 mul add b 0.11 mul add setgray } bind def')

#______________________________________________________________________________
def define_length():
  print('/mm { ' + f'{0.1*cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')
  print('/cm { ' + f'{cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')
  print('/m { ' + f'{100*cfg.cm_to_point*cfg.scale_factor}' +
        ' mul } def')

#______________________________________________________________________________
def draw_box(x, z, color):
  with transform():
    path_box(0, 0, x, z)
    fill(color)
    stroke()

#______________________________________________________________________________
def draw_circle(r, color):
  with transform():
    path_circle(r)
    fill(color)
    stroke()

#______________________________________________________________________________
def draw_sector(r_inner, r_outer, theta1, theta2, color):
  with transform():
    path_sector(r_inner, r_outer, theta1, theta2)
    fill(color)
    stroke()

#______________________________________________________________________________
def draw_polygon(x, y, color):
  with transform():
    path_polygon(0, 0, x, y)
    fill(color)
    stroke()

#______________________________________________________________________________
def draw_tag(tag, angle, dx, dy, tag_type):
  tag_line_len = 1200
  if tag == 'BLC1b': tag_line_len = 850
  tag_line_angle = 10
  if not cfg.text_tag:
    return
  with transform():
    if tag_type < 0 or tag_type == 200:
      translate_xy(-dx, dy)
    else:
      translate_xy(dx, dy)
    if abs(tag_type) % 100 == 0:
      move_to_xy(0, 0)
      if tag_type == 100:
        draw_text(tag, angle, 10)
      elif tag_type == 200:
        draw_text(tag, angle, -1)
      else:
        draw_text(tag, angle, 1)
    else:
      tilt_angle = int((abs(tag_type) % 100) / 2) * tag_line_angle
      if abs(tag_type) % 2 == 1:
        tilt_angle *= -1
      align = 1
      if tag_type < 0:
        tilt_angle = 180 - tilt_angle
        align = -1
      if int(abs(tag_type) / 100) == 1:
        if math.sin(math.radians(tilt_angle)) >= 0:
          align = 0
        else:
          align = 10
      elif int(abs(tag_type) / 100) == 2:
        align *= -1
      with transform():
        with transform():
          set_line_style(width=cfg.line_width*4, color=cfg.color_white)
          move_to_xy(0, 0)
          line_to_rtheta(tag_line_len, tilt_angle)
          stroke()
        move_to_xy(0, 0)
        line_to_rtheta(tag_line_len, tilt_angle)
        stroke()
        translate_rtheta(tag_line_len*1.2, tilt_angle)
        draw_text(tag, angle, align)

#______________________________________________________________________________
def draw_text(text, angle, align):
  '''
  Align:
    1: left align
    0: center align, y higher
   10: center align, y lower
   -1: right align
  Text between | pairs is rendered as a subscript.
  '''
  if '|' in text:
    draw_text_sub(text, angle, align)
    return
  with transform():
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
def draw_text_sub(text, angle, align):
  ''' draw_text for strings with |subscript| segments (odd parts after
  splitting on |). Subscripts are 0.7x size, dropped by 0.25x size. '''
  parts = text.split('|')
  sub_drop = 0.25 * cfg.font_size

  def set_size(scale=1.0):
    print(f'{cfg.font} findfont {cfg.font_size*scale} scalefont setfont')

  with transform():
    move_to_xy(0, 0)
    rotate(-cfg.global_rotation_angle + angle)
    print('/wtot 0 def')
    for i, part in enumerate(parts):
      if not part:
        continue
      set_size(0.7 if i % 2 else 1.0)
      print(f'({part}) stringwidth pop wtot add /wtot exch def')
    set_size()
    if align == 1:
      print('(A) stringtop 2.0 div neg 0. exch rmoveto')
    elif align == -1:
      print('wtot neg (A) stringtop 2.0 div neg rmoveto')
    elif align == 0:
      print('wtot 2.0 div neg (A) stringbottom neg rmoveto')
    elif align == 10:
      print('wtot 2.0 div neg (A) stringtop neg rmoveto')
    for i, part in enumerate(parts):
      if not part:
        continue
      set_size(0.7 if i % 2 else 1.0)
      if i % 2:
        print(f'0 {-sub_drop} rmoveto ({part}) show 0 {sub_drop} rmoveto')
      else:
        print(f'({part}) show')
    set_size()

#______________________________________________________________________________
def fill(color):
  if color is None:
    return
  with transform():
    set_color(color)
    print('fill')

#______________________________________________________________________________
def finalize():
  print("showpage")
  print("%%EOF")

#______________________________________________________________________________
def grestore():
  print('grestore')

#______________________________________________________________________________
def gsave():
  print('gsave')

#______________________________________________________________________________
def header():
  bbox = getattr(cfg, 'bbox', None)
  if bbox is None:
    bbox = [0, 0, cfg.paper_width, cfg.paper_height]
  x0, y0, x1, y1 = (v / 10 * cfg.cm_to_point for v in bbox)
  print('%!PS-Adobe-3.0 EPSF-3.0')
  # print('%%Orientation: Landscape')
  print(f'%%Creator: {os.getlogin()}')
  print(f'%%CreationTime: {datetime.datetime.now()}')
  print(f'%%Description: J-PARC E{cfg.experiment} experiment setup ' +
        'in K1.8BR beam line')
  print('%%Pages: 1')
  print(f'%%BoundingBox: {int(x0)} {int(y0)} '
        f'{int(x1 + 1)} {int(y1 + 1)}')
  print('%%EndComments')

#______________________________________________________________________________
def initialize():
  header()
  set_font()
  define_length()
  define_command()
  print('%%EndProlog')
  translate_xy(cfg.paper_width / cfg.scale_factor / 2,
               cfg.paper_height / cfg.scale_factor / 2)
  rotate(cfg.global_rotation_angle + 90)
  set_line_style()

#______________________________________________________________________________
def line_to_xy(x, y, width=None, color=None, dash=None):
  if width is not None or color is not None or dash is not None:
    width = cfg.line_width if width is None else width
    color = cfg.color_black if color is None else color
    dash = [] if dash is None else dash
    set_line_style(width, color, dash)
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
def path_box(x_center, z_center, x, z):
  translate_xy(x_center, z_center)
  newpath()
  move_to_xy(-x, -z)
  line_to_xy( x, -z)
  line_to_xy( x,  z)
  line_to_xy(-x,  z)
  closepath()
  translate_xy(-x_center, -z_center)

#______________________________________________________________________________
def path_circle(r):
  newpath()
  print(f'0 0 {r} mm 0 360 arc')

#______________________________________________________________________________
def path_sector(r_inner, r_outer, theta1, theta2):
  newpath()
  move_to_rtheta(r_outer, theta1)
  arc(r_outer, theta1, theta2)
  line_to_rtheta(r_inner, theta2)
  arcn(r_inner, theta2, theta1)
  closepath()

#______________________________________________________________________________
def path_polygon(x_center, y_center, x_list, y_list):
  if len(x_list) == 0 or len(y_list) == 0 or len(x_list) != len(y_list):
    return
  translate_xy(x_center, y_center)
  newpath()
  for i in range(len(x_list)):
    if i == 0:
      move_to_xy(x_list[0], y_list[0])
    line_to_xy(x_list[i], y_list[i])
  closepath()
  translate_xy(-x_center, -y_center)

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
def set_line_style(width=cfg.line_width, color=cfg.color_black, dash=[]):
  if color < 0 or color is None:
    color = 1.0 # black
  print(f'{width} mm setlinewidth {color} setgray')
  dash_str = '[' + ' '.join(str(d) for d in dash) + ']'
  print(f'{dash_str} 0 setdash')

#______________________________________________________________________________
def stroke():
  print('stroke')
  set_line_style()

#______________________________________________________________________________
def translate_xy(x, y):
  print(f'{x} mm {y} mm translate')

#______________________________________________________________________________
def translate_rtheta(r, theta):
  print(f'{r} {theta} cos mul mm ' +
        f'{r} {theta} sin mul mm translate')
