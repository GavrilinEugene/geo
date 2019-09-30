import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
from os import listdir
from os.path import isfile, join, splitext, basename


def setup_driver(load_time_out=30):
    driver = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs')
    driver.set_page_load_timeout(load_time_out)
    return driver


def create_snapshot(list_links, suffix):
    df_links = pd.DataFrame(list(set(list_links)))
    df_links.to_csv(f'filename_{suffix}.csv', sep=';', index=None)


def click_on_element(driver, element_text):
    for i in range(10):
        try:
            driver.find_element_by_xpath(f".//*[contains(text(), '{element_text}')]").click()
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            print(e)
            time.sleep(1)
    else:
        raise e


def combine_files(flat_folder, filename):
    if not os.path.exists('combined_files'):
        os.makedirs('combined_files')

    link_parsed_flats = [join(flat_folder, f) for f in listdir(flat_folder) if isfile(join(flat_folder, f))]
    list_df = []
    for file in link_parsed_flats:
        df = pd.read_csv(file, sep=';')
        list_df.append(df)

    df_all = pd.concat(list_df)
    df_all.to_csv(f'combined_files/{filename}.csv', sep=';')
