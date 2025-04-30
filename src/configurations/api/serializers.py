from rest_framework import serializers
from src.configurations.models import ApplicationProperty

class ApplicationPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationProperty
        # fields = [*get_fields('orders'),]
        fields = '__all__'