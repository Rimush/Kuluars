# -*- coding: utf-8 -*-

from portfolio.models import Settings

def load_settings(request):
    return {'site_settings': Settings.load()}
    