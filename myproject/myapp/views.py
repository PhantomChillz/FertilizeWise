from django.shortcuts import render
from django.shortcuts import render
from myapp.models import Fertilizers
# from MainModel import predict_fertilizer
import pandas as pd
from sklearn.pipeline import Pipeline
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.MainModel import predict_fertilizer
import requests
import json
from django.http import JsonResponse
from .NPK import get_npk_values
from .models import WeatherPrediction
def index(request):
    return render(request,"index.html")
def get_weather_data(latitude, longitude):
    """Fetch weather details from Open-Meteo API"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            current = data.get('current', {})
            
            # Convert weather code to description
            weather_code = current.get('weather_code', 0)
            weather_descriptions = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Foggy",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow fall",
                73: "Moderate snow fall",
                75: "Heavy snow fall",
                95: "Thunderstorm",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail",
            }
            
            # Calculate moisture using humidity and dew point
            humidity = current.get('relative_humidity_2m')
            dew_point = current.get('dew_point_2m')
            moisture = min(100, max(0, (humidity * 0.6 + (dew_point + 20) * 2))) if humidity and dew_point else 50

            return {
                'temperature': round(current.get('temperature_2m', 0)),
                'humidity': current.get('relative_humidity_2m', 0),
                'description': weather_descriptions.get(weather_code, "Unknown"),
                'feels_like': round(current.get('apparent_temperature', 0)),
                'pressure': current.get('pressure_msl', 0),
                'wind_speed': current.get('wind_speed_10m', 0),
                'moisture': round(moisture, 1),
                'dew_point': round(current.get('dew_point_2m', 0), 1)
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    return None

def predict_view(request):
    context = {}
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX request for weather data
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        if latitude and longitude:
            weather_data = get_weather_data(float(latitude), float(longitude))
            if weather_data:
                return JsonResponse({'weather_data': weather_data})
            return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)
        return JsonResponse({'error': 'Location parameters missing'}, status=400)
    
    # Handle soil type selection and form submission
    if request.method == 'POST':
        soil_type = request.POST.get('soil_type')
        predict = request.POST.get('predict') == 'true'
        
        if soil_type:
            # Get NPK values for selected soil type
            npk_values, error = get_npk_values(soil_type)
            if error:
                context['error'] = error
            else:
                context['npk_values'] = npk_values
                context['selected_soil_type'] = soil_type
                context['selected_crop_type'] = request.POST.get('crop_type')
        
        # Only process prediction if the predict button was clicked
        if predict:
            try:
                # Get location data
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                
                # Get weather data if location is provided
                weather_data = None
                if latitude and longitude:
                    weather_data = get_weather_data(float(latitude), float(longitude))
                    if not weather_data:
                        raise ValueError("Failed to retrieve weather data.")

                # Get input data from form and convert to appropriate types
                input_data = {
                    'Temparature': round(float(request.POST.get('temperature'))) if not weather_data else round(float(weather_data['temperature'])),
                    'Humidity': round(float(request.POST.get('humidity'))) if not weather_data else round(float(weather_data['humidity'])),
                    'Moisture': round(float(request.POST.get('moisture'))),
                    'Soil_Type': request.POST.get('soil_type'),
                    'Crop_Type': request.POST.get('crop_type'),
                    'Nitrogen': int(request.POST.get('nitrogen')),
                    'Potassium': int(request.POST.get('potassium')),
                    'Phosphorous': int(request.POST.get('phosphorous'))
                }

                # Make prediction using the model
                predicted_fertilizer, confidence_score, explanation = predict_fertilizer(input_data)
                data = Fertilizers.objects.get(Fertilizer_Name=predicted_fertilizer)
                
                # Save the prediction and weather data to the model
                WeatherPrediction.objects.create(
                    temperature=input_data['Temparature'],
                    humidity=input_data['Humidity'],
                    moisture=input_data['Moisture'],
                    soil_type=input_data['Soil_Type'],
                    crop_type=input_data['Crop_Type'],
                    predicted_fertilizer=predicted_fertilizer,
                    nitrogen=input_data['Nitrogen'],
                    potassium=input_data['Potassium'],
                    phosphorous=input_data['Phosphorous']
                )

                # Update context with prediction results
                context.update({
                    'data': data,
                    'predicted_fertilizer': predicted_fertilizer,
                    'confidence_score': confidence_score,
                    'explanation': explanation,
                    'weather_data': weather_data
                })
                
                return render(request, 'model_output.html', context)

            except Exception as e:
                context['error'] = str(e)  # Capture the error message
                context['retry'] = True  # Indicate that a retry is possible

    return render(request, 'input_form.html', context)

def get_npk(request):
    """Handle AJAX request for NPK values based on soil type"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        soil_type = request.GET.get('soil_type')
        if soil_type:
            npk_values, error = get_npk_values(soil_type)
            if npk_values:
                return JsonResponse({
                    'success': True,
                    'npk': npk_values
                })
            return JsonResponse({
                'success': False,
                'error': error
            })
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })

