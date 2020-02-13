import requests
from bs4 import BeautifulSoup

storytel_url = 'https://www.storytel.com/pl/pl/books/1167516'
r = requests.get(storytel_url)

soup = BeautifulSoup(r.text, 'html.parser')
error_msg = soup.select('.heroContentInner')

if not error_msg:
    book_wrapper = soup.select_one('#bookDetailWrapper')
    book_title = book_wrapper.select_one('.hide-on-mobile').text.strip()
    print(book_title)
    book_author = book_wrapper.select_one('.expandAuthorName').text.strip()
    print(book_author)

    book_voice_over_elem = book_wrapper.select_one('.expandReaderName')
    
    
    if book_voice_over_elem: # ebooks dont have this field
        book_voice_over = book_voice_over_elem.text.strip()
    else:
        book_voice_over = '-'
    print(book_voice_over)
    
    audiobook_or_ebook = book_wrapper.select_one('.expandReleaseDate').text[:-2].strip()
    print(audiobook_or_ebook)

    book_description = book_wrapper.select_one('.bookDetailText').text.strip()
    print(book_description[:50])
    
    book_language = book_wrapper.select_one('.expanderLanguage').text[7:].strip()
    print(book_language)

    book_category = book_wrapper.select_one('.expandCat').text[11:].strip()
    print(book_category)

    book_add_details = book_wrapper.select_one('.publisherInfoContainer')

    book_details_elems = book_add_details.select('.bookDetailListItem')
    for i, book_elem in enumerate(book_details_elems, start=1):
        if 'Wydawca' in book_elem.text:
            book_publisher = book_elem.text[9:].strip()
            print(book_publisher)
        elif 'Data wydania' in book_elem.text:
            book_release_date = book_elem.text[14:].strip()
            print(book_release_date)
        elif 'ISBN' in book_elem.text:
            book_isbn = book_elem.text[7:].strip()
            print(book_isbn)
        elif 'Czas trwania' in book_elem.text:
            book_audio_length = book_elem.text[14:].strip()
            print(book_audio_length)

