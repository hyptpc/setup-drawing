import math

ff_angle = 166 - 90

#______________________________________________________________________________
def ff_to_xy(offset):
  ''' ff is center (0, 0) '''
  rad = math.radians(ff_angle)
  x = -offset * math.sin(rad)
  y =  offset * math.cos(rad)
  return x, y

#______________________________________________________________________________
def ff_to_d5(offset=-1456.615-309.4):
  ''' Beam crossing point of the D5 exit yoke face, along the FF axis.
  Survey: yoke exit face is 309.4 mm upstream of BLC2a at z=-1456.615 FF
  (refs/d5_-_blc_position.pdf p.2). '''
  return ff_to_xy(offset)
