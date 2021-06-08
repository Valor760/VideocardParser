from bs4 import BeautifulSoup
import requests
import csv
import email_sender


def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find('div', id='main_container_wrapper').find_all('li', class_ = 'col col--xs-4 product js-product js-touch-hover')
    links = []

    for div in divs:
        if '1660' in div.find(class_ = 'product__title').find('a').get_text() or '1650' in div.find(class_ = 'product__title').find('a').get_text():
            a = div.find('a', class_ = 'overlay').get('href')
            links.append('https://www.rdveikals.lv/' + a)
    return links



def get_page_data(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        model = soup.find('h1', itemprop = "name").get_text()
        model = model.replace('videokarte ', '')
    except:
        model = ''

    try:
        price = soup.find('strong').text.strip()
        price = price[0:3]
        price = int(price)
    except:
        price = ''

    if price < 280:
        email_sender.send_mail(url)

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
        print('RD Electronics:\t' + data['model'] + '   -------   ', data['price'], "Eur")



def main():
    url_dateks = "https://www.rdveikals.lv/categories/lv/417/sort/2/filter/0.461_0_0_0/page/1/Videokartes.html"

    all_links = get_all_links(get_html(url_dateks))

    for x in all_links:
        write_csv(get_page_data(get_html(x), x))




if __name__ == '__main__':
    main()

