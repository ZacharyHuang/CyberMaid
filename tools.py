from datetime import datetime
import json

import requests

from resources import openai, weather_api_key
from utils import update_tone_data


def get_master_profile(tool_call) -> str:
    with open('config.json', encoding='utf-8') as config_file:
        return str(json.load(config_file)['profile'])

def get_time(tool_call) -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_weather(tool_call) -> str:
    base_url = "https://api.weatherapi.com/v1/forecast.json"
    arguments = json.loads(tool_call.function.arguments)

    params = {
        "key": weather_api_key,
        "q": arguments['location'],
        "days": arguments['days'],
        "day_fields": "maxtemp_c,mintemp_c,condition",
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    print(data)

    forecast_days = data['forecast']['forecastday']
    output_text = []
    for day in forecast_days:
        date = day['date']
        weather_text = day['day']['condition']['text']
        max_temp_c = day['day']['maxtemp_c']
        min_temp_c = day['day']['mintemp_c']
        output_text.append(f"Date: {date}\nWeather: {weather_text}\nTemperature: {min_temp_c}°C ~ {max_temp_c}°C")
    return "\n\n".join(output_text)

def record_refinement(tool_call) -> str:
    arguments = json.loads(tool_call.function.arguments)
    update_tone_data(data={
        "user": arguments['user'],
        "bad_reply": arguments['bad_reply'],
        "good_reply": arguments['good_reply']
    })
    return "Refinement recorded successfully"
    
tools_map = {
    'get_master_profile': get_master_profile,
    'get_time': get_time,
    'get_weather': get_weather,
    'record_refinement': record_refinement
}

def process_tool_call(tool_call):
    try:
        function_name = tool_call.function.name
        if function_name in tools_map:
            return {
                'tool_call_id': tool_call.id,
                'output': tools_map[function_name](tool_call)
            }
        else:
            raise NotImplementedError(f'{function_name} tool is not supported yet')
    except Exception as e:  # pylint: disable=broad-except
        print(e)
        return {
            'tool_call_id': tool_call.id,
            'output': str(e)
        }