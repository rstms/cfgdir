name = 'cfgdir'

import sys

if sys.version_info[0] < 3:
    from cfgdir import *
else:
    from cfgdir.cfgdir import *
