'''
This script gets data from the given list of paginated urls and finds
the average weight of all air-conditioners according to industry-standard
measurements.
'''

import json
import requests


PREFIX = "http://wp8m3he1wt.s3-website-ap-southeast-2.amazonaws.com"
FIRST_PAGE = "/api/products/1"
DIV_FACTOR = 1000000
CONV_FACTOR = 250


def main():
    '''
    Perfroms data retrieval from url and calculates average weight of
    all acs.
    '''

    url = PREFIX + FIRST_PAGE
    total_volume = 0
    total_acs = 0
    # go through all urls
    while url != '':
        # get response in the current url
        try:
            response = requests.get(url)
            response_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print('There was a problem decoding the response from ' +
                  'one of the provided urls. The program will now quit.')
            return
        # go through items in the page
        for item in response_data['objects']:
            if item['category'].lower() == 'air conditioners':
                size = item['size']
                height = float(size['height'])
                width = float(size['width'])
                length = float(size['length'])
                vol = (height * width * length) / DIV_FACTOR
                total_volume += vol
                total_acs += 1

            next_suffix = response_data['next']

            if next_suffix is None:
                url = ''
            else:
                url = PREFIX + next_suffix
    if total_acs == 0:
        print('There were no air-conditioners in the urls provided')
    else:
        average_volume = total_volume / total_acs
        average_weight = average_volume * CONV_FACTOR
        print(f'The average weight of all air conditioners ' +
              f'is {round(average_weight, 4)}kg')


if __name__ == '__main__':
    main()
