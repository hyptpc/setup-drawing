import config as cfg
import pshelper as ps

#______________________________________________________________________________
def draw_scale():
  ps.comment('Scale of length')
  x = -8000
  y = -4000
  scale_length = 2000
  n_tic = 4
  tic_size = 300
  subtic_size = 150
  with ps.transform(x, y, -cfg.global_rotation_angle):
    ps.set_line_style(20, 0)
    ''' draw scale line '''
    ps.move_to_xy(0, 0)
    ps.line_to_xy(scale_length, 0)
    ps.stroke()
    ''' draw left tic '''
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
