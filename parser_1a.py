from bs4 import BeautifulSoup
import requests
import csv
import email_sender



def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find('div', class_ = 'catalog-taxons-products-container__grid-row').find_all('div', class_ = 'catalog-taxons-product catalog-taxons-product--grid-view')
    links = []

    for div in divs:
        if '1660' in div.find('a', class_ = 'catalog-taxons-product__name').get_text() or '1650' in div.find('a', class_ = 'catalog-taxons-product__name').get_text():
            a = div.find('a', class_ = 'catalog-taxons-product__name').get('href')
            links.append('https://www.1a.lv' + a)
    return links



def get_page_data(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        model = soup.find('h1').text.strip()
    except:
        model = ''

    try:
        price = soup.find('span', class_ = 'price').find('span').text.strip()
        price = price[0:3]
        price = int(price)
    except:
        price = ''

    try:
        if price < 280:
            email_sender.send_mail(url)
    except:
        pass


    data = {'model' : model,
            'price' : price,
            'url' : url}

    return data


def write_csv(data):
    with open('videocards.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['model'],
                         data['price'],
                         data['url']))
        print('1a:\t' + data['model'] + '   -------   ', data['price'], "Eur")



def main():
    url_1a = "https://www.1a.lv/c/datoru-komponentes-tikla-produkti/komponentes/video-kartes/2vs?sort=price__desc"

    all_links = get_all_links(get_html(url_1a))

    for x in all_links:
        write_csv(get_page_data(get_html(x), x))




if __name__ == '__main__':
    main()

