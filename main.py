import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass



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
    
    

if __name__ == "__main__":
    storytel_url = 'https://www.storytel.com/pl/pl/books/1167516'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    r = requests.get(storytel_url, headers=headers)
    open("video.html", "w", encoding='utf8').write(r.text)

    soup = BeautifulSoup(r.text, 'html.parser')
    is_page_avail = soup.select('.heroContentInner')
    if not is_page_avail:
        book = {}
        get_book_data(soup, book)
        print(book)
