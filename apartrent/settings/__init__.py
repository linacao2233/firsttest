from .settings_base import * 

try:
	from .settings_local import *
except:
	from .settings_server import *