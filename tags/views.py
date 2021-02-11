from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import Tags

class TagsView(View):
    def get(self, request, tag, *args, **kwargs):
        obj, created = Tags.objects.get_or_create(tag=tag)

        return render(request, 'tags/tag_view.html',{"obj":obj})