import math

from . import config as cfg
from . import geomhelper as geom
from . import pshelper as ps

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
def draw_scale():
  ps.comment('Scale of length')
  x = 4700
  y = -7700
  scale_length = cfg.scale_length*1e3
  n_tic = int(cfg.scale_length)
  tic_size = 300
  subtic_size = 150
  ps.set_font(font=cfg.font, font_size=cfg.font_size*0.8)
  # Rotate -90 so the bar lies horizontally on the page.
  with ps.transform(x, y, -cfg.global_rotation_angle - 90):
    ps.set_line_style(20, 0)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(scale_length, 0)
    ps.stroke()
    if cfg.scale_with_tic:
      ps.move_to_xy(0, 0)
      ps.line_to_xy(0, -tic_size)
      ps.stroke()
      dy = -1.4*tic_size
      with ps.transform(0, dy):
        ps.draw_text(f'{scale_length/1e3:.0f} m',
                     cfg.global_rotation_angle + 180, 0)
      dtic = scale_length / n_tic
      for i in range(n_tic - 1):
        ps.move_to_xy((i+1)*dtic, 0)
        ps.line_to_xy((i+1)*dtic, -subtic_size)
        ps.stroke()
      with ps.transform(scale_length, 0):
        ps.move_to_xy(0, 0)
        ps.line_to_xy(0, -tic_size)
        ps.stroke()
        with ps.transform(0, dy):
          ps.draw_text('0', cfg.global_rotation_angle + 180, 0)
    else:
      with ps.transform(scale_length/2, 3*subtic_size):
        ps.draw_text(f'{scale_length/1e3:.0f} m',
                     cfg.global_rotation_angle + 180, 0)
  ps.set_font()

#______________________________________________________________________________
def draw_zaxis():
  ps.comment('Z axis')
  with ps.transform():
    # upstream
    x, y = geom.ff_to_xy(-2000)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(x, y, dash=[10, 5])
    ps.stroke()
    if not cfg.draw_ftof:
      return
    # downstream straight axis to the forward arm. When compressed, the
    # arm is shifted upstream by cfg.ftof_shift and a wavy break line
    # (perpendicular to the axis) separates it from the SHS region.
    compress = getattr(cfg, 'ftof_compress', True)
    s = cfg.ftof_shift if compress else 0
    z_end = 14309 - s                  # downstream end (SFV)
    ps.move_to_xy(0, 0)
    ps.line_to_xy(*geom.ff_to_xy(z_end), dash=[10, 5])
    ps.stroke()
    if compress:
      draw_break_line(1400, label=f'~{cfg.ftof_shift/1000:.0f} m')

#______________________________________________________________________________
def draw_break_line(z, length=2300, amp=80, label=None):
  ''' Long wavy line perpendicular to the beam axis at drawn FF z,
  marking an omitted distance between the SHS region and the forward
  arm. Spans far enough to read as a cut across the figure; an optional
  label notes the omitted real distance. '''
  rad = math.radians(geom.ff_angle)
  dx, dy = -math.sin(rad), math.cos(rad)   # +z (axis) direction
  px, py = math.cos(rad), math.sin(rad)    # perpendicular to the axis
  cx, cy = geom.ff_to_xy(z)
  n_cycle = max(2, round(2 * length / 245))   # keep ~245 mm wavelength
  n = 20 * n_cycle
  for i in range(n + 1):
    t = -length + 2 * length * i / n
    d = amp * math.sin(2 * math.pi * n_cycle * i / n)
    x, y = cx + t * px + d * dx, cy + t * py + d * dy
    if i == 0:
      ps.move_to_xy(x, y)
    else:
      ps.line_to_xy(x, y)
  ps.stroke()
  if label:
    lx, ly = cx + 0.55 * length * px, cy + 0.55 * length * py
    with ps.transform(lx, ly, -cfg.global_rotation_angle - 90):
      ps.draw_text(label, cfg.global_rotation_angle + 180, 0)
