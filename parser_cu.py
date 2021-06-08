from bs4 import BeautifulSoup
import requests
import csv
import email_sender



def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find('div', class_ = 'c-pl__main__hits').find_all('div', class_ = 'c-productItem')
    links = []

    for div in divs:
        if '1660' in div.find('a', class_ = 'at__productListItemTitle js-tr-productlink').get_text():
            a = div.find('a', class_ = 'catalog-taxons-product__name').get('href')
            links.append('https://www.computeruniverse.net/' + a)
    return links



def get_page_data(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        model = soup.find('h1', class_ = 'at__productheadline').text.strip()
    except:
        model = ''

    try:
        price = soup.find('div', class_ = 'product-price price-value-114498 at__productpricevalue').text.strip()
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
        print('CU:\t' + data['model'] + '   -------   ', data['price'], "Eur")



def main():
    url_cu = "https://www.computeruniverse.net/ru/c/apparatnoe-obespechenie-i-komponenty/videokarty-nvidia?hitsPerPage=120&sortBy=Prod-ComputerUniverse_ru_delivery"

    all_links = get_all_links(get_html(url_cu))

    for x in all_links:
        write_csv(get_page_data(get_html(x), x))




if __name__ == '__main__':
    main()

