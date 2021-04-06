import base64
import cgi
import fnmatch
import gzip
import math
import os
import re
import shutil
import sqlite3
import sys
import time
import requests
import urllib
from urllib.parse import urlparse
import zipfile
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import xml.etree.ElementTree as ET
from datetime import date,datetime,timedelta
from dateutil import parser as dparser
from resources.lib.modules._addon import *


GetDigit = lambda x: int(filter(str.isdigit, x) or 0)

def AddonInfo(addonID,info):
	ADDON = xbmcaddon.Addon(addonID)
	INFO = ADDON.getAddonInfo(info)
	return INFO

def InstallAddon(addonID):
	if not HasAddon(addonID):
		xbmc.executebuiltin('InstallAddon({})'.format(addonID))
	else:
		Log('Addon already installed {}'.format(addonID))

def AddonSetSetting(addonID,setting,value):
	ADDON = xbmcaddon.Addon(addonID)
	ADDON.setSetting(setting, value)
	Sleep(1)
	if ADDON.getSetting(setting) == value:
		Log('{} setting {} modified to {}'.format(addonID,setting,value))
	else:
		Log('{} Unable to modify setting {} to {}'.format(addonID,setting,value))

def AddonSetting(addonID,setting):
	#Use for getting settings of other addons
	setting_str = xbmcaddon.Addon(addonID).getSetting(setting)
	if setting_str == 'true':
		return True
	elif setting_str == 'false':
		return False
	else:
		return setting_str
		
def CreateDir(folder_path):
	if not xbmcvfs.exists(folder_path):
			created = xbmcvfs.mkdir(folder_path)
			if created:
				Log('Directory Created {}'.format(folder_path))
			else:
				Log('Unable to create {}'.format(folder_path))
	else:
		Log('Directory {} already exists'.format(folder_path))

def CreateFile(file_path):
	if not xbmcvfs.exists(file_path):
		file=open(file_path,'a')
		file.close()
		XbmcSleep(5)
		if xbmcvfs.exists(file_path):
			Log('{} created '.format(file_path))
		else:
			Log('{} not created '.format(file_path))
	else:
		Log('{} already excist'.format(file_path))

def CopyFile(src,dst):
	if os.path.exists(src):
		try:
			shutil.copy2(src, dst)
			Sleep(3)
			if PathExists(dst):
				Log('File {} copied to {}'.format(src,dst))
		except:
			xbmcvfs.copy(src, dst)
			Sleep(3)
			if PathExists(dst):
				Log('File {} copied to {}'.format(src,dst))
	else:
		Log('{} does not excist'.format(src))

def bsixfour(s):
	try:
		bs = base64.b64decode(s)
		return bs
	except TypeError:
		Log('s = {} TypeError = {}'.format(s,TypeError))
		return s
	except:
		Log('s = {} Unknown Error'.format(s))
		return s

