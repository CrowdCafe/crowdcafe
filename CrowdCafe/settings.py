import os
import socket

hostname = socket.gethostname()

print '----------------------------------'
print hostname

if hostname == "Codesign":

	from settings_digitalocean import *

elif 'VCAP_SERVICES' in os.environ:

	from settings_appfog import *

else:

	from settings_local import *