#!/usr/bin/python
# -*- coding: utf-8 -*-

from .env import is_debug_mode
from .app import app
import os

if __name__ == '__main__':
    app().run(debug=is_debug_mode(), port=os.getenv("PORT", default=5000))
