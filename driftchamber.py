import math

import beamline
import config as cfg
import geomhelper as geom
import pshelper as ps

zref_bcout = -1300.885

#______________________________________________________________________________
def draw():
  ps.comment('Drift Chamber')
  draw_blc1('a')
  draw_blc1('b')
  draw_blc2('a')
  draw_blc2('b')

#______________________________________________________________________________
# BLC1a/b: identical planar MWDCs, 300 mm apart along the beam, effective
# area 256 x 256 mm, layers tilted +/-45 deg (Akaishi thesis Table 2.5).
# Placed on the upstream straight beam axis between the D5 entrance end
# guard (out to 230 mm) and the Q8 yoke face (687 mm).
BLC1_L_B = 310                      # BLC1b center, mm upstream of D5 face
BLC1_L_A = 610                      # BLC1a center

def draw_blc1(label):
  ps.comment('BLC1' + label)
  w = 390 * math.sqrt(2) / 2
  w_window = 261 * math.sqrt(2) / 2
  t = 64 / 2
  if 'a' in label:
    l = BLC1_L_A
    tag_type = -202
  elif 'b' in label:
    l = BLC1_L_B
    tag_type = -202
  else:
    print(f'%%ERROR invalid label={label}')
    return
  with beamline.d5_upstream_frame() as phi_e:
    ps.translate_xy(0, l)
    ps.draw_box(w, t, cfg.color_light_gray)
    ps.draw_box(w_window, t, cfg.color_white)
    # Leader-line tag; the angle un-rotates the text to the ff orientation.
    ps.draw_tag('BLC1'+label, 2 * phi_e - 180, w + 20, 0, tag_type)

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
