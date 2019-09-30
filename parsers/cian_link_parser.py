import numpy as np
from parse_utils import setup_driver, create_snapshot
from bs4 import BeautifulSoup


def run_parsing(driver, subway):

    list_links = []
    for page in range(1, 56):
        link = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&foot_min=45&metro%5B0%5D={subway}&offer_type=flat&only_foot=2&p={page}&room1=1&room2=1&room3=1&sort=price_object_order'
        for i in range(10):
            try:
                driver.get(link)
                break
            except Exception as e:
                print(e)
                driver.quit()
                driver = setup_driver(10)

        if page > 1 and '&p=1' in driver.current_url:
            break

        soup = BeautifulSoup(driver.page_source, 'lxml')
        a_hrefs = soup.find_all('a', href=True)
        list_links.append([x['href'] for x in a_hrefs if 'sale/' in x['href']])
        print(subway, page)

    list_links = [item for sublist in list_links for item in sublist]
    print(f'for subway {subway} found: {len(list(set(list_links)))}')
    create_snapshot(list_links, f'{subway}')


def run():
    array = np.arange(1, 400)
    np.random.shuffle(array)
    driver = setup_driver()
    for subway_station in array:
        try:
            run_parsing(driver, subway_station)
        except Exception as e:
            print(subway_station)
            print(str(e))

    driver.quit()

if __name__ == "__main__":
    run()

