# from rest_framework import serializers
#
#
#
# class StringSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, value):
#         return value
#
#
# class JournalSerializer(serializers.ModelSerializer):
#     author = StringSerializer(many=False)
#     categories = StringSerializer(many=True)
#
#     class Meta:
#         model = Journal
#         fields = ('__all__')
