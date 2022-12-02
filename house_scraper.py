# https://realpython.com/python-web-scraping-practical-introduction/
# https://developers.google.com/maps/documentation/directions/
# https://developers.google.com/places/web-service/

import requests
import urllib3
import urllib
import re
from contextlib import closing
from bs4 import BeautifulSoup
import os
import operator
import csv
import json
import sys
import subprocess

def get_grocery_store_locations():
    """ 
    Call function only when needed; possibly just once. Get addresses of all Grocery Stores and print this out to a text file. The aim is to figure out what store is the closest.
    """ 
    store_names = [
        'qfc seattle',
        'safeway seattle',
        'albertsons seattle',
        'pcc community markets seattle',
        'metropolitan market seattle',
        'fred meyer seattle',
        'trader joes seattle',
        'whole foods seattle',
        'grocery outlet seattle'
        'larry\'s markets seattle',
        'red apple seattle',
        'kress iga supermarket seattle',
        'target seattle',
    ]

    for store in store_names:
        print("Getting addresses for " + store)
        get_exact_addresses_grocery_stores(store)


def get_exact_addresses_grocery_stores(store):
    # https://maps.googleapis.com/maps/api/place/textsearch/json?query=trader+joes+seattle&key=AIzaSyCOjWTTV4sm104O4qaq-nHwwZu4daytdR4
    output_dir = 'grocery_stores/'
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + store + '&key=' + apikey
    response = requests.get(url)
    if response.status_code == 200:
        store = store.replace(' ', '_')
        with open(output_dir + store + '.txt', 'w') as f:
            for entry in response.json()['results']:
                f.write(entry['formatted_address'] + "\n")


