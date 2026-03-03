
import requests

def getCountries():
    try:
        url = "https://country-state-city-search-rest-api.p.rapidapi.com/allcountries"

        headers = {
            "x-rapidapi-key":"d5c5fe5c5dmshf006ed9f1ab63d6p1c8a6djsn1caa7867a7e8",
            "x-rapidapi-host": "country-state-city-search-rest-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        countries =[(country['isoCode'], country['name']) for country in response.json()]
        
        return countries
    except Exception as e:
        print(e)
        return [('----------', '----------')]


def getState(isoCode):
    
    url = "https://country-state-city-search-rest-api.p.rapidapi.com/states-by-countrycode"

    querystring = {"countrycode":"us"}

    headers = {
        "x-rapidapi-key": "d5c5fe5c5dmshf006ed9f1ab63d6p1c8a6djsn1caa7867a7e8",
        "x-rapidapi-host": "country-state-city-search-rest-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    states = [(state['name'].lower(), state['name'] )for state in response.json()]
    
    return states

# print(getCountries())

# print(getState('us'))