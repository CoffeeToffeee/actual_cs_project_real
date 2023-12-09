from AppKit import datetime
import time as t

from datetime import datetime
from time import sleep

last_active_name = None
while True:
	active_app = NSWorkspace.sharedWorkspace().activeApplication()
	if active_app:
		if active_app['NSApplicationName'] != last_active_name:
			last_active_name = active_app['NSApplicationName']
			print( '%s: [%s] %s (%s)' % (
				datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				active_app['NSApplicationProcessIdentifier'],
				active_app['NSApplicationPath'],
				active_app['NSApplicationName']
			))
	else:
		if last_active_name:
			print( '%s: %s' % (
				datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				'*** no active app ***'
			))
			last_active_name = None
	sleep(0.05)
