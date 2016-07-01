#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pdfkit
import getpass
import smtplib
import lxml.html

from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase

NAVER_SMTP = "smtp.naver.com"
NAVER_SMTP_PORT = 587
NAVER_SUFFIX = "@naver.com"

DAUM_SMTP = "smtp.hanmail.net"
DAUM_SMTP_PORT = 465
DAUM_SUFFIX = "@hanmail.net"

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_SUFFIX = "@gmail.com"

# store the webpage in a byte variable
def html2pdf(url):
	# convert the webpage to pdf
	options={
       	'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-left': '0',
        'margin-bottom': '0',
        'encoding': "UTF-8",
        'no-outline': None,
    }
	return pdfkit.from_url(url, False, options=options)

def get_title_from_webpage(url):
	# Get the title from url
	t = lxml.html.parse(url)
	return t.find(".//title").text

def send_pdf_to_kindle(server, sender, receiver):
	body = MIMEMultipart()
	body["From"] = sender
	body["To"] = receiver
	body["Subject"] = ""

	url = input("킨들에 전송하고자 하는 url을 입력하세요.")

	title = get_title_from_webpage(url)
	try:
		pdf = html2pdf(url)
	except:
		print("pdf 로 변환하는데 오류가 발생했습니다.")
	#pdf = pdfkit.from_url(url, False)
	#file = html2pdf_as_file(url)

	#file = open("out.pdf", "rb")
	attachment = MIMEBase("application/pdf", "application/x-pdf")
	attachment.set_payload(pdf)
	#attachment.set_payload(file.read())
	#file.close()
	encoders.encode_base64(attachment)
	attachment.add_header("Content-Disposition", "attachment", filename= title + '.pdf')
	body.attach(attachment)

	try:
		server.sendmail(sender, receiver, body.as_string())
		print(receiver +  "로 전송 완료")
		server.quit()
	except:
		print('메일을 전송하는데 오류가 발생했습니다.')

def main():
	# initialize configurations for sending email
	while True:
		email_provider = input("어떤 이메일을 사용할까요? 1. 네이버 2. 다음 한메일 3. 구글 지메일")
		if email_provider == '1':
			smtp_server = NAVER_SMTP
			smtp_port = NAVER_SMTP_PORT
			smtp_suffix = NAVER_SUFFIX
			USE_SSL = False
			break
		elif email_provider == '2':
			smtp_server = DAUM_SMTP
			smtp_port = DAUM_SMTP_PORT
			smtp_suffix = DAUM_SUFFIX
			USE_SSL = True
			print("Kindle 허용 이메일에는 @hanmail.net 이메일로 추가해주세요.")
			break
		elif email_provider == '3':
			smtp_server = GMAIL_SMTP
			smtp_port = GMAIL_SMTP_PORT
			smtp_suffix = GMAIL_SUFFIX
			USE_SSL = False
			break
		else: 
			print("잘못 입력하셨습니다.")
	if USE_SSL:
		server = smtplib.SMTP_SSL(smtp_server, smtp_port)
	else:
		server = smtplib.SMTP(smtp_server, smtp_port)
	username = input("로그인 ID를 입력해주세요.")
	sender_email = username + smtp_suffix
	password = getpass.getpass("비밀번호를 입력해주세요.")
	server.starttls()
	server.login(username, password)
	print("로그인 되었습니다.")
	#print("로그인 실패")

	receiver_email = input("Kindle 이메일 계정을 입력하세요.")

	send_pdf_to_kindle(server, sender_email, receiver_email)

if __name__ == "__main__":
    main()
