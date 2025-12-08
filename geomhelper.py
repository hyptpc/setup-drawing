import math

ff_angle = 166 - 90

#______________________________________________________________________________
def ff_to_xy(offset):
  ''' ff is center (0, 0) '''
  rad = math.radians(ff_angle)
  x = -offset * math.sin(rad)
  y =  offset * math.cos(rad)
  return x, y
