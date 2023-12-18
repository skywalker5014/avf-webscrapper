from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['POST'])
def parameter():
     search_parameter = request.json
     amazon_filter, flipkart_filter = the_scrapper(search_parameter['product_name'])
     amazonlist = amazon_scrapper(amazon_filter)
     flipkartlist = flipkart_scrapper(flipkart_filter)
     tailored_response = the_processor(amazonlist, flipkartlist)
     return jsonify(tailored_response)
     
     

def the_scrapper(product_name):
     amazon_filter = product_name.replace(' ','+')
     flipkart_filter = product_name.replace(' ', '%20')
     return amazon_filter,flipkart_filter
     


def amazon_scrapper(amazon_filter):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    res = requests.get(f'https://www.amazon.in/s?k={amazon_filter}', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    pricesama = soup.find_all('span',{"class":"a-price-whole"})
    ratingScoreama = soup.find_all('span', {'class':'a-icon-alt'})
    noOfratingama = soup.find_all('span', {'class':'a-size-base s-underline-text'})
    amazonlist = []
    for val in range(0,11):
        amazonObject = {}
        amazonObject['price'] = int(pricesama[val].text.replace(',',''))
        amazonObject['score'] = float(ratingScoreama[val].text.split(' ')[0])
        amazonObject['ratings'] = int(noOfratingama[val].text.replace(',',''))
        amazonlist.append(amazonObject)
    return amazonlist

def flipkart_scrapper(flipkart_filter):
    response = requests.get(f'https://www.flipkart.com/search?q={flipkart_filter}')
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = soup.find_all('div',{"class":"_30jeq3 _1_WHN1"})
    ratingscore = soup.find_all('div', {'class':"_3LWZlK"})
    noOfRating = soup.find_all('span', {'class': "_2_R_DZ"})
    flipkartlist = []
    for val in range(0,5):
        flipkartobj = {}
        flipkartobj['price'] = int(prices[val].text.split("₹")[1].replace(',',''))
        flipkartobj['score'] = float(ratingscore[val].text)
        flipkartobj['ratings'] = int(noOfRating[val].text.split(' ')[0].replace(',',''))
        flipkartlist.append(flipkartobj)
    return flipkartlist

def the_processor(amazonlist, flipkartlist):
    response_obj = {}
    amazondf = pd.DataFrame(amazonlist[2:7])
    flipkartdf = pd.DataFrame(flipkartlist)
    fmean = []
    for item in flipkartdf['price']:
        fmean.append(item)
    fmean = pd.Series(fmean)
    amean = []
    for item in amazondf['price']:
        amean.append(item)
    amean = pd.Series(amean)
    fmin = fmean.min()
    amin = amean.min()
    response_obj['message_1'] = f'FLIPKART sells this for the lowest price of ₹{fmin} AMAZON sells this for the lowest price of ₹{amin}'
    if amin > fmin:
        response_obj['message_2']= f'you can SAVE EXTRA ₹{abs(amin-fmin)} from FLIPKART'
    elif amin < fmin:
        response_obj['message_2'] = f'you can SAVE EXTRA ₹{abs(amin-fmin)} from AMAZON'
    else:
        response_obj['message_2'] = f'Both sells for the same price'
    ascore = round(amazondf['score'].mean())
    fscore = round(flipkartdf['score'].mean())
    if ascore == fscore:
        response_obj['message_3'] = f'both platform has same average rating of {ascore} from customers'
    elif ascore > fscore:
        response_obj['message_3'] = f'AMAZON has higher average rating of {ascore}'
    else:
        response_obj['message_3'] = f'FLIPKART has the highest rating of {fscore}'
    fsum = flipkartdf['ratings'].sum() 
    asum = amazondf['ratings'].sum()
    if fsum > asum :
        response_obj['message_4'] = f'FLIPKART has more ratings, over {abs(fsum-asum)} more customers trust FLIPKART'
    elif fsum < asum: 
        response_obj['message_4'] = f'AMAZON has more ratings, over {abs(fsum-asum)} more customers trust AMAZON'
    else:
        response_obj['message_4'] = f'both have same amount of ratings'
    return response_obj



# #amazon top three
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# res = requests.get('https://www.amazon.in/s?k=asus+tuf+a15', headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')
# pricesama = soup.find_all('span',{"class":"a-price-whole"})
# ratingScoreama = soup.find_all('span', {'class':'a-icon-alt'})
# noOfratingama = soup.find_all('span', {'class':'a-size-base s-underline-text'})
# amazonlist = []
# for ab in range(0,11):
#         amazonObject = {}
#         amazonObject['price'] = int(pricesama[ab].text.replace(',',''))
#         amazonObject['score'] = float(ratingScoreama[ab].text.split(' ')[0])
#         amazonObject['ratings'] = int(noOfratingama[ab].text.replace(',',''))
#         amazonlist.append(amazonObject)

# #flipkart top three
# response = requests.get('https://www.flipkart.com/search?q=asus%20tuf%20a15')
# soup = BeautifulSoup(response.text, 'html.parser')
# prices = soup.find_all('div',{"class":"_30jeq3 _1_WHN1"})
# ratingscore = soup.find_all('div', {'class':"_3LWZlK"})
# noOfRating = soup.find_all('span', {'class': "_2_R_DZ"})
# flipkartlist = []
# for ab in range(0,5):
#         flipkartobj = {}
#         flipkartobj['price'] = int(prices[ab].text.split("₹")[1].replace(',',''))
#         flipkartobj['score'] = float(ratingscore[ab].text)
#         flipkartobj['ratings'] = int(noOfRating[ab].text.split(' ')[0].replace(',',''))
#         flipkartlist.append(flipkartobj)

# amazondf = pd.DataFrame(amazonlist[2:7])
# flipkartdf = pd.DataFrame(flipkartlist)

# fmean = []
# for item in flipkartdf['price']:
#     fmean.append(item)
# fmean = pd.Series(fmean)

# amean = []
# for item in amazondf['price']:
#     amean.append(item)
# amean = pd.Series(amean)


# fmin = fmean.min()
# amin = amean.min()
# print(f'flipkart sells this for the lowest price of {fmin} \namazon sells this for the lowest price of {amin}')
# if amin > fmin:
#     print(f'you can save extra {abs(amin-fmin)} from flipkart')
# else:
#     print(f'you can save extra {abs(amin-fmin)} from amazon')


# ascore = round(amazondf['score'].mean())
# fscore = round(flipkartdf['score'].mean())
# if ascore == fscore:
#     print(f'both platform has same average rating of {ascore} from customers')
# elif ascore > fscore:
#     print(f'amazon has higher average rating of {ascore}')
# else:
#     print(f'flipkart has the highest rating of {fscore}')


# fsum = flipkartdf['ratings'].sum() 
# asum = amazondf['ratings'].sum()

# if fsum > asum :
#     print(f'flipkart has more ratings, over {abs(fsum-asum)} more customers trust flipkart')
# else: 
#     print(f'amazon has more ratings, over {abs(fsum-asum)} more customers trust amazon')



if __name__ == '__main__':
     app.run(port=4000)