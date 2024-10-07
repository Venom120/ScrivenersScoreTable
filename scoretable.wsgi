#!/usr/bin/python3.8
import sys

# Activate the virtual environment
activate_this = '/scoretable/venv/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Set the application path
sys.path.insert(0, "/scoretable")

from scoretable import app as application