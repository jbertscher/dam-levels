import urllib.request
import json
import datetime
import time

with open('wu_api_key', 'r') as f:
    API_KEY = f.read()

def get_historic_weather(api_key, date, geo_location):
    f = urllib.request.urlopen('http://api.wunderground.com/api/'+api_key+'/history_'+date+'/q/'+geo_location+'.json')
    json_response = f.read()
    return json.loads(json_response)

def download_historic_weather_json(api_key, date, geo_location, file_location):
    print('Requesting: ', date, geo_location, '...')
    parsed_json = get_historic_weather(api_key, date, geo_location)
    parsed_json = str(parsed_json).replace("'", '"')
    with open(file_location ,'w') as f:
        f.write(parsed_json)
    print('Done. Written to: ', file_location)

if __name__ == "__main__":
    location = {'Theewaterskloof': '-34.078056,19.289167'}
    date = datetime.date(year = 2012, month = 1, day = 1)
    counter = 0
    for dam, loc in location.items():
        while date < datetime.date.today():
            date_string = date.strftime('%Y%m%d')

            download_historic_weather_json(API_KEY,
                                           date_string,
                                           loc,
                                           'data/weather/{0}_{1}.json'.format(dam, date_string))

            date = date + datetime.timedelta(days = 1)
            counter += 1
            if counter == 10:
                print('Sleeping for 65 seconds...')
                time.sleep(65)
                counter = 0
