import imaplib
import email
import re
import hashlib
from email.header import decode_header

class ImapHelper(object):

	SSLPORT = 993
	DEFPORT = 143
	is_secure = False

	def __init__(self, account_data):
		if account_data.retrieve_host.host_ssl == True:
			self.is_secure = True
			if account_data.retrieve_host.host_port is not None:
				self.set_port(account_data.retrieve_host.host_port)
			else:
				self.set_port(self.SSLPORT)
		else:
			if account_data.retrieve_host.host_port is not None:
				self.set_port(account_data.retrieve_host.host_port)
			else:
				self.set_port(self.DEFPORT)	
		
		self.server = self.load_connection(account_data)				


	def set_port(self, port):
		self.port = port


	def load_connection(self, account_data):	
		if self.is_secure:			
			server = imaplib.IMAP4_SSL(account_data.retrieve_host.host_name, int(self.port))
		else:
			server = imaplib.IMAP4(account_data.retrieve_host.host_name, int(self.port))	

		server.login(account_data.logon_name, account_data.password)	

		return server


	def load_mailboxes(self):
		if self.server is not None:			
			typ, mailboxes = self.server.list()
			mailbox_names = []			

			for box in mailboxes:			
				mailbox_name = re.split('"', str(box))
				mailbox_names.append(mailbox_name[3])
				
				
			return mailbox_names


	def select_mailbox(self, mailbox):
		if self.server is not None:
			self.server.select(mailbox)


	def load_mail_from_mailbox(self):
		mails = []
		
		typ, data = self.server.uid('search', None, "ALL")
		h = hashlib.sha256()

		for num in data[0].split():
			mail = {}
			typ, data = self.server.uid('fetch', num, '(RFC822)')
			raw_email = data[0][1]
			msg = email.message_from_bytes(raw_email)
			
			subject, encoding = decode_header(msg['subject'])[0]
			if encoding is None:
				mail['subject'] = subject
			else:
				mail['subject'] = subject.decode(encoding)

			mail['source'] = msg
			mail['sender'] = msg['from']
			mail['receiver'] = msg['to']			
			ident = h.update(raw_email)
			mail['identifier'] = h.hexdigest() 
			mails.append(mail)
		

		return mails	

	def close_connection(self):
		if self.server is not None:			
			self.server.logout()



