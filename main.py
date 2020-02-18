import requests
from bs4 import BeautifulSoup
import pickle
import pprint
import time
import progressbar
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed as future_as_completed
from math import ceil

def get_basic_book_data(book_wrapper, book):
    #Scrape basic book data,
    #ex. title, author, desc and store it in dict book
    book_title = book_wrapper.select_one('.hide-on-mobile').text.strip()
    book['title'] = book_title
    
    book_author = book_wrapper.select_one('.expandAuthorName').text.strip()
    book['author'] = book_author

    audiobook_or_ebook = book_wrapper.select_one('.expandReleaseDate').text[:-2].strip()
    book['audiobook_or_ebook'] = audiobook_or_ebook

    book_description = book_wrapper.select_one('.bookDetailText').text.strip()
    book['description'] = book_description
    
    book_language = book_wrapper.select_one('.expanderLanguage').text[7:].strip()
    book['language'] = book_language

    book_category = book_wrapper.select_one('.expandCat').text[11:].strip()
    book['category'] = book_category


def get_additional_book_data(book_wrapper, book):
    #Scrape additional book data (if it exists),
    #ex. publisher, release_date, isbn

    book_voice_over_elem = book_wrapper.select_one('.expandReaderName')

    if book_voice_over_elem: # ebooks dont have this field
        book_voice_over = book_voice_over_elem.text.strip()
        book['voice_over'] = book_voice_over

    book_add_details = book_wrapper.select_one('.publisherInfoContainer')
    book_details_elems = book_add_details.select('.bookDetailListItem')
    
    for i, book_elem in enumerate(book_details_elems, start=1):
        if 'Wydawca' in book_elem.text:
            book_publisher = book_elem.text[9:].strip()
            book['publisher'] = book_publisher
            
        elif 'Data wydania' in book_elem.text:
            book_release_date = book_elem.text[14:].strip()
            book['release_date'] = book_release_date
            
        elif 'ISBN' in book_elem.text:
            book_isbn = book_elem.text[7:].strip()
            book['isbn'] = book_isbn
            
        elif 'Czas trwania' in book_elem.text:
            book_audio_length = book_elem.text[14:].strip()
            book['audio_length'] = book_audio_length


def get_book_data(soup, book):
    #Scrape book data from site
   
    book_wrapper = soup.select_one('#bookDetailWrapper')
    get_basic_book_data(book_wrapper, book)
    get_additional_book_data(book_wrapper, book)
    
    
def scrape_book_page(page_id):
    #get html data of given page and scrape info from it
    #return book dictionary if there is book available, else return None
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    storytel_url_base = 'https://www.storytel.com/pl/pl/books/'
    
    storytel_url = storytel_url_base + str(page_id)
    r = requests.get(storytel_url, headers=headers)
    #r = requests.get(storytel_url)
    #open("video.html", "w", encoding='utf8').write(r.text)

    soup = BeautifulSoup(r.text, 'html.parser')
    is_access_denied = soup.select_one('#cf-wrapper')

    if not is_access_denied:
        is_page_avail = soup.select('.heroContentInner')
        if not is_page_avail:
            book = {}
            book['id'] = page_id
            get_book_data(soup, book)
            return book
        return None
    else:
        print('access denied')
        return None

def pickle_to_file(data, filename='books.txt', append=False):
    #pickles data to file
    #TODO: fix appending to file
    if append:
        parameters = 'ab'
    else:
        parameters = 'wb'
    with open(filename, parameters) as fp:   #Pickling
        pickle.dump(data, fp)
    print(f'Books list pickled to books.txt')

def scrape_page_range(books, range_min, range_max):
    #Scrapes page range of books
    #Appends found books to books dict
    #TODO: create one progress bar for all proccesses?
    with progressbar.ProgressBar(max_value=range_max-range_min) as bar:
        for i, page_id in enumerate(range(range_min, range_max)):
            #print('scraping book id=%d'%page_id)
            book = scrape_book_page(page_id)
            if book:
                books.append(book)
            bar.update(i) 

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
        RANGE_MIN = 816814
        RANGE_MAX = 816818
        print('No range parameters given, testing mode')
        
    NUM_OF_PAGES = RANGE_MAX-RANGE_MIN
    NUM_OF_WORKERS = 20
    ranges = split_equal(RANGE_MIN, RANGE_MAX, NUM_OF_WORKERS)
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(scrape_page_range, books, ranges[i], ranges[i+1])
                          for i in range(len(ranges)-1)}
        #print(future_to_url)
        #for future in future_as_completed(future_to_url):
            #print(future.result())

    elapsed_time = round(time.time() - start_time)

    #pprint.pprint(books)
    print(f'SCRAPING {RANGE_MAX-RANGE_MIN} pages took {elapsed_time} sec')
    print(f'Found {len(books)} books')
    if len(books) > 0:
        pickle_to_file(books, append=True)
        
if __name__ == "__main__":
    main()
