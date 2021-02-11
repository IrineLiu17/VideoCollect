from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall
from .models import Video
from .forms import VideoForm, SearchForm, CreateForm, VideoFormSet
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.forms.utils import ErrorList
import urllib
import requests
from rest_framework import serializers
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from tags.models import Tags
from django.conf import settings
from django.contrib.auth.models import User

YOUTUBE_API_KEY = 'AIzaSyAODfuLUC8u5j6cFp3Wxj4_rBiPA-XJxcI'

# Create your views here.
def home(request):
    search_form = SearchForm()
    recent_halls = Hall.objects.all().order_by('-id')
    tags = Tags.objects.all().order_by('-tagTimes')[0:5]
    if request.user.is_authenticated:
        recent_halls = recent_halls.exclude(user=request.user)
    return render(request, 'halls/home.html',{"recent_halls":recent_halls,'search_form':search_form,'tags':tags})


@login_required
def dashboard(request):
    halls = Hall.objects.filter(user=request.user,parent__isnull=True)
    for hall in halls:
        if hall.tags:
            hall.tags = hall.tags.split(",")
    halls_saved = request.user.saved.all()
    for item in halls_saved:
        item.tags = item.tags.split()
        print(item.tags)

    return render(request, 'halls/dashboard.html',{'halls':halls,'halls_saved':halls_saved})

def userdetail(request,pk):
    targetUser = User.objects.get(pk=pk)
    halls = Hall.objects.filter(user=targetUser)
    for hall in halls:
        if hall.tags:
            hall.tags = hall.tags.split(",")
    halls_saved = Hall.objects.filter(user=request.user,parent__isnull=False)
    return render(request, 'halls/user_detail.html',{'halls':halls,'halls_saved':halls_saved,'targetuser':targetUser})

class VideoAddView(generic.TemplateView):
    template_name = "halls/add_video.html"
    search_form = SearchForm()

    def get(self, *args, **kwargs):
        formset = VideoFormSet(queryset=Video.objects.none())
        search_form = SearchForm()
        return self.render_to_response({'video_formset': formset,'search_form':search_form})

    # Define method to handle POST request
    def post(self,request,pk, *args, **kwargs):

        formset = VideoFormSet(data=self.request.POST)
        
        for form in formset:
            print("----------------------------")
            print(form)
            if formset.is_valid():
                video = Video()
                video.url = form.cleaned_data['url']
                parsed_url = urllib.parse.urlparse(video.url)
                video_id = urllib.parse.parse_qs(parsed_url.query).get("v")
                if video_id:
                    video.youtube_id = video_id[0]
                    response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                    json = response.json()
                    
                    video.title = json['items'][0]['snippet']['title']           
                    video.hall = Hall.objects.get(pk=pk)
                    video.save()
        
                else:
                    errors = form._errors.setdefault('url',ErrorList())
                    errors.append('Needs to be a Youtube url.')
        
        return redirect('view_hall',pk)

        # Check if submitted forms are valid
        # if formset.is_valid():
        #     formset.save()
        #     return redirect(reverse_lazy("dashboard"))

        return self.render_to_response({'video_formset': formset})

@login_required
def add_video(request,pk):
    form = VideoForm()
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)
    print(request)
    if request.method == 'GET':
        return render(request, 'halls/add_video.html',{'hall':hall,'form':form,'search_form':search_form})

    if not hall.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get("v")
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                json = response.json()
                
                video.title = json['items'][0]['snippet']['title']           
                video.hall = Hall.objects.get(pk=pk)
                video.save()
                return redirect('view_hall',pk)
            else:
                errors = form._errors.setdefault('url',ErrorList())
                errors.append('Needs to be a Youtube url.')
                
            

    return render(request, 'halls/add_video.html',{"form":form,"search_form":search_form})

@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    print(search_form)
    print(request.GET)
    temp=request.GET
    if "quote" in request.GET:
        print (request.GET.__getitem__("quote"))

    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={ YOUTUBE_API_KEY }')
        if "quote" in request.GET:
            nextPage = request.GET.__getitem__("quote")
            response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&pageToken={nextPage}&maxResults=6&q={encoded_search_term}&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json());
    return JsonResponse({'error':'not able to find the videos'})  

def hall_search(request):
    data=[]
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        halls = Hall.objects.filter(title__icontains=encoded_search_term)
        # response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={encoded_search_term}&key={ YOUTUBE_API_KEY }')
        data = serializers.serialize('json',halls,fields=('title','id'))
        print(data)
        return JsonResponse(data,safe=False);
    return JsonResponse({'error':'not able to find the videos'})  


class SignUp(generic.CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('home')
    template_name='registration/signup.html'

    #override form_valid to login the user??
    def form_valid(self, form):
        view = super(SignUp,self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username,password=password)
        login(self.request,user)
        return view


class SavehallView(generic.View):
    def get(self,request,pk,*args,**kwargs):
        hall = get_object_or_404(Hall,pk=pk)
        if request.user.is_authenticated:
            new_hall = Hall.objects.savehall(request.user,hall)
            return HttpResponseRedirect("/")
        return redirect("view_hall",hall.id)

class CreateHall(LoginRequiredMixin,generic.CreateView):
    # model = Hall
    # fields = ['title','tags']
    form_class = CreateForm
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        #add 
        form.instance.user = self.request.user
        super(CreateHall,self).form_valid(form)
        new_id = Hall.objects.latest('id')
        print(new_id.id)
        return redirect("view_hall",new_id.id)


class ViewHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail.html'

class UserDetailview(generic.DetailView):
    model = User
    template_name='halls/user_detail.html'

class UpdateHall(LoginRequiredMixin, generic.UpdateView):
    # model = Hall
    # fields=['title','tags']
    queryset = Hall.objects.all()
    form_class = CreateForm
    template_name = 'halls/update_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(UpdateHall,self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall
    
    def form_valid(self,form):
        super(UpdateHall,self).form_valid(form)
        hall = super(UpdateHall,self).get_object()
        hall.save()
        return redirect("view_hall",hall.id)


class DeleteHall(LoginRequiredMixin, generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(DeleteHall,self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class DeleteVideo(LoginRequiredMixin,generic.DeleteView):
    model = Video
    template_name = 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo,self).get_object()
        if not video.hall.user == self.request.user:
            raise Http404
        return video
    
    def delete(self,request,pk):
        video = super(DeleteVideo,self).get_object()
        hall_id = video.hall.id
        video.delete()
        return redirect("view_hall",hall_id)
