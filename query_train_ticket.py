#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,json,re
import smtplib
import traceback

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


start="JXB";end="HBB";date="2017-01-21";
"""
representation for seat type
wz: null seat, standing ticket
yz: hard seat, normal seat ticket
rz: soft seat, premium seat ticket
yw: hard bed, normal bed ticket
rw: soft bed, premium bed ticket
"""
trains = {
	'K7076':('yz','rz','yw','rw'),
	'K7028':('yz','rz','yw','rw'),
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
		resp=requests.get("http://www.12306.cn/opn/leftTicket/queryA?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={start}&leftTicketDTO.to_station={to}&purpose_codes=ADULT".format(date=date,start=start,to=end), verify='srca.cer.pem')
		resp.encoding = 'utf-8'
		status = (resp.status_code == 200 and 'query sent success') or 'query sent failed'
		print status
	except requests.exceptions.ConnectionError:
		print 'connection failed'
		traceback.print_exc()
		return None
	return resp

def main():
	msg=u''
	resp = send_query(date, start, end)
	data=json.loads(resp.text)
	# regex to test if a value is a digit
	is_digit_pattern = re.compile("\d+")
	# loop through each train returned
	for train in data['data']:
		s = train["queryLeftNewDTO"]
		str = u'{0}: from {1} to {2}; null seat:{3} hard seat:{4} soft seat:{5} hard bed:{6} soft bed:{7}'.format(
			s['station_train_code'],s['start_time'],s['arrive_time'],s['wz_num'],s['yz_num'],s['rz_num'],s['yw_num'],s['rw_num'])
		print str.encode('utf-8')
		# if any desired seat available
		if s['station_train_code'] in trains:
			for seat in trains[s['station_train_code']]:
				num = s[seat+'_num'].encode('utf-8')
				if is_digit_pattern.match(num) :  # check if the value of number is a digit
					msg += u'train {} is available on {} from {} to {} \n'.format(s['station_train_code'],date, start, end)
	if len(msg)>0:
		print msg
		send_email(msg)

if __name__ == '__main__':
	main()