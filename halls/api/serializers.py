from rest_framework import serializers

from halls.models import Hall
from halls.models import Video
from accounts.api.serializers import UserDisplaySerializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title','url','youtube_id']

class HallModelSerializer(serializers.ModelSerializer):
    # videos = serializers.StringRelatedField(many=True)
    # videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())
    videos = VideoSerializer(many=True,read_only=True)
    user = UserDisplaySerializer()
    tags = serializers.SerializerMethodField()
    saves = serializers.SerializerMethodField()
    did_save = serializers.SerializerMethodField()
    
    # def get_videos(self,obj):
    #     return obj.video_set.all()
    def get_did_save(self,obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated:
            if user in obj.saved.all():
                return True
        return False
    

    def get_tags(self,obj):
        return obj.tags.split(",")
    
    def get_saves(self,obj):
        return obj.saved.all().count()

   
    class Meta:
        model = Hall
        fields = ['title','user','videos','tags','id','saves','did_save']



