#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/10/14
# @Desc  :

from functools import wraps
from lxml import etree
from locale import getdefaultlocale
from urllib.parse import quote
import sys
import os
import random
import json
import requests
import time
import datetime


code_page = getdefaultlocale()

print(code_page)
