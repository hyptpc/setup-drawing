#!/usr/bin/env python3

import sys

from module import config as cfg
from module import beamline
from module import counter
from module import driftchamber as dc
from module import misc
from module import pshelper as ps
from module import shs

#______________________________________________________________________________
def main():
  if len(sys.argv) > 1:
    cfg.load(sys.argv[1])
  ps.initialize()
  misc.draw_scale()
  misc.draw_zaxis()
  # misc.draw_ff()
  shs.draw()
  counter.draw()
  beamline.draw()
  dc.draw()
  ps.finalize()

#______________________________________________________________________________
if __name__ == "__main__":
  main()
