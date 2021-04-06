import os
import xbmc
import xbmcaddon
import xbmcvfs

addon           = xbmcaddon.Addon('script.thfczone')
addoninfo       = addon.getAddonInfo
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
setting_set     = addon.setSetting
local_str       = addon.getLocalizedString
has_addon       = lambda x: xbmc.getCondVisibility("System.HasAddon({addon})".format(addon=str(x)))



addon_version   = addoninfo('version')
addon_name      = addoninfo('name')
addon_id        = addoninfo('id')
addon_icon      = addoninfo("icon")
addon_fanart    = addoninfo("fanart")
addon_path      = xbmcvfs.translatePath(addoninfo('path'))
addon_profile   = xbmcvfs.translatePath(addoninfo('profile'))


# XBMC USERDATA FOLDERS
UD_DATABASE = xbmcvfs.translatePath('special://database')

#FILES
CACHEDB = os.path.join(UD_DATABASE,'thfc_zone.db')