import imaplib


class ImapHelper(object):

	SSLPORT = 993
	DEFPORT = 143
	is_secure = False

	def __init__(self, account_data):
		if account_data['is_secure'] == True:
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
			server = imaplib.IMAP4_SSL(account_data['host_name'], int(self.port))
		else:
			server = imaplib.IMAP4(account_data['host_name'], int(self.port))	

		server.login(account_data['logon_name'], account_data['password'])	

		return server


	def load_mailboxes(self):
		if self.server is not None:			
			mailboxes = self.server.list()
			return mailboxes


	def close_connection(self):
		if self.server is not None:			
			self.server.logout()

