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

		if hasattr(obj, 'calendar'):
			ret = {}
			ret['appointment_id'] = obj.pk
			ret['series'] = obj.series != None
			ret['color'] = obj.calendar.color
			ret['name'] = obj.title
			ret['notes'] = obj.description
			ret['starttime'] = obj.start_date.strftime("%Y-%m-%dT%H:%M:%S.000+0200")
			ret['endtime'] = obj.end_date.strftime("%Y-%m-%dT%H:%M:%S.000+0200")
			
			return ret      

		return json.JSONEncoder.default(self, obj)

