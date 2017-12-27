import urllib.request
import json
import datetime
import time

with open('wu_api_key.txt', 'r') as f:
    API_KEY = f.read()

def get_historic_weather(api_key, date, geo_location):
    f = urllib.request.urlopen('http://api.wunderground.com/api/'+api_key+'/history_'+date+'/q/'+geo_location+'.json')
    json_response = f.read()
    return json.loads(json_response)

def download_historic_weather_json(api_key, date, geo_location, file_location):
    parsed_json = get_historic_weather(api_key, date, geo_location)
    parsed_json = str(parsed_json).replace("'", '"')
    with open(file_location ,'w') as f:
        f.write(parsed_json)

if __name__ == "__main__":
    print('Starting @ {0}'.format(str(datetime.datetime.now())))

    location = {'Theewaterskloof': '-34.078056,19.289167'}
    location2 = {'hottentots_holland': '-34.1005,18.9645',
                 'two_rivers_farm': '-33.873,19.032',
                 'airport': '-33.965,18.593'}

    date = datetime.date(year = 2015, month = 5, day = 24)
    day_counter = 0
    min_counter = 0
    for dam, loc in location.items():
        while date < datetime.date.today():
            date_string = date.strftime('%Y%m%d')
            file_location = 'data/weather/{0}_{1}.json'.format(dam, date_string)

            print('Requesting: ', date_string, loc, '...')
            download_historic_weather_json(API_KEY,
                                           date_string,
                                           loc,
                                           file_location)

            date = date + datetime.timedelta(days = 1)
            print('Done. Written to: ', file_location)

            min_counter += 1
            day_counter += 1
            if min_counter == 9:
                print('Sleeping for a minute...')
                time.sleep(60)
                min_counter = 0
            if day_counter == 480:
                print('Sleeping for 24 hours @ {0}'.format(str(datetime.datetime.now())))
                time.sleep((60*60*24)+(60*5))
                day_counter = 0

