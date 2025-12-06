#!/usr/bin/env python3

import pshelper as ps

#______________________________________________________________________________
def main():
  ps.header(experiment=72)
  print("72 72 translate")

  print("newpath")
  print("0 0 moveto")
  print("300 0 lineto")
  print("300 200 lineto")
  print("stroke")

  print("newpath")
  print("150 100 30 0 360 arc")
  print("stroke")

  # print("/Times-Roman findfont 12 scalefont setfont")
  print("10 220 moveto")
  print("(Beamline) show")

  print("showpage")
  print("%%EOF")

#______________________________________________________________________________
if __name__ == "__main__":
  main()
