#!/usr/bin/env python3

import counter
import misc
import pshelper as ps
import shs

#______________________________________________________________________________
def main():
  ps.initialize(experiment=72)
  misc.draw_scale(with_tic=False)
  misc.draw_zaxis()
  # misc.draw_ff()
  shs.draw()
  counter.draw()
  ps.finalize()

#______________________________________________________________________________
if __name__ == "__main__":
  main()
