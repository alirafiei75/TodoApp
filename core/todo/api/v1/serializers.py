from rest_framework import serializers
from ...models import Task 

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task instances"""
    class Meta:
        model = Task
        fields = [
           'id',
           'user',
           'title',
           'completed',
           'created_date',
           'updated_date', 
        ]