#Python program to read Transaction List by Customer.CSV from QuickBooks and e-mail customer a Receipt.


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
		d[tmp_name][count] = tmp_list
		d[tmp_name]['total'] = d[tmp_name]['total'] + float(row[10])
		count = count + 1
		
    return d   #hehe return the d

def send_email(name, recipients, msg, total):

    recipient = 'init6@init6.me' # for testing

    gmail_user = 'jason@thelab.ms'
    gmail_pass = 'password'
    
    from_email = 'no-reply@thelab.ms'
    to_email = recipient if type(recipient) is list else [recipient]
    subject = 'TheLab.ms - 2015 Contribution Summary'
    body = '''%s,  The rest of the leadership team and I want to thank you for supporting TheLab.ms.

2015 wrap up
words
words
words
words

Contribution Summary:
%s
Total: $%s
''' % (name, msg, total)

    
    message = '''From: %s\nTo: %s\nSubject: %s\n\n%s''' % (from_email, ", ".join(to_email), subject, body)




    try:

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(gmail_user, gmail_pass)
	smtpObj.sendmail(from_email, to_email, message)
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
	    send_email(name, email, msg, total)
