'''
 bot_status.py
 Created 03/18/22
 Current Version: 1.0
----------------------

Setup:
* Install Python 3.7+ 64-bit

As Administrator - install these packages using pip.

* TBD...
'''

import os, traceback
import random
#from api import SPPD_API
import time
#import HELPER
#import RESTFUL

from dotenv import load_dotenv

import requests

import threading
import re
from collections import namedtuple

load_dotenv()
WSID = os.getenv('WSID') # Web Socket ID
WSTOKEN = os.getenv('WSTOKEN') # Web Socket Token

#BASE_URL = "https://discord.com/api/v8"
BASE_URL = "https://discord.com/api/v10"

HEADERS={
	"X-Unity-Version": "2018.4.26f1",
	"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; VirtualBox Build/MOB31T)",
	"Connection": "Keep-Alive",
	"Accept-Encoding": "gzip"
}

def getAssetList():
	pretty_time=time.strftime('%Y-%m-%d %H:%M', time.localtime())
	print(pretty_time)
	host = f"https://ubistatic-a.akamaihd.net/0081/stable/bundle_version_Android.txt?t={int(time.time())}"
	result = None
	try:
		r = requests.get(host, headers=HEADERS)
		if r.status_code == 200:
			result = r.text
	except:
		print("ERROR: getAssetList")
	time.sleep(1)
	return result

def postMessageToWebhook(content):
	webhook_url = f"{BASE_URL}/webhooks/{WSID}/{WSTOKEN}"
	json = {"content": content}
	try:
		r = requests.post(webhook_url, json=json)
	except:
		print("ERROR: postMessageToWebhook")

ASSET_LIST = []

def findNewAssets(result):
	global ASSET_LIST
	if len(ASSET_LIST) == 0:
		ASSET_LIST = result.split('\r\n')
		print(ASSET_LIST)
		return None
	long_string = ""
	tmp_assets = result.split('\r\n')
	for asset in tmp_assets:
		if asset not in ASSET_LIST:
			ASSET_LIST.append(asset)
			pretty_time=time.strftime('%Y-%m-%d %H:%M', time.localtime())
			long_string += f"{asset} | {pretty_time}\n"
	if long_string == "": return None
	return long_string
	

def execute():

	#postMessageToWebhook("I'm alive!")
	
	RESULT = None
	OFFLINE = False
	while True:
		
		RESULT = getAssetList()
		OFFLINE = RESULT == None
		
		if OFFLINE:
			postMessageToWebhook("SPPD is Offline :(")
			while OFFLINE:
				time.sleep(1 * 60) # Wait 1 minutes
				RESULT = getAssetList()
				OFFLINE = RESULT == None
				if not OFFLINE:
					postMessageToWebhook("SPPD is Online :)")
			
		if RESULT != None:
			NEW_ASSETS = findNewAssets(RESULT)
			if NEW_ASSETS != None:
				postMessageToWebhook(NEW_ASSETS)
				
		time.sleep(1 * 60) # Wait 1 minutes

if __name__ == '__main__':
	#Run
	try:
		execute()
	except Exception as e:
		print("ERROR!")
		print(e)
		