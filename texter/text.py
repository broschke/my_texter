from twilio.rest import TwilioRestClient
import datetime
import random
import time
import os
from texter.time_zone import USTimeZone

#from key import account_sid, auth_token, twilio_number

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_number = os.environ['twilio_number']

#Instantiate class TwilioRestClient with your credentials
client = TwilioRestClient(account_sid, auth_token)

#List that holds the messages that are texted
text = ['Hello. This is your reminder to drink water. Thank you.',
		'Bernardo wants to know if you\'re drinking water. Hugs!',
		'*computer voice* Drink water please!',
		'May I recommend this site: http://greatist.com/health/health-benefits-water',
		'I\'m thirsty. Are you thirsty? Let\'s go grab a water!',
		'It\'s Water O\'Clock somewhere, am I right?',
		'Hey kid, wanna try some water? All the cool kids are drinking it.',
		'Gimme a H. Gimme a 2. Gimme an O. What\'s that spell? Water!',
		'Don\'t you love letting out a big \'Aaaahhh\' after a nice gulp of water?',
		'Kick back, put your feet up, grab a drink of water and enjoy this https://www.youtube.com/watch?v=oHg5SJYRHA0',
		'Waiter, what\'s the water de jour? It\'s the water of the day. Thank you, I\'ll have that.',
		'Listen...Do you hear that? It\'s the sound of you not drinking water.',
		'I heard the watercooler just got a fresh keg, let\'s go!',
		'I know you want a cocktail right now, but a drink of water is more important.',
		'I love the taste of water. Especially frozen into cubes and completely surrounded by vodka.',
		'Tell Janice from Accounting to relax. She\'ll get her numbers after your drink of water',
		'Dihydrogen monoxide is a colorless and odorless chemical compound that the government is purposely telling its citizens to ingest. We must stop this abuse!']


def get_tz(timezone):
	if timezone == "eastern":
		Eastern = USTimeZone(-5, "Eastern",  "EST", "EDT")
		return Eastern
	elif timezone == "central":
		Central  = USTimeZone(-6, "Central",  "CST", "CDT")
		return Central
	elif timezone == "mountain":
		Mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
		return Mountain
	elif timezone == "pacific":
		Pacific  = USTimeZone(-8, "Pacific",  "PST", "PDT")
		return Pacific
	
def send_to_twilio(notification):
	
	contact = notification.user.contacts.first()
	number = '+1'+contact.number1
	client.messages.create(body = random.choice(text),
    	    		to = number, 
    	    		from_ = twilio_number)
	time.sleep(1.5)
	
def send_text(notification):
	actual_timezone = get_tz(notification.timezone)
	d = datetime.datetime.now(actual_timezone)
	
	if notification.status == 'disabled':
		
		return
	
	if d.hour not in range(10, 19):
		
		return
	
	if notification.days == "every_day":
		if notification.frequency == "every_hour":
			send_to_twilio(notification)
		elif notification.frequency == "every_two_hours":
			if d.hour % 2 == 0:
				send_to_twilio(notification)
	elif notification.days == "weekdays_only":
		if d.isoweekday() in range(1, 6):
			if notification.frequency == "every_hour":
				send_to_twilio(notification)
			elif notification.frequency == "every_two_hours":
				if d.hour % 2 == 0:
					send_to_twilio(notification)
		
