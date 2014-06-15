from django.core.serializers.python import Serializer

class CalSerializer(Serializer):
	def end_object(self, obj):
		self._current['id'] = obj._get_pk_val()
		self.objects.append(self._current)

