import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.application import MIMEApplication

data = {
"toaddr" : "xxxxxxx@qq.com",
"fromaddr":"xxxxxx@126.com",
"host":"smtp.126.com",
"user":"xxxxx",
"pwd":"xxxxxxx"
}

def sendmail4(path,name):                         ###发送邮件函数
    global data
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
    msg['From'] = data['fromaddr']
    msg['To']= data['toaddr']
    server = smtplib.SMTP(data['host'])
    server.login(data['user'],data['pwd'])
    #server.set_debuglevel(1)
    server.sendmail(data['fromaddr'], data['toaddr'], msg.as_string())
    server.quit()