def get_data(url):
    """
    Get the response of the request for a specific house
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
    try:
        with closing(requests.get(url, stream=True, headers=headers, verify=False)) as resp:
            if is_good_response(resp):
                return resp.content.decode('utf-8')
            else:
                return None
    except requests.RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    if resp:
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)

def scrape(resp):
    """
    Extract all house details from response using Beautiful Soup
    """
    soup = BeautifulSoup(resp, 'lxml')
    house_details = {}
    count = 0

    # Description of House
    for p in soup.select('p'):
        if 'class' in p.attrs:
            if p['class'] == ['font-b1']:
                house_details['Description'] = p.get_text()

    # Key Details
    for d in soup.select('div'):
        if 'class' in d.attrs:
            if d['class'] == ['keyDetailsList']:
                for entry in d.contents:
                    tmp = entry.get_text().lower()
                    # HOA
                    if 'hoa' in tmp:
                        tmp = tmp.replace('$', ': ').split(': ')[1]
                        #print(tmp.title())
                        house_details['Hoa'] = tmp.title()
                    # Levels in house
                    elif 'style' in tmp.lower():
                        tmp = tmp.replace('style', 'Style: ').split(':')[1]  
                        if 'condominium' in tmp.title().lower(): 
                            house_details['Style'] = 'condo'
                        elif 'townhouse' in tmp.title().lower(): 
                            house_details['Style'] = 'townhouse'
                        elif 'multi' in tmp.title().lower(): 
                            house_details['Style'] = 'multifamily'
                        elif 'residential' in tmp.title().lower(): 
                            house_details['Style'] = 'residential'
                        elif 'story' in tmp.title().lower(): 
                            house_details['Style'] = 'residential'
                        #print(tmp.title())
            elif d['class'] == ['amenity-group']:
                for entry in d.contents:
                    # Equipment in House
                    tmp=entry.get_text().lower()
                    if 'equipment' in tmp:
                        tmp = tmp.replace('equipment', 'Equipment: ').split(':')[1]  
                        house_details['Equipment'] = tmp
                        #print(tmp)
                    # Stuff included in HOA
                    if 'homeowners association information' in tmp:
                        tmp = tmp.replace('homeowners association information', 'HOA Includes: ').split(':')[1]
                        house_details['Hoa includes'] = tmp
                        #print(tmp)
            elif d['class'] == ['percentage']:
                for entry in d.contents:
                    tmp=entry.get_text().lower()
                    if '/' not in tmp:
                        if count == 0:
                            #print("Walk-Score:", tmp)
                            house_details['Walk-Score'] = tmp
                        elif count == 1:
                            #print("Transit-Score:", tmp)
                            house_details['Transit-Score'] = tmp
                        elif count == 2:
                            #print("Bike-Score:", tmp)
                            house_details['Bike-Score'] = tmp
                        count +=1 
            elif d['class'] == ['info-block']:
                if 'data-rf-test-id' in d.attrs:
                    if d['data-rf-test-id'] == 'abp-beds':
                        house_details['maxbeds'] = d.text.lower().replace('beds', '')
                        house_details['maxbeds'] = house_details['maxbeds'].replace('bed', '')
                    if d['data-rf-test-id'] == 'abp-baths':
                        house_details['maxbaths'] = d.text.lower().replace('baths', '')
                        house_details['maxbaths'] = house_details['maxbaths'].replace('bath', '')
            elif d['class'] == ['info-block', 'price']:
                if 'data-rf-test-id' in d.attrs:
                    if d['data-rf-test-id'] == 'abp-price':
                        house_details['Price'] = d.text.lower().replace('price', '')

    # Get all house details and parse this later
    aboutHouse = soup.findAll('li', attrs={'class': 'entryItem'})
    for entry in aboutHouse:
        tmp = entry.get_text().lower()
        if ':' in tmp:
            l1 = tmp.replace(' ','').split(':')[1]
        else:
            l1 = tmp.replace(' ','')
        
        # Number of bedrooms
        if 'bedrooms' in tmp:
            if 'upper' in tmp:
                house_details['Bedrooms_UpperLevel'] = l1
            elif 'lower' in tmp:
                house_details['Bedrooms_LowerLevel'] = l1
            elif 'main' in tmp:
                house_details['Bedrooms_MainLevel'] = l1

        # Number of bathrooms
        if 'baths' in tmp:
            # No of levels in house
            if 'full' in tmp:
                house_details['Full_Baths'] = l1
            elif '1/2' in tmp:
                house_details['0.5_Baths'] = l1
            elif '3/4' in tmp:
                house_details['0.75_Baths'] = l1

        # Type of heating
        if 'heat' in tmp:
            if 'water' in tmp:
                house_details['Water_heater']  = l1
            else:
                house_details['Room_heater']  = l1

        # Gas or electric stove
        if 'range' in tmp:
            house_details['Cooking'] = l1

        # Elevator or not
        if 'elevator' in tmp:
            house_details['Elevator'] = 'Yes'

        # Parking spot
        if 'assigned spaces' in tmp:
            house_details['Parking_Spot'] = l1

    return house_details


def get_directions(origin, destination, mode):
        """
        Get directions between the start and the end while specifying the mode
        """
        origin = origin.replace('#', '%23')
        destination = destination.replace('#', '%23')
        destination = re.sub(r'\(.*\)', r'', destination)
        fullpath = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&mode={}&key={}'.format(origin, destination, mode, apikey)
        response = requests.get(fullpath, verify=False)
        if response.status_code == 200:
            if response.json()['routes']:
                distance = response.json()['routes'][0]['legs'][0]['distance']
                return(distance['text'])
            else:
                return False
        else:
            print('Failed to get destination', destination)
        print('-' * 10)


def get_transit_directions(origin, destinations):
    """
    Transit directions for daily commute
    """
    directions = {}
    for dest in destinations:
        dest = dest.rstrip()
        fullpath = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + origin + '&destination=' + dest + '&mode=transit' + '&key=' + apikey + '&transit_routing_preference=less_walking'
        response = requests.get(fullpath, verify=False)
        if response.status_code == 200:
            for step in response.json()['routes'][0]['legs'][0]['steps']:
                if dest not in directions:
                    if step['travel_mode'] != 'TRANSIT':
                        directions[dest] = [step['travel_mode'] + ' ' + step['duration']['text'] + '\n']
                    else:
                        directions[dest] = [step['travel_mode'] + ' ' + step['duration']['text'] + ', BUS/TRAIN NUMBER:' + step['transit_details']['line']['short_name'] + '\n']
                else:
                    if step['travel_mode'] != 'TRANSIT':
                        directions[dest].append(step['travel_mode'] + ' ' + step['duration']['text'] + '\n')
                    else:
                        directions[dest].append(step['travel_mode'] + ' ' + step['duration']['text'] + ', BUS/TRAIN NUMBER:' + step['transit_details']['line']['short_name'] + '\n')

    return directions


def get_locality_info(zipcode):
    #Crime Rates - https://www.niche.com/places-to-live/z/98109/
    #Public Schools Niche - https://www.niche.com/api/metadata/?u=https%3A%2F%2Fwww.niche.com%2Fk12%2Fsearch%2Fbest-public-schools%2Fz%2F98109%2F
    #Public Schools Great Schools - https://www.greatschools.org/search/search.page?distance=2&lat=47.6288591&locationLabel=Seattle%2C%20WA%2098109&locationType=zip&lon=-122.34569190000002&st%5B%5D=public_charter&st%5B%5D=public&st%5B%5D=charter&state=WA&tableView=Academic&view=list

    crime_rate_url = 'https://www.niche.com/places-to-live/z/' + str(zipcode)
    resp = get_data(crime_rate_url)
    soup = BeautifulSoup(resp, 'lxml')

    aboutArea= soup.findAll('li', attrs={'class': 'ordered__list__bucket__item'})

    locality_data = {}
    for li in aboutArea:
        t1 = li.text
        if '+' in li.text or '-' in li.text:
            grade = t1[-2:]
            locality_data[t1[:-2]] = t1[-2:]
        else:
            grade = t1[-1]
            locality_data[t1[:-1]] = t1[-1:]
    
    return locality_data


def get_grocery_store_house_distances():
    store_dir = 'grocery_stores/'
    store_directions = {}
    for store in os.listdir(store_dir):
        l1 = {}
        if store.endswith('.txt'):
            with open(store_dir + store, 'r') as f2:
                for address in f2:
                    address = address.rstrip().replace('#', '%23')
                    t1 = get_directions(url_w, address, 'walking')
                    t1 = float(t1.replace(' mi',''))
                    l1[address] = t1
            
            l1 = sorted(l1.items(), key=operator.itemgetter(1))
            if l1:
                store_directions[store.replace('.txt','_') + l1[0][0]] = l1[0][1]

    return store_directions


def get_school_info(url_w, zipcode):
    """
    Get school ratings of all schools close to this house
    """
    school_grade_data = {}
    school_distance_data = {}
    page = 1
    rem = 1
    school_url = 'https://www.niche.com/api/renaissance/results/?zipCode=' + str(zipcode) + '&type=traditional&type=charter&type=magnet&listURL=best-schools&page=' + str(page) + '&searchType=school'
    mode = 'driving'
    resp = requests.get(school_url, verify=False)
    if resp:
        resp_json = json.loads(resp.text)
        limit = resp_json['limit']
        total = resp_json['total']
        count = 1

        while rem > 0:
            rem = total - limit
            entities = resp_json['entities']
            for e in entities:
                #destination = e['content']['entity']['name'] + ',Seattle,WA'
                destination = e['content']['entity']['url']
                distance = get_directions(url_w, destination, mode)
                if 'value' in e['content']['grades'][0]:
                    grade = e['content']['grades'][0]['value']
                    school_grade_data[destination] = float(str(grade))
                    school_distance_data[destination] = float(str(distance).replace(' mi',''))
                else:
                    continue
                count += 1
            page += 1
            school_url = 'https://www.niche.com/api/renaissance/results/?zipCode=' + str(zipcode) + '&type=traditional&type=charter&type=magnet&listURL=best-schools&page=' + str(page) + '&searchType=school'
            resp = requests.get(school_url, verify=False)
            resp_json = json.loads(resp.text)
            total = rem

    return school_grade_data, school_distance_data

def get_closest_link_rail(origin, railstations):
    """
    Get closest link rail stations via walk and transit
    """
    #print("Origin:", origin, "Destination:", destination)
    mode='walking'
    directions = {}

    for destination in railstations:
        destination = destination.rstrip()
        fullpath = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + origin + '&destination=' + destination + '&mode=' + mode + '&key=' + apikey
        response = requests.get(fullpath, verify=False)
        if response.status_code == 200:
            t1 = response.json()['routes'][0]['legs'][0]['distance']['text'].replace(' mi','')
            t1 = float(t1)
            directions[destination] = t1
        else:
            print('Failed to get destination', destination)
    return directions


def get_recently_sold_houses(orig, zipcode, beds, baths, style):
    """
    Calculate directions between sold house and original house, sort by distance and then print price, beds/baths and sell date
    """
    orig = orig.replace('.txt','')
    print('* Getting recently sold houses for {}'.format(zipcode))
    urls = []

    # Exact match for houses
    url1 = 'https://www.redfin.com/zipcode/{}/filter/property-type={},min-beds={},max-beds={},min-baths={},max-baths={},include=sold-6mo'.format(zipcode,style,beds,beds,baths,baths)

    # Start from 1 bed, 1 bath and see what all has been sold in the area
    url2 = 'https://www.redfin.com/zipcode/{}/filter/property-type={},min-beds={},min-baths={},include=sold-6mo'.format(zipcode,style,1,1)
    urls.append(url1)
    urls.append(url2)

    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
    sold_zipcode_path = zipcode + '_sold_houses.txt'

    for url in urls:
        print(url)
        resp = get_data(url)
        soup = BeautifulSoup(resp, 'lxml')
        sold_dist = {}
        sold_price = {}
        sold_date = {}
        sold_bed_bath = {}
        sold_size = {}

        li = soup.findAll('a', href=True)
        for x in li:
            if x['href'].startswith('/stingray'):
                download_url = 'https://www.redfin.com{}'.format(x['href'])
                r = requests.get(download_url, headers=headers)
                if r.status_code == 200:
                    for count, house in enumerate(r.text.rstrip().split('\r\n')[1:], start=1):
                        sell_data = house.split(',')
                        print(sell_data)
                        # Get directions between sold house and original house
                        x = get_directions(orig, sell_data[3], 'driving')

                        # Go here only if you can get directions successfully
                        if x:
                            x = x.replace(',','')
                            x = x.replace(' mi', '')
                            if 'ft' in x:
                                x = float(x.replace(' ft', ''))
                                x = round(x/5280, 2)
                            else:
                                x = float(x)
                           
                            sold_dist[sell_data[3]] =  x

                            # Price for sold house
                            sold_price[sell_data[3]] = sell_data[7]

                            # Date on which the house was sold
                            sold_date[sell_data[3]] = sell_data[1]

                            # How many bedrooms and bathrooms did the house have?
                            sold_bed_bath[sell_data[3]] = sell_data[8] + 'beds,' + sell_data[9] + 'baths'

                            # Sq FT area of the house
                            sold_size[sell_data[3]] = sell_data[11] + ' sq ft'
#                        else:
#                            continue

                    with open(sold_zipcode_path, 'a') as f3:
                        for entry in sorted(sold_dist.items(), key=operator.itemgetter(1)):
                            print(entry[0], ':', str(entry[1]) + ' miles - ', str(sold_price[entry[0]]) + '$', sold_date[entry[0]], sold_bed_bath[entry[0]])
                            t1 = str(entry[0] + ',' + str(entry[1]) + ' miles,' + str(sold_price[entry[0]]) + '$,' + sold_date[entry[0]] + ',' + sold_bed_bath[entry[0]] + ',' + sold_size[entry[0]] + '\n')
                            f3.write(t1)

                        f3.write("-" * 10)
                        f3.write("\n")

                break

    with open(sold_zipcode_path, 'r') as f3:
        sold_houses_data = f3.read()

    return sold_houses_data


# Code starts here
if __name__ == "__main__":
    #Google API Key
    apikey = 'AIzaSyCOjWTTV4sm104O4qaq-nHwwZu4daytdR4'

    #Turn off Python requests warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with open('urls') as f:
        list_of_house_urls = f.readlines()

    for url in list_of_house_urls:
        print(url.rstrip())
        url=url[:-1]
        url_w = re.sub(r'https://www.redfin.com/(.*?)/(.*?)/(.*?)/.*', r"\3-\2-\1", url)

        # Get zipcode for later use in getting schools and crime rates
        zipcode = url_w.split('-')[-3]
        url_w = url_w + '.txt'

        #Scrape that page in RedFin if you haven't downloaded it already
        if not os.path.exists(url_w):
            # Download response
            resp = get_data(url)
    
            # Recording response for offline use
            with open(url_w, 'w') as f:
                f.write(str(resp))
        else:
            print("* Redfin data already retrieved and stored for ", url_w)

        # Extract data from Redfin response
        with open(url_w, 'r') as f:
            resp = f.read()

        #Get directions using Google Maps if you don't have them already downloaded
        results_file = url_w.replace('.txt', '') + "_details.txt"
        if not os.path.exists(results_file):
            with open(results_file, 'w') as f:
                # Locality relevant data
                locality_data = get_locality_info(zipcode)
                print("* Getting information about the neighborhood")
                f.write("About the neighborhood\n\n")
                for k,v in locality_data.items():
                    t1 = k + ':' + v + "\n"
                    f.write(t1)

                f.write('-' * 10)
                f.write("\n")

                # Get all data about the house from RedFin
                print("* Saving data about the house")
                f.write("About the house\n\n")
                house_details = scrape(resp)
                for k,v in house_details.items():
                    #print(k, ':', v)
                    t1 = k + ':' + v + "\n"
                    f.write(t1)
                #print('-' * 10)
                f.write('-' * 10)
                f.write("\n")

                # Transit directions for daily commutes
                with open('work.txt', 'r') as f1:
                    destinations = f1.readlines()

                print("* Calculating common commute locations")
                f.write("Common commute locations\n\n")
                directions = get_transit_directions(url_w, destinations)
                for dest, directions in directions.items():
                    f.write(dest)
                    f.write("\n")
                    for entry in directions:
                        f.write(str(entry))
                    f.write("\n")

                f.write('-' * 10)
                f.write("\n")

                print("* Calculating closest link rail stations")
                # Transit directions for daily commutes
                with open('rail.txt', 'r') as f1:
                    railstations = f1.readlines()

                f.write("Link Rail Stations\n\n")
                directions = get_closest_link_rail(url_w, railstations)
                directions = sorted(directions.items(), key=operator.itemgetter(1))[:2]
                for d in directions:
                    f.write(d[0])
                    f.write(': ')
                    f.write(str(d[1]))
                    f.write(' miles')
                    f.write("\n")
                f.write('-' * 10)
                f.write("\n")

                # Calculate distance from every grocery store for the house
                print("* Calculating grocery store distances")
                f.write("Grocery store distances\n\n")
                store_directions = get_grocery_store_house_distances()
                for k,v in sorted(store_directions.items(), key=operator.itemgetter(1)):
                    t1 = str(k) + ':' + str(v)
                    f.write(t1)
                    f.write(" miles")
                    f.write("\n")
                f.write('-' * 10)
                f.write("\n")

                # School ratings from Niche for the locality
                school_grade_data, school_distance_data = get_school_info(url_w, zipcode)
                print("* Getting information about the schools from niche.com")
                f.write("School ratings for that zipcode. Highest rating first.\n\n")
                for k,v in sorted(school_grade_data.items(), key=operator.itemgetter(1), reverse=True):
                    t1 = k + ':' + str(v) + "\n"
                    f.write(t1)
                f.write('-' * 10)
                f.write("\n")

                f.write("School distances from the house. Closest school first.\n\n")
                for k,v in sorted(school_distance_data.items(), key=operator.itemgetter(1)):
                    t1 = k + ':' + str(v) + " miles\n"
                    f.write(t1)

                f.write('-' * 10)
                f.write("\n")

                # Removing old data for this zipcode
                subprocess.call(["rm", "-rf", zipcode+'.txt'])

                # Get recently sold houses that fit your criteria that sold in that zipcode. Then get distances to each place, and sort by closest distance.
                f.write("Prices for recently sold houses with that zipcode sorted by distance from house\n\n")
                sold_houses_data = get_recently_sold_houses(url_w, zipcode, house_details['maxbeds'], house_details['maxbaths'], house_details['Style'])
                f.write(sold_houses_data)

                # Delimiter before you start the next house
                print('-' * 10)
        else:
            print("* House already analyzed and results in", url_w.replace('.txt','')+'_details.txt')
            print('-' * 10)
