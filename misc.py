import math

import config as cfg
import geomhelper as geom
import pshelper as ps

#______________________________________________________________________________
def draw_zaxis():
  ps.comment('Z axis')
  with ps.transform():
    x, y = geom.ff_to_xy(-2000)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(x, y, dash=[10, 5])
    ps.stroke()
    x, y = geom.ff_to_xy(9000)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(x, y, dash=[10, 5])
    ps.stroke()

#______________________________________________________________________________
def draw_ff():
  ps.comment('Final Focus Point (FF)')
  outer_r = 300
  inner_r = outer_r * 0.7
  color = 0.5 # gray
  angle = 0
  with ps.transform():
    ps.set_color(color)
    ps.draw_circle(outer_r, cfg.color_white)
    ps.draw_circle(inner_r, cfg.color_white)
    ps.move_to_xy(-outer_r/math.sqrt(2), -outer_r/math.sqrt(2))
    ps.line_to_xy(outer_r/math.sqrt(2), outer_r/math.sqrt(2))
    ps.stroke()
    ps.move_to_xy(outer_r/math.sqrt(2), -outer_r/math.sqrt(2))
    ps.line_to_xy(-outer_r/math.sqrt(2), outer_r/math.sqrt(2))
    ps.stroke()

#______________________________________________________________________________
def draw_scale(with_tic=False):
  ps.comment('Scale of length')
  x = -8000
  y = -4000
  scale_length = 2000
  n_tic = 4
  tic_size = 300
  subtic_size = 150
  ps.set_font(font=cfg.font, font_size=cfg.font_size*0.8)
  with ps.transform(x, y, -cfg.global_rotation_angle):
    ps.set_line_style(20, 0)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(scale_length, 0)
    ps.stroke()
    if with_tic:
      ps.move_to_xy(0, 0)
      ps.line_to_xy(0, tic_size)
      ps.stroke()
      dy = 1.5*tic_size
      with ps.transform(0, dy):
        ps.draw_text('0', cfg.global_rotation_angle, 0)
      dtic = scale_length / n_tic
      for i in range(n_tic - 1):
        ps.move_to_xy((i+1)*dtic, 0)
        ps.line_to_xy((i+1)*dtic, subtic_size)
        ps.stroke()
      with ps.transform(scale_length, 0):
        ps.move_to_xy(0, 0)
        ps.line_to_xy(0, tic_size)
        ps.stroke()
        with ps.transform(0, dy):
          ps.draw_text(f'{scale_length/1e3:.0f} m', cfg.global_rotation_angle, 0)
    else:
      with ps.transform(scale_length/2, subtic_size):
        ps.draw_text(f'{scale_length/1e3:.0f} m', cfg.global_rotation_angle, 0)
  ps.set_font()
