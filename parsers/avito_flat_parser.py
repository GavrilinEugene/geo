from parser import AvitoFlatParser
from parse_utils import setup_driver, combine_files
import pandas as pd
from tqdm import tqdm
import os
from os import listdir
from os.path import isfile, join, splitext, basename

FLAT_FOLDER = 'parsed_flats/avito'


def save_file(flats, suffix):
    df = pd.DataFrame(flats)
    df = df[['id', 'lat', 'lon', 'price', 'square', 'floor']]
    df.to_csv(f'{FLAT_FOLDER}/{suffix}_parsed.csv', sep=';', index=None)


def get_list_of_files():
    if not os.path.exists(FLAT_FOLDER):
        os.makedirs(FLAT_FOLDER)

    folder = 'parsed_links/avito'
    link_files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    return link_files


def run():
    link_files = get_list_of_files()
    link_files.remove('parsed_links/avito/filename_1_moskovskaya_oblast.csv')
    for file in link_files:
        df = pd.read_csv(file, sep=';')[1:]
        suffix = splitext(basename(file))[0]
        list_flats = []
        driver = setup_driver()
        print(f'parsing {file} ...')
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            try:
                driver.get(row[0])
                p = AvitoFlatParser(driver.current_url.split('_')[-1], driver.page_source)
                p.parse()
                list_flats.append(p.get_output())
            except Exception as e:
                print(str(e))
                save_file(list_flats, suffix)
                driver.quit()
                driver = setup_driver(15)

        save_file(list_flats, suffix)
        driver.quit()


if __name__ == "__main__":
    # run()
    combine_files(filename='avito_flats', flat_folder='parsed_flats/avito')