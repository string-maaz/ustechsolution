# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CricketConfig(AppConfig):
    name = 'cricket'
    
    def ready(self):
        import cricket.signals
