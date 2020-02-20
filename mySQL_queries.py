create_book_table = (
        '''
       CREATE TABLE books (
        book_id int PRIMARY KEY AUTO_INCREMENT, 
        title varchar(200) NOT NULL,
        author varchar(100),
        audiobook_or_ebook varchar(10) NOT NULL,
        description_ varchar(3000),
        language_ varchar(50),
        category varchar(100),
        voice_over varchar(200),
        publisher varchar(50),
        release_date date,
        ISBN varchar(20),
        audio_length varchar(20),
        page_id varchar(20) UNIQUE,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
            );
        '''
    )

add_book = (
        '''
        INSERT INTO books 
        (title, author, audiobook_or_ebook, description_, language_, 
		category, voice_over, publisher, release_date, ISBN, audio_length, page_id)
        VALUES (%(title)s, %(author)s, %(audiobook_or_ebook)s, %(description)s,
         %(language)s, %(category)s, %(voice_over)s, %(publisher)s, %(release_date)s,
          %(isbn)s, %(audio_length)s, %(page_id)s);
        '''
    )

