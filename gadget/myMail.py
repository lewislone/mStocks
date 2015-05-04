# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '2402156431@qq.com'
receiver = 'jdicisyesterday@163.com'
subject = 'pytest'
username = 'actiontec_test@qq.com'
password = 'actiontec1'

#msg = MIMEText('</pre><h1>this is from python test</h1><pre>','html','utf-8')
#msg['Subject'] = subject
msg = MIMEText('this is from python test', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')


smtp = smtplib.SMTP()
smtp.connect('smtp.qq.com', 587)
#smtp.login(username, password)
#smtp.sendmail(sender, receiver, msg.as_string())
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
