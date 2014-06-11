import smtplib


class SmtpHelper(object):

	
	SSLPORT = 465
	DEFPORT = 25
	is_secure = False

	def __init__(self, account_data):
		if account_data['is_secure']:
			self.is_secure = True
			if account_data['port'] is not None:
				self.set_port(account_data['port'])
			else:
				self.set_port(self.SSLPORT)
		else:
			if account_data['port'] is not None:
				self.set_port(account_data['port'])
			else:
				self.set_port(self.DEFPORT)

		self.server = self.load_connection(account_data)						

	def set_port(self, port):
		self.port = port


	def load_connection(self, account_data):
		if self.is_secure:
			server = smtplib.SMTP_SSL(account_data['host_name'], int(self.port))
		else:
			server = smtplib.SMTP(account_data['host_name'], int(self.port))

		server.set_debuglevel(False)
		server.login(account_data['logon_name'], account_data['password'])		


	def send_message(self, message):
		if self.server is not None:
			self.server.sendmail(message['sender'], message['destination'], message['body'].as_string())


	def close_connection(self):
		if self.server is not None:
			self.server.close()

			