from rest_framework import serializers
from src.configurations.models import ApplicationProperty

class ApplicationPropertySerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    class Meta:
        model = ApplicationProperty
        # fields = [*get_fields('orders'),]
        fields = '__all__'
        
    def get_section(self, obj):
        return obj.section.name