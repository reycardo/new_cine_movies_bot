import requests
from bs4 import BeautifulSoup as bs

class Cine_Movies:
    def __init__(self):        
        self.base_url = 'https://cinemas.nos.pt'
        self.cinemas_prefix = '/Cinemas/Pages/'        
        self.filmes_prefix = '/Filmes/Pages/'
        self.page_suffix = '.aspx'
    
    def key_words_search_words(self, user_message):                
        """Separates user_message in keywords and search_words
        """
        words = user_message.split()[1:]
        keywords = '-'.join(words)
        search_words = ' '.join(words)        
        return keywords, search_words
    

    def search_film(self, keywords, cine):
        """Searches for the film
        """
        response = requests.get(self.base_url+self.filmes_prefix+keywords+self.page_suffix)
        content = response.content
        soup = bs(content, 'html.parser')        
        articles = soup.findAll('article', class_ ='line')
        available_dates = [[date for date in date_options.stripped_strings] for date_options in soup.find('select').findAll('option')]                
        movie_hours = []
        for article in articles:
            if cine in ''.join([[y for y in x.stripped_strings] for x in article.children][1]).lower():
                lst = [[y for y in x.stripped_strings] for x in article.find('div', class_ = 'hours').findAll('a')]
                hours = [item[0] for item in lst]
                movie_hours.append(hours)
        dates_hours = {key: value for keys, value in zip(available_dates, movie_hours) for key in keys}
        image = soup.find('article', class_='details--left').find('img')['src']
        return dates_hours,self.base_url+image