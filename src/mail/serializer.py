import json
import datetime
from time import mktime
from mail.models import MailAccount

class AccountSerializer(json.JSONEncoder):

	def default(self, obj):
		
		ret = {}
		ret['account_id'] = obj.id
		ret['sender_name'] = obj.sender_name
		ret['email'] = obj.email
			 
		return ret
