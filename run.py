#!/usr/bin/env python3

import misc
import pshelper as ps

#______________________________________________________________________________
def main():
  ps.initialize(experiment=72)
  misc.draw_scale(with_tic=False)
  misc.draw_ff()

  print("newpath")
  print("0 0 moveto")
  print("300 0 lineto")
  print("300 200 lineto")
  print("stroke")

  print("newpath")
  print("150 100 30 0 360 arc")
  print("stroke")

  print("10 220 moveto")
  print("(Beamline) show")

  print("showpage")
  print("%%EOF")

#______________________________________________________________________________
if __name__ == "__main__":
  main()
