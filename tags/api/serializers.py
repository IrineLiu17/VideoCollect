from rest_framework import serializers

from halls.models import Hall
from tags.models import Tags



class TagModelSerializer(serializers.ModelSerializer):
    # videos = serializers.StringRelatedField(many=True)
    # videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())
    
    # tags = serializers.SerializerMethodField()
    tagTimes = serializers.SerializerMethodField()
    
    # def get_videos(self,obj):
    #     return obj.video_set.all()

    
    def get_tagTimes(self,obj):
        return len(obj.get_halls())

   
    class Meta:
        model = Tags
        fields = ['tag','tagTimes']



