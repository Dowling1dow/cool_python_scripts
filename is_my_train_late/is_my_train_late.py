import requests
from lxml import html
from twilio.rest import TwilioRestClient

def get_late_trains():
	irish_rail_url = 'http://www.irishrail.ie/timetables/live-departure-times'
	location_data = dict(key="{{ STATION LOCATION }}")
	depart_page = requests.post(irish_rail_url, data=location_data)
	root = html.fromstring(depart_page.content)

	a_tags = root.xpath('..//a[contains(text(), "Dublin Heuston")]')
	late_trains = []

	for a_tag in a_tags:
	 	tr_tag = a_tag.getparent().getparent()
		sch = int(tr_tag[2].text.replace(":", ""))
		eta = int(tr_tag[3].text.replace(":", ""))
		sch_str = str(sch)
		time_delayed = abs(sch - eta)
		if (time_delayed > 5):
			late_trains.append(sch_str[:2]+":"+sch_str[2:] + " train delayed by "+ str(time_delayed))

	return late_trains

def send_text(late_trains):
	# Using Twilio here
	account_sid = "{{ account_sid }}"
	auth_token  = "{{ auth_token }}"
	client = TwilioRestClient(account_sid, auth_token)
	client.messages.create(
		body=compose_text(late_trains),
	    to="+{{ ENTER NUMBER }}",    # My phone number
	    from_="+{{ ENTER TWILIO NUMBER }}") # Twilio number

def compose_text(late_train_list):
	msg = ""
	for train in late_train_list:
		msg = msg + train + "\n"
	return msg	


late_trains = get_late_trains()
if len(late_trains) != 0:
	send_text(late_trains)

