import imaplib
import email

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


	def select_mailbox(self, mailbox):
		if self.server is not None:
			self.server.select(mailbox)


	def load_mail_from_mailbox(self):
		mails = []
		typ, data = self.server.uid('search', None, "ALL")

		for num in data[0].split():
			typ, data = self.server.uid('fetch', num, '(RFC822)')
			raw_email = data[0][1]
			mails.append(email.message_from_bytes(raw_email))

		return mails	

	def close_connection(self):
		if self.server is not None:			
			self.server.logout()



