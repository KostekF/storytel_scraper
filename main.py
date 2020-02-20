import sys
import time
import pickle

from scraping_functions import scrape_page_range
from db_connector import interact_with_db


def pickle_to_file(data, filename='books.txt', append=False):
    #pickles data to file
    with open(filename, 'wb') as fp:   #Pickling
        pickle.dump(data, fp)
    print(f'Books list pickled to books.txt')


def main():
    books = []
    if len(sys.argv) > 1:
        RANGE_MIN = int(sys.argv[1])
        RANGE_MAX = int(sys.argv[2])
    else:
        RANGE_MIN = 40200
        RANGE_MAX = 40300
        print(f'No range parameters given, testing mode from {RANGE_MIN} to {RANGE_MAX} page_id')
        
    start_time = time.time()
    scrape_page_range(books, RANGE_MIN, RANGE_MAX)
    elapsed_time = round(time.time() - start_time)

    print(f'SCRAPING {RANGE_MAX - RANGE_MIN} pages took {elapsed_time} sec')
    print(f'Found {len(books)} books')

    pickle_to_file(books)
    interact_with_db(books)


if __name__ == "__main__":
    main()
