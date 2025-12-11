import math

import config as cfg
import geomhelper as geom
import pshelper as ps

zref_bcout = -1300.885

#______________________________________________________________________________
def draw():
  ps.comment('Drift Chamber')
  draw_blc2('a')
  draw_blc2('b')

#______________________________________________________________________________
def draw_blc2(label):
  ps.comment(label)
  w = 250 * math.sqrt(2) / 2
  t = 64 / 2
  if 'a' in label:
    z = zref_bcout - 105.73 - t
    tag_type = -5
  elif 'b' in label:
    z = zref_bcout + 107.88 + t
    tag_type = -3
  else:
    print(f'%%ERROR invalid label={label}')
    return
  x, y = geom.ff_to_xy(z)
  with ps.transform(x, y, geom.ff_angle):
    ps.draw_box(w, t, cfg.color_light_gray)
    w_window = 165 * math.sqrt(2) / 2
    ps.draw_box(w_window, t, cfg.color_white)
    ps.draw_tag('BLC2'+label, 0, w+20, 0, tag_type)
