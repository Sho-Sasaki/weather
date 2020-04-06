import requests

from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    ''' index page '''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=<YOUR_KEY>'

    err_msg = ''
    user_msg = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Invalid city name: {}'.format(new_city)
            else:
                err_msg = '{} already exist in the database.'.format(new_city)

        if err_msg:
            user_msg = err_msg
            message_class = 'is-danger'
        else:
            user_msg = 'City added successfully'
            message_class = 'is-success'

    form = CityForm()

    def get_weather(city):
        response = requests.get(url.format(city)).json()
        return {
            'city'  : city.name,
            'temp'  : int(response['main']['temp']),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

    cities = City.objects.all()
    weather_data = [get_weather(c) for c in cities]
    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : user_msg,
        'message_class' : message_class,
    }
    print(context)

    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    ''' delete city '''
    City.objects.get(name=city_name).delete()
    return redirect('home')
    