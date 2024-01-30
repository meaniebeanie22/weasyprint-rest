#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from .env import is_debug_mode
from .app import app

if __name__ == '__main__':
    app().run(debug=is_debug_mode(), port=os.getenv("PORT", default="5000"))
    print('Main run')
