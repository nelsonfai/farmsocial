from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime
from django.contrib import messages
# Create your views here.


def apphome(request):
                return render(request, 'agricapps/apphome.html')
def prices (request):
    pass
    return render(request,'template')
def weather (request):
            if request.method=='POST':
                    city= request.POST.get('city')
            else:
                    country_name = request.user.location.name
                    response = requests.get(f"https://restcountries.com/v3.1/name/cameroon?fullText=true")
                    if response.status_code == 200:
                        # Parse JSON response
                        country_data = response.json()
                        # Extract capital city from response
                        #city = country_data[0]["capital"]
                        city = 'yaounde'
                        return city
                    else:
                        # Handle error response
                        return None

            if city:
                
                        apikey='7de287427ec7e9a45fbc14c76c1f7e22'
                        url=f"http://api.openweathermap.org/data/2.5/weather?q=buea&appid={apikey}"
                        result=requests.get(url)
                        response=result.json()
                        
                        if result:
                                temp= response['main']['temp'] 
                                temp_celsius = f'{round(temp- 273.15)} °C'
                                humidity =response['main']['humidity'] 
                                pressure =response['main']['pressure'] 
                                windspeed =response['wind']['speed'] 
                                country=response['sys']['country']
                                city_2=response['name']
                                sunrise_unix=response['sys']['sunrise']
                                sunset_unix= response['sys']['sunset']
                                sunrise= datetime.fromtimestamp(int(sunrise_unix)).strftime('%H:%M:%S')
                                date=datetime.now
                                icon=response['weather'][0]['icon']
                                weather=response['weather'][0]['description']
                                lat=response['coord']['lat']
                                lon=response['coord']['lon']
                            
                                sunset= datetime.fromtimestamp(int(sunset_unix)).strftime('%H:%M:%S')
                                #cloud=['clouds']['all']
                                apikey_onecall='7de287427ec7e9a45fbc14c76c1f7e22'
                                url_onecall=f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,current,hourly&appid={apikey_onecall}"
                                result_onecall= requests.get(url_onecall)
                                data=result_onecall.json()
                                daily=data['daily']
                                
                                
                                for dt in daily:
                                    dt['dt']=(datetime.fromtimestamp(int(dt['dt'])).strftime('%A, %d.%b'))
                                
                                    
                                
                                
                                context={
                                    'city_2':city_2,
                                    'temp':temp_celsius,
                                    'humidity':humidity,
                                    'pressure':pressure,
                                    'windspeed':windspeed,
                                    'country':country,
                                    'sunrise':sunrise,
                                    #'sunset':sunset,
                                    'date':date,
                                    'icon':icon,
                                    'weather':weather,
                                    'daily':daily,
                                
                                }
                                return render(request, 'agricapps/weather.html',context)
                        else:
                            messages.error(request,'City not found!!')
                            return render(request, 'agricapps/weather.html')

                    