def ConvertTimeDelta(td):
	#convert timedelta seconds to days h m s 
	days = td.days
	hours, remainder = divmod(td.seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	return days,hours,minutes,seconds

def CreateModule(url='',mode='',name='',description='',icon=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+urllib.quote_plus(description)+"&iconimage="+urllib.quote_plus(icon)
	return u

def DateTimeDelta(date,h=0,d=0):
	newDT = date+timedelta(hours=h,days=d)
	return newDT

def DateTimeObject(date_str,df=False):
	DTO = dparser.parse(date_str,dayfirst=df)
	return DTO

def DateTimeNow():
	DTN = datetime.now()
	return DTN

def DateTimeStrf(dateString,fmt):
	DTS = dateString.strftime(fmt)
	return DTS

def DateTimeStrp(dateString,fmt):
	try:
		DTS = datetime.strptime(dateString, fmt)
	except TypeError:
		DTS = datetime.fromtimestamp(time.mktime(time.strptime(dateString,fmt)))
	return DTS

def DateTimeToday():
	DTT = datetime.today()
	return DTT



def DelAllContents(path,ignore_errors=True):
	if PathExists(path):
		shutil.rmtree(path,ignore_errors=ignore_errors)
		Sleep(3)
		if not PathExists(path):
			Log('{} deleted '.format(path))

def DownloadFile(url,dst):
	from requests.adapters import HTTPAdapter
	from requests.packages.urllib3.util.retry import Retry
	session = requests.Session()
	retry = Retry(connect=3, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	file = session.get(url, stream=True,proxies=urllib.request.getproxies())
	dump = file.raw
	with open(dst, 'wb') as location:
		shutil.copyfileobj(dump, location)
	if os.path.exists(dst):
		Log('File {} downloaded From {}'.format(dst,url))
		return True
	else:
		Log('File {} not downloaded From {}'.format(dst,url))
		return False

def EnscapeStr(s,Quotes=True):
	# escape string to html quotes true will inc " false will not 
	es = cgi.escape(s, quote=Quotes)
	return es


def ExtractZip(file,dst):
	if file.endswith('.zip'):
		z = zipfile.ZipFile(file)
		z.extractall(dst)
	elif file.endswith('.gz'):
		with gzip.open(file, 'r') as f_in, open(dst, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)

def FileMod_dt(file):
	#modified datetime of file returns as 0 if file does not excist 
	if PathExists(file):
		modTime = datetime.fromtimestamp(os.path.getmtime(file))
	else:
		modTime = datetime.fromtimestamp(0)
	return modTime

def FromTimeStamp(dt_stamp,fmt=''):
	stamp = datetime.fromtimestamp(float(dt_stamp))
	if fmt == '':
		return stamp
	else:
		strstamp = stamp.strftime(fmt)
		return strstamp

def FnMatch(string,regex):
	match = fnmatch.fnmatch(string,regex)
	return match

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param


def HasAddon(addonID):
	if xbmc.getCondVisibility('System.HasAddon({})'.format(addonID)):
		return True
	else:
		return False

def KeyBoard(msg,default='',hidden=False):
	text = ''
	kb = xbmc.Keyboard()
	kb.setDefault(default)
	kb.setHeading(msg)
	kb.setHiddenInput(hidden)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
	return text

def Log(msg):
	if setting_true('debug'):
		from inspect import getframeinfo, stack
		fileinfo = getframeinfo(stack()[1][0])
		xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(addon_name,addon_version,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)
	else:pass

def Notify(title='',message='',times='',icon=''):
	if title == '':
		title = addon_name
	if times == '':
		times = '10000'
	if icon == '':
		icon = addon_icon
	Notification = 'Notification({},{},{},{})'.format(title,message,times,icon)
	xbmc.executebuiltin(str(Notification))


def OpenSettings(addonID=''):
	if addonID:
		xbmcaddon.Addon(addonID).openSettings()
	else:
		addon.openSettings()

def PathExists(path):
	if os.path.exists(path):
		return True
	else:
		return False


def ReplaceMulti(string,replace_items):
	#replace_items is a dict with keys {'to replace':'replacement'}
	String = re.compile('|'.join(replace_items.keys()))
	string = String.sub(lambda m:replace_items[m.group(0)],string)
	return string

def RemoveFormatting(label):
	label = re.sub(r"\[/?[BI]\]",'',label)
	label = re.sub(r"\[/?COLOR.*?\]",'',label)
	return label

def SettingDefault(settingID):
	tree = ET.parse(SETTINGS_XML)
	settings = tree.getroot()
	for setting in settings.iter('setting'):
		if setting.attrib.get('id')==settingID:
			if SystemBuild() >= 18:
				s=setting.findtext('default')
				break
			else:
				s=(setting.attrib.get('default',''))
				break
		else:
			s=None
	return s 

def Sleep(sec):
	time.sleep(sec)

def XbmcSleep(sec):
	xbmc.sleep(sec)

def SystemBuild():
	sb = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	return sb

def TimedeltaTotalSeconds(timedelta):
	return (
		timedelta.microseconds + 0.0 +
		(timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def ToTimeStamp(dt):
	#varible must be datetime object
	ts = time.mktime(dt.timetuple())
	return ts


def update_container():
	xbmc.executebuiltin("XBMC.Container.Update")


def UrlFileName(url):
	a = urlparse(url)                   
	return os.path.basename(a.path)




