#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Application routes

Created by: Rui Carmo (https://github.com/rcarmo)
"""

import os, sys, logging

log = logging.getLogger()

version = '1'
prefix = '/api/v%s' % version

# install route submodules
import admin, feeds, assetlist
