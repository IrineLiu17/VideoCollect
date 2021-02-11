from rest_framework import generics
from django.db.models import Q

from halls.models import Hall
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import HallModelSerializer
from .pagination import StandardResultsPagination

class HallListAPIView(generics.ListAPIView):
    serializer_class = HallModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(HallListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        results = Hall.objects.all()
        results = results.filter(parent__isnull=True)
        query = self.request.GET.get("q",None)
        print(query)
        if not query==None:
            results = results.filter(title__icontains=query)
        tag = self.request.GET.get("tag",None)
        print(tag)                
        if not tag==None:
            results = results.filter(tags__icontains=tag)
        print(results)
        if self.request.user.is_authenticated:
            results = results.exclude(user=self.request.user)

        return results
        

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        hall_qs = Hall.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated:
            is_saved = Hall.objects.save_toggle(request.user,hall_qs.first())
            return Response({'saved':is_saved})
        
        return Response({"message":message},status=400)