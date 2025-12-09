import math

import config as cfg
import geomhelper as geom
import pshelper as ps

#______________________________________________________________________________
def draw():
  ps.comment('Counter')
  draw_bac()
  draw_bh2()
  draw_kvc()
  if cfg.draw_ftof:
    draw_cvc()
    draw_sac3()
    draw_sfv()

#______________________________________________________________________________
def draw_bac():
  ps.comment('BAC')
  # x, y = geom.ff_to_xy(-603)
  # with ps.transform(x, y, geom.ff_angle):
  #   w = 147 / 2
  #   t = 120 / 2 # real thickness is 5
  #   ps.draw_box(w, t, cfg.color_light_gray)
  x, y = geom.ff_to_xy(-648)
  with ps.transform(x, y, geom.ff_angle):
    w = 115 / 2
    t = 30 / 2 # real thickness is 5
    ps.draw_box(w, t, cfg.color_white)
    ps.draw_tag('BAC', 0, 60, -5, 3)

#______________________________________________________________________________
def draw_bh2():
  ps.comment('BH2')
  x, y = geom.ff_to_xy(-746)
  n_seg = 15
  w = 14 / 2
  t = 5 / 2
  with ps.transform(x, y, geom.ff_angle):
    ps.translate_xy(-(n_seg-1)*w, 0)
    with ps.transform():
      for i in range(n_seg):
        ps.draw_box(w, t, cfg.color_white)
        ps.translate_xy(2*w, 0)
    ps.draw_tag('BH2', 0, 110, -10, 7)

#______________________________________________________________________________
def draw_cvc():
  # ps.comment('CVC')
  ps.comment('FTOF')
  x, y = geom.ff_to_xy(13918)
  n_seg = 34
  w = 100 / 2
  t = 30 / 2
  r_pmt = 2 * 25.4 / 2
  with ps.transform(x, y, geom.ff_angle):
    ps.translate_xy(-(n_seg-1)*w, 0)
    with ps.transform():
      for i in range(n_seg):
        ps.draw_box(w, t, cfg.color_white)
        if cfg.draw_pmt:
          ps.draw_circle(r_pmt, cfg.color_light_gray)
        ps.translate_xy(2*w, 0)
    # ps.draw_tag('CVC', 0, 500, 0, 200)
    ps.draw_tag('FTOF', 0, 350, 0, 200)

#______________________________________________________________________________
def draw_kvc():
  ps.comment('KVC')
  x, y = geom.ff_to_xy(460)
  w = 210 / 2
  t = 20 / 2
  with ps.transform(x, y, geom.ff_angle):
    ps.translate_xy(-216, 0)
    ps.draw_box(w, t, cfg.color_white)
    ps.draw_tag('KVC', 0, 110, 10, -6)

#______________________________________________________________________________
def draw_sac3():
  ps.comment('SAC3')
  x, y = geom.ff_to_xy(14100)
  w = 400 / 2
  t = 120 / 2
  n_pmt = 8
  r_pmt = 2 * 25.4 / 2
  dy = 40
  x_margin = 10
  with ps.transform(x, y, geom.ff_angle):
    ps.draw_box(w, t, cfg.color_white)
    ps.translate_xy(-w+r_pmt+x_margin, dy/2)
    # if cfg.draw_pmt:
    #   for i in range(n_pmt):
    #     ps.draw_circle(r_pmt, cfg.color_light_gray)
    #     ps.translate_xy((w-r_pmt-x_margin)/(n_pmt-1)*2,
    #                     -dy if i%2 == 0 else dy)
    # ps.draw_tag('SAC', 0, 300, 0, 200)

#______________________________________________________________________________
def draw_sfv():
  ps.comment('SFV')
  x, y = geom.ff_to_xy(14200)
  n_seg = 6
  w = 70 / 2
  t = 10 / 2
  r_pmt = 1 * 25.4 / 2
  dy = 3 * t
  with ps.transform(x, y, geom.ff_angle):
    ps.translate_xy(-(n_seg-1)*w, dy)
    with ps.transform():
      for i in range(n_seg):
        ps.draw_box(w+2, t, cfg.color_white)
        if cfg.draw_pmt:
          ps.draw_circle(r_pmt, cfg.color_light_gray)
        ps.translate_xy(2*w, -dy if i%2 == 0 else dy)
    ps.draw_tag('SAC/SFV', 0, 200, 200, 200)
