#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,json,re
import smtplib
import traceback

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


start="HBB";end="JXB";date="2018-02-13";
"""
representation for seat type
wz: null seat, standing ticket
yz: hard seat, normal seat ticket
rz: soft seat, premium seat ticket
yw: hard bed, normal bed ticket
rw: soft bed, premium bed ticket
"""
trains = {
	# 'K7076':('yz','rz','yw','rw'),
	# 'K7028':('yz','rz','yw','rw'),
	'K39':('yz','rz','yw','rw'),
	'K7173':('yz','rz','yw','rw'),
	'K7081':('yz','rz','yw','rw'),
}


"""
sending email notification for avialible train
"""
from email.mime.text import MIMEText
def send_email(content, title=None, sender_gmail=None, sender_password=None, receiver_email=None):
	sender = sender_gmail or '<default sender gmail>'
	password = sender_password or '<default sender password>'
	receiver = receiver_email or '<default receiver email>'

	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()

	msg = MIMEText(content)
	msg['Subject'] = 'Avaiable ticket alert'
	msg['From'] = sender
	msg['To'] = receiver
	
	try:
		server.login(sender,password)
		server.sendmail(sender,receiver,msg.as_string())
		server.quit()
		print 'email sent successfull'
	except:
		print 'error in sending email notification, close connection'
		server.close()

"""
Send query on the train information from start station to end position on date date
Return: http response raw message
"""
def send_query(date, start, end):
	resp = None
	try:
		url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={start}&leftTicketDTO.to_station={to}&purpose_codes=ADULT".format(date=date,start=start,to=end)
		resp=requests.get(url, verify='srca.cer.pem')
		# resp=requests.get("http://www.12306.cn/opn/leftTicket/queryA?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={start}&leftTicketDTO.to_station={to}&purpose_codes=ADULT".format(date=date,start=start,to=end), verify='srca.cer.pem')
		resp.encoding = 'utf-8'
		status = (resp.status_code == 200 and 'query sent success') or 'query sent failed'
		print 'response: '
		print status
		# print resp.text
	except requests.exceptions.ConnectionError:
		print 'connection failed'
		traceback.print_exc()
		return None
	return resp


def has_vacancy_train(entry):
	seats = entry.split('|')
	# if any desired seat available
	return has_vacancy(seats[23]) \
		or has_vacancy(seats[28]) \
		or has_vacancy(seats[29]) \
		or has_vacancy(seats[26])	# null seat


def has_vacancy(seat):
	# regex to test if a value is a digit
	is_digit_pattern = re.compile("\d+")
	return seat.encode('utf-8')=='有' \
		or is_digit_pattern.match(seat.encode('utf-8'))	# check if the value of number is a digit


def main():
	msg=u''
	resp = send_query(date, start, end)
	data=json.loads(resp.text)['data']
	print trains.keys()
	# loop through each train returned
	for train in data['result']:
		for key in trains.keys():
			if key in train and has_vacancy_train(train):
				msg += u'train {} is available on {} from {} to {} \n'.format(key, date, start, end)
	if len(msg)>0:
		print msg
		send_email(msg)

if __name__ == '__main__':
	main()