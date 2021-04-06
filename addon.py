#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xbmc


if float(xbmc.getInfoLabel("System.BuildVersion")[:4]) >= 18:
	xbmc.executebuiltin('Dialog.Close(busydialog)')
from resources.lib.uiControl import window_home
d=window_home.WindowHome()
d.doModal()
del d
