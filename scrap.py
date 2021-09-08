import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://elcomercio.pe/noticias/coronavirus/'
XPATH_LINK_TO_ARTICLE = '//div[@class="story-item__information-box w-full"]/h2/a[@itemprop="url"]/@href'
XPATH_TITLE = '//h1[@itemprop="name" and @class="sht__title"]/text()'
XPATH_SUMMARY = '//h2[@itemprop="name" and @class="sht__summary"]/text()'



def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
            except IndexError:
                return


            try:    
                with open(f'{today}/{title.replace(" ","_")}.txt', 'w', encoding='utf-8') as f:
                    f.write(title)
                    f.write('\n\n')
                    f.write(summary)
            except OSError:
                return


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link.replace('/','https://elcomercio.pe/',1), today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()