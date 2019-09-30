from selenium.common.exceptions import TimeoutException
from parse_utils import setup_driver, create_snapshot, click_on_element


def run_parsing(suffix):
    """ Обход сайта для получения ссылко на квартиры """
    flats = []
    page = 1
    while True:
        links = driver.find_elements_by_xpath("//a[@href]")
        for link in links:
            if 'kvartiry/' in link.get_attribute("href") and 'p=' not in link.get_attribute(
                    "href") and 'prodam' not in link.get_attribute("href"):
                flats.append(link.get_attribute("href"))

        flats = list(set(flats))
        print(f'page {page} finished, found {len(flats)}')
        page = page + 1
        try:
            python_button = driver.find_element_by_link_text("Следующая страница →")
            python_button.click()
        except Exception as e:
            create_snapshot(flats, suffix)
            print(str(e))
            break
        create_snapshot(flats, suffix)


def strategy_1_new_flats(driver, suffix, city='moskva'):
    """ Настраиваем сайт так, чтобы получить максимум квартир"""
    try:
        driver.get(f'https://www.avito.ru/{city}/kvartiry/prodam')
        click_on_element(driver, 'Новостройка')
        click_on_element(driver, '1 комната')
    except TimeoutException:
        print("can't load page")

    run_parsing(f'{suffix}_{city}')


def strategy_2_new_flats(driver, suffix, city='moskva'):
    """ Настраиваем сайт так, чтобы получить максимум квартир"""
    try:
        driver.get(f'https://www.avito.ru/{city}/kvartiry/prodam')
        click_on_element(driver, 'Новостройка')
        click_on_element(driver, '2 комнаты')
    except TimeoutException:
        print("can't load page")

    run_parsing(f'{suffix}_{city}')


def strategy_3_4_new_flats(driver, suffix, city='moskva'):
    """ Настраиваем сайт так, чтобы получить максимум квартир"""
    try:
        driver.get(f'https://www.avito.ru/{city}/kvartiry/prodam')
        click_on_element(driver, 'Новостройка')
        click_on_element(driver, '3 комнаты')
        click_on_element(driver, '4 комнаты')
    except TimeoutException:
        print("can't load page")

    run_parsing(f'{suffix}_{city}')


def strategy_1_2_old_flats(driver, suffix, city='moskva'):
    """ Настраиваем сайт так, чтобы получить максимум квартир"""
    try:
        driver.get(f'https://www.avito.ru/{city}/kvartiry/prodam')
        click_on_element(driver, 'Вторичка')
        click_on_element(driver, '1 комната')
        click_on_element(driver, '2 комнаты')
    except TimeoutException:
        print("can't load page")

    run_parsing(f'{suffix}_{city}')


def strategy_3_4_old_flats(driver, suffix, city='moskva'):
    """ Настраиваем сайт так, чтобы получить максимум квартир"""
    try:
        driver.get(f'https://www.avito.ru/{city}/kvartiry/prodam')
        click_on_element(driver, 'Вторичка')
        click_on_element(driver, '1 комната')
        click_on_element(driver, '2 комнаты')
    except TimeoutException:
        print("can't load page")

    run_parsing(f'{suffix}_{city}')


if __name__ == "__main__":
    driver = setup_driver()
    # moscow
    strategy_1_new_flats(driver, 1)
    strategy_2_new_flats(driver, 2)
    strategy_3_4_new_flats(driver, 3)
    strategy_1_2_old_flats(driver, 4)
    strategy_3_4_old_flats(driver, 5)

    # moskovskaya_oblast
    strategy_1_new_flats(driver, 1, 'moskovskaya_oblast')
    strategy_2_new_flats(driver, 2, 'moskovskaya_oblast')
    strategy_3_4_new_flats(driver, 3, 'moskovskaya_oblast')
    strategy_1_2_old_flats(driver, 4, 'moskovskaya_oblast')
    strategy_3_4_old_flats(driver, 5, 'moskovskaya_oblast')

    # sankt_peterburg_i_lo
    strategy_1_new_flats(driver, 1, 'sankt_peterburg_i_lo')
    strategy_2_new_flats(driver, 2, 'sankt_peterburg_i_lo')
    strategy_3_4_new_flats(driver, 3, 'sankt_peterburg_i_lo')
    strategy_1_2_old_flats(driver, 4, 'sankt_peterburg_i_lo')
    strategy_3_4_old_flats(driver, 5, 'sankt_peterburg_i_lo')
    driver.quit()

