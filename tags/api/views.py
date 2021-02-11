from rest_framework import generics
from django.db.models import Q

from tags.models import Tags
from .serializers import TagModelSerializer

class TagListAPIView(generics.ListAPIView):
    serializer_class = TagModelSerializer

    def get_queryset(self):
        results = Tags.objects.all()
        
        print(results)

        return results
        

