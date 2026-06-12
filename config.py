import os

import yaml

#______________________________________________________________________________
def load(path=None):
  ''' Load drawing settings from a YAML file into module attributes.
  [R, G, B] color lists are encoded into the negative integer form used
  by pshelper.set_color; font_size is scaled by scale_factor. '''
  if path is None:
    path = os.path.join(os.path.dirname(__file__), 'config.yml')
  with open(path) as f:
    settings = yaml.safe_load(f)
  for key, value in settings.items():
    if isinstance(value, list):
      r, g, b = value
      value = -(r * 1000000 + g * 1000 + b)
    globals()[key] = value
  globals()['font_size'] = font_size * scale_factor

load()
