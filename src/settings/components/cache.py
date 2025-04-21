#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Arvin
# datetime: 1/7/2021 3:54 PM
# software: BioTime
from src.settings.components.env import config

CACHE_HOST = config('REDIS_HOST', default='192.168.1.8')
CACHE_PORT = config('REDIS_PORT', default=6378)
CACHE_PASSWORD = config('CACHE_PASSWORD', default='')
CACHE_DB = config('CACHE_DB', default=1)
