from django.shortcuts import render,redirect
import requests
import json
from .decorators import user_has_city
from django.http import HttpResponseRedirect,HttpResponse
from .forms import CityForm, UserProfileForm
from .models import city
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        # print(city)
        api_url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=ad6d91c541e7f84004e3201f55d89a05').read()
        api_url2 = json.loads(api_url)

        data = {
            "country": city,
            "weather_description": api_url2['weather'][0]['description'],
            "weather_temperature": api_url2['main']['temp'],
            "weather_pressure": api_url2['main']['pressure'],
            "weather_humidity":api_url2['main']['humidity'],
            "weather_icon": api_url2['weather'][0]['icon'],
        }
        
    else:
        city = None
        data = {
            "country": None,
            "weather_description": None,
            "weather_temperature": None,
            "weather_pressure": None,
            "weather_humidity":None,
            "weather_icon": None,
        }
    print(data['weather_icon'])
    return render(request, 'weather.html', {"city": city, "data" :data})
    


@login_required(login_url='/accounts/login')
def my_profile(request):
  profile=request.user.profile
  if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('my_profile')
  else:
      form = UserProfileForm(instance=request.user.profile)
  

  context={
    'profile':profile,
    'form':form
  }

  return render(request,'my_profile.html',context)  




@login_required(login_url='/accounts/login')
@user_has_city
def about(request) :
    return render(request,'about.html')

@login_required(login_url='/accounts/login') 
@user_has_city 
def delete_city(request, city_name):
    city.objects.get(name=city_name).delete()
    return redirect('home')


@login_required(login_url='/accounts/login')
@user_has_city
def help(request):
    return render(request,'help.html')