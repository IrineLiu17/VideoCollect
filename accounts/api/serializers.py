from django.contrib.auth import get_user_model

from rest_framework import serializers

from django.urls import reverse_lazy

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self,obj):
        return reverse_lazy("user_dash",args=[obj.id])

    class Meta:
        model = User
        fields = [
            'username',
            'id',
            'url'
        ]    
    