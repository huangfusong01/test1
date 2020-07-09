import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import configs.settings

report_path = configs.settings.REPORT_PATH #'D:\\PycharmProjects\\test\\report\\'#
#print(report_path)
def send_email(report):
    #打开文件
    f = open(report,'rb')
    mail_body = f.read()
    #print(mail_body)
    f.close()

    #发送邮箱服务器
    smtpserver = "smtp.qq.com"
    #端口
    port = 465
    #发送邮箱用户名、密码
    user = '1161313037@qq.com'
    password = 'rjsucylsutuqieec'
    #发送邮箱
    send_emil = '1161313037@qq.com'
    #接收邮箱
    receiver= '18871174055@163.com'
    #发送主题
    subject = '自动化测试报告'

    #邮件中文是MIMEText
    body = MIMEText(mail_body,'html','utf-8')
    #print(body)

    #邮件对象
    msg = MIMEMultipart('related')#创建一个带附件的实例
    msg['Subject'] = Header(subject,'utf-8').encode()
    msg['From'] = Header('hfs','utf-8')
    msg['To'] = Header('HFS','UTF-8')
    msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")
    #msg.attach(body)

    #附件
    att = MIMEText(mail_body,"base64","utf-8")
    att["Content-Type"] = "application/octet-stream"
    att.add_header('Content-Disposition', 'attachment', filename = 'test_report.html')
    msg.attach(att)

    #发送邮件
    smtp = smtplib.SMTP_SSL(host=smtpserver)
    smtp.connect(host=smtpserver,port=port)
    smtp.login(user,password)
    smtp.sendmail(send_emil,receiver,msg.as_string())#发送者和接收者
    smtp.quit()


#对测试报告进行排序，取时间最新的报告
def new_report(report_path):
    lists = os.listdir(report_path)
    print(lists)
    time = os.path.getmtime(report_path)
    print(time)
    key = lambda fn: os.path.getmtime(report_path + "/" + fn)
    print(key)
    lists.sort(key=lambda fn: os.path.getmtime(report_path + "/" + fn))
    print(lists)
    file_new = os.path.join(report_path,lists[-1])
    #print(file_new)
    return  file_new


if __name__ == '__main__':
    report = new_report(report_path)
    try:
        send_email(report)
        print('邮件已发送！请查收')
    except smtplib.SMTPException as Error:

        print(Error.encode('UTF-8'))
        print ("Error:邮件发送失败")
