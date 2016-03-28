# 18-842 Distributed Systems // Spring 2016.
# Multegula - A P2P block breaking game.
# ScreenEnum.py.
# Team Misfits // amahmoud. ddsantor. gmmiller. lunwenh.

# imports
from enum import Enum

### Screens - enumerate different screens
class Screens(Enum):
  SCRN_NONE = 0;
  SCRN_SPLASH = 1;
  SCRN_MENU = 2;
  SCRN_PAUSE = 3;
  SCRN_GAME = 4;