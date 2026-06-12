#!/usr/bin/env python3

import sys

import config as cfg
import beamline
import driftchamber as dc
import counter
import misc
import pshelper as ps
import shs

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
