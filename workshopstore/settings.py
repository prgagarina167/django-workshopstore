# Django settings for workshopstore project.

from platform import node

if node() == 'bumblebee.yokodzun.kiev.ua':
    PRODUCTION = True
    from settings_production import *
else:
    PRODUCTION = False
    from settings_development import *


DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG
