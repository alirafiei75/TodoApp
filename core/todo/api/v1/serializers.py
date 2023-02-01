from rest_framework import serializers
from ...models import Task 
from django.urls import reverse
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task instances"""
    absolute_url = serializers.SerializerMethodField()
    completed = serializers.CreateOnlyDefault
    class Meta:
        model = Task
        fields = [
           'id',
           'user',
           'title',
           'completed',
           'absolute_url',
           'created_date',
           'updated_date', 
        ]
        read_only_fields = ['user']
    
    def get_absolute_url(self, obj):
        """getting the url of each task."""
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('todo:todo-api:task-detail', args=(obj.pk, )))

    def to_representation(self, instance):
        """separating representation and create section.
        also separation of tasks list and task detail representation."""
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('absolute_url', None)
        rep.pop('user', None)
        return rep

    def create(self, validated_data):
        """override create to automate user selection."""
        print(validated_data)
        validated_data['user'] = User.objects.get(id=self.context.get('request').user.id)
        return super().create(validated_data)


class TasksSerializer(TaskSerializer):
    """Serializer for Tasks list.
    Just like the TaskSerializer but 'completed' field is read only."""
    class Meta:
        model = Task
        fields = [
           'id',
           'user',
           'title',
           'completed',
           'absolute_url',
           'created_date',
           'updated_date', 
        ]
        read_only_fields = ['user', 'completed']