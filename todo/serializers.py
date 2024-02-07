from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

    def create(self, validated_data):
        # Set the user who created the todo based on the currently authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
  
    def update(self, instance, validated_data):
        # Prevent certain fields from being updated
        validated_data.pop('created_at', None)
        return super().update(instance, validated_data)
