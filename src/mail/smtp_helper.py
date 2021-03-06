import smtplib


class SmtpHelper(object):

	
	SSLPORT = 465
	DEFPORT = 25
	is_secure = False

	def __init__(self, account_data):
		if account_data.send_host.host_ssl:
			self.is_secure = True
			if account_data.send_host.host_port is not None:
				self.set_port(account_data.send_host.host_port)
			else:
				self.set_port(self.SSLPORT)
		else:
			if account_data.send_host.host_port is not None:
				self.set_port(account_data.send_host.host_port)
			else:
				self.set_port(self.DEFPORT)

		self.server = self.load_connection(account_data)						

	def set_port(self, port):
		self.port = port


	def load_connection(self, account_data):
		if self.is_secure:
			server = smtplib.SMTP_SSL(account_data.send_host.host_name, int(self.port))
		else:
			server = smtplib.SMTP(account_data.send_host.host_name, int(self.port))

		server.set_debuglevel(False)
		server.login(account_data.logon_name, account_data.password)		

		return server


	def send_message(self, message):
		if self.server is not None:
			try:
				print('send')
				self.server.sendmail(message['sender'], message['destination'], message['body'])
			except SMTPRecipientsRefused:
				print('rec refused')
			except SMTPHeloError:
				print('helo')
			except SMTPSenderRefused:
				print('snder')
			except SMTPDataError:		
				print('data')
		

	def close_connection(self):
		if self.server is not None:
			self.server.close()
		
