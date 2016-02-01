import csv
import re
import sys
import smtplib

def read_csv(csv_file):

    #row[0] = Name if empty means line item.
    #row[2] = Date of transaction.
    #row[5] = E-Mail address
    #row[9] = Item detail that has been formated
    #row[10] = Ammount for item. 

    tmp_name = ''
    d = {}
    count = 0

    with open(csv_file, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	itercsvreader = iter(csvreader)
	next(itercsvreader)   #skip first line what is the csv header.
	for row in itercsvreader:
	    if row[0]:
		tmp_name = re.sub(r'[^\x00-\x7f]',r' ',row[0])
		d[tmp_name] = {}
		d[tmp_name]['total'] = 0

	    if row[5]:
		d[tmp_name]['email'] = row[5]


	    if not row[0]:
		tmp_list = []
		tmp_list.append(row[2])
		tmp_list.append(' '.join(row[9].split()[2:]))
		tmp_list.append(float(row[10]))

		d[tmp_name][count] = {}
		#d[tmp_name][count]['date'] = row[2]
		#d[tmp_name][count]['email'] = row[5]
		#d[tmp_name][count]['item'] = ' '.join(row[9].split()[2:])
		#d[tmp_name][count]['amount'] = float(row[10])
		d[tmp_name][count] = tmp_list
		d[tmp_name]['total'] = d[tmp_name]['total'] + float(row[10])

		count = count + 1
    #print d
    return d   #hehe return the d

def send_email(name, emails, msg):

    sender = 'no-reply@thelab.ms'
    email = ['init6@init6.me']

    message = '''From: TheLab.ms <no-reply@thelab.ms>\r\n
To: %s\r\n
Subject: TheLab.ms - 2015 Contribution Summary\r\n
\r\n
%s,  The rest of the leadership team and I want to thank you for supporting TheLab.ms.\r\n

2015 wrap up\r\n
words\r\n
words\r\n
words\r\n
words\r\n

Contribution Summary:\r\n
%s
''' % (email, name, msg)


    try:
	username = 'jason@thelab.ms'
	password = 'password'

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(username,password)
	smtpObj.sendmail(sender, email, message)
	print("Successfully sent email")
	smtpObj.quit()

    except Exception as e:
	print("Error: Unable to send email: %s" % (e))
	smtpObj.quit()



if __name__ == "__main__":

    csv_file = 'TLbC.CSV'

    data = read_csv(csv_file)

    for key,values in data.iteritems():
	msg = ''
	name = key
	
	total = data[key]['total']
	try:
	    email = data[key]['email']
	except:
	    pass

	for k,v in values.iteritems():
	    if type(v) == list:
		msg += 'Date: %s, Item: %s, Amount: %s\r\n' % (v[0],v[1],v[2])

	if email:
	    send_email(name, email, msg)
	#print('Name: %s' % (name))
	#print('Line item detail:\n%s\n' % (msg) )
