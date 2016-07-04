import sys
sys.path.insert(0, '/home/skin/skintosticker')
activate_this = '/home/skin/skintosticker/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from app import app as application
