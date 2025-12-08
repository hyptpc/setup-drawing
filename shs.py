import math

import config as cfg
import geomhelper as geom
import pshelper as ps

#______________________________________________________________________________
def draw():
  ps.comment('Superconducting Hyperon Spectrometer')
  x, y = geom.ff_to_xy(-150)
  with ps.transform(x, y, geom.ff_angle):
    draw_magnet()
    draw_htof()
    draw_hyptpc()
  x, y = geom.ff_to_xy(-150-143)
  with ps.transform(x, y, geom.ff_angle):
    draw_target()

#______________________________________________________________________________
def draw_hyptpc():
  ps.comment('HypTPC')
  w = 500.0 / 2
  l = w * math.tan(math.radians(22.5))
  x = [-w, -w, -l, l, w, w, l, -l, -w]
  y = [-l, l, w, w, l, -l, -w, -w, -l]
  with ps.transform():
    ps.draw_polygon(x, y, cfg.color_light_yellow)
  ps.draw_tag('HypTPC', 0, 250, 0, -1)

#______________________________________________________________________________
def draw_htof():
  ps.comment('HTOF')
  n_layer = 8
  n_seg = 4
  x = 68.0 / 2
  z = 10.0 / 2
  l = 340.0 # distance from center
  for i in range(n_layer):
    with ps.transform():
      ps.rotate(i*45)
      ps.translate_xy(-5*x, -l)
      for j in range(n_seg):
        ps.translate_xy(2*x, 0)
        ps.draw_box(x, z, cfg.color_white)
  ps.draw_tag('HTOF', 0, 340, 140, -4)

#______________________________________________________________________________
def draw_magnet():
  ps.comment('SHS Magnet')
  yoke_x = 1920 / 2
  yoke_z = 1200 / 2
  yoke_hole_outer_r = 800 /2
  yoke_hole_inner_r = 600 /2
  ps.draw_box(yoke_x, yoke_z, cfg.color_light_pink)
  ps.draw_circle(yoke_hole_outer_r, cfg.color_light_gray)
  ps.draw_circle(yoke_hole_inner_r, 1)
  ps.draw_tag('HS Magnet', 0, 1100, 0, 0)

#______________________________________________________________________________
def draw_target():
  ps.comment('Liquid Hydrogen Target')
  r = (113 + 107) / 2 / 2
  ps.draw_circle(r, cfg.color_white)
  # r = 107 / 2
  # ps.draw_circle(r, cfg.color_white)
  # r = 94 / 2
  # ps.draw_circle(r, cfg.color_white)
  r = 80 / 2
  ps.draw_circle(r, cfg.color_light_cyan)
  ps.draw_tag('Target', 0, 20, -20, -5)
