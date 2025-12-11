#!/usr/bin/env python3

import driftchamber as dc
import counter
import misc
import pshelper as ps
import shs

#______________________________________________________________________________
def main():
  ps.initialize()
  misc.draw_scale()
  misc.draw_zaxis()
  # misc.draw_ff()
  shs.draw()
  counter.draw()
  dc.draw()
  ps.finalize()

#______________________________________________________________________________
if __name__ == "__main__":
  main()
