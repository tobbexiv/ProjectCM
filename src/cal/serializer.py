from django.core.serializers.python import Serializer

class CalSerializer(Serializer):
	def end_object(self, obj):
		self._current['id'] = obj._get_pk_val()
		self.objects.append(self._current)


import json
import datetime
from time import mktime
from cal.models import Calendar

class DateTimeEncoder(json.JSONEncoder):

	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return int(mktime(obj.timetuple()))

		if obj.calendar != '':
			ret = {}
			ret['calendar'] = obj.calendar.id
			ret['title'] = obj.title
			ret['description'] = obj.description
			ret['start_date'] = obj.start_date
			ret['end_date'] = obj.end_date
			
			return ret      

		return json.JSONEncoder.default(self, obj)

