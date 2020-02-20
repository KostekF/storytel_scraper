import sys
import time
from math import ceil
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
from tqdm import tqdm
import pprint

from scraping_functions import scrape_page_range
from db_connector import interact_with_db


def split_equal(min_val, max_val, parts):
    #Creates list with values distributed equally between <min_val; max_val>
    #Should return parts+1 elements but sometimes doesnt (fix maybe?)
    step = ceil((max_val-min_val)/(parts-1))
    bins = list(range(min_val, max_val, step))
    bins.append(max_val)
    return bins


def main():
    books = []
    if len(sys.argv) > 1:
        RANGE_MIN = int(sys.argv[1])
        RANGE_MAX = int(sys.argv[2])
    else:
        RANGE_MIN = 1000
        RANGE_MAX = 1500
        print(f'No range parameters given, testing mode from {RANGE_MIN} to {RANGE_MAX} page_id')
        
    NUM_OF_WORKERS = 20
    ranges = split_equal(RANGE_MIN, RANGE_MAX, NUM_OF_WORKERS)
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = [executor.submit(scrape_page_range, books, ranges[i], ranges[i + 1])
                         for i in range(len(ranges) - 1)]
        #print(future_to_url)

    elapsed_time = round(time.time() - start_time)
    print(f'SCRAPING {RANGE_MAX - RANGE_MIN} pages took {elapsed_time} sec')
    print(f'Found {len(books)} books')

    interact_with_db(books)
    #pprint.pprint(books)

if __name__ == "__main__":
    main()
