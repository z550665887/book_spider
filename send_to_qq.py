import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.application import MIMEApplication


def sendmail4(path,name,message):                         ###发送邮件函数
    subject="测试"
    message="测试"
    msg=email.mime.multipart.MIMEMultipart()
    '''
    添加附件
    '''
    txtpart = MIMEApplication(open('{0}/{1}/{2}.txt'.format(path,name,name), 'rb').read())
    txtpart.add_header('Content-Disposition', 'attachment', filename=('gbk', '', '{0}.txt'.format(name)))
    msg.attach(txtpart)

    msg['Subject'] = subject
    msg.attach(email.mime.text.MIMEText(message))
    msg['From'] = message['fromaddr']
    msg['To']= message['toaddr']
    server = smtplib.SMTP(message['host'])
    server.login(message['user'],message['pwd'])
    #server.set_debuglevel(1)
    server.sendmail(message['fromaddr'], message['toaddr'], msg.as_string())
    server.quit()

