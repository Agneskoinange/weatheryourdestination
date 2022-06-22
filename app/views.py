from django.shortcuts import render,redirect
import requests
import json
from django.http import HttpResponseRedirect,HttpResponse
from .forms import CityForm
from .models import city
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


api_key = "9e26c2486a12a759d7a692b9b05a3948"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
new_city = ("Nairobi")
url = base_url + "appid=" + api_key + "&q=" + new_city
response = requests.get(url)

#views.
@login_required(login_url='/accounts/login')
def index(request):
    
    # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={YOUR API KEY}'
    url =f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid="9e26c2486a12a759d7a692b9b05a3948"'
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}"
    # x = requests.get(url, params={"appid": "9e26c2486a12a759d7a692b9b05a3948"})

    # x = x.json()
    # url='api.openweathermap.org/data/2.5/weather?q={'city'} &units=imperial&appid=9e26c2486a12a759d7a692b9b05a3948'

    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = city.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"
    
    print(err_msg)
    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for citi in cities:

        r = requests.get(url.format(citi)).json()
        city_weather  = {
            'city' : citi.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/weather.html',context)

@login_required(login_url='/accounts/login')
def about(request) :
    return render(request,'weather/about.html')

@login_required(login_url='/accounts/login')  
def delete_city(request, city_name):
    city.objects.get(name=city_name).delete()
    return redirect('home')


@login_required(login_url='/accounts/login')
def help(request):
    return render(request,'weather/help.html')