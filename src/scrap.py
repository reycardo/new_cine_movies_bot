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

    def search_cine(self, keywords):
        """Searches for the cinema
        """
        response = requests.get(self.base_url+self.filmes_prefix+keywords+self.page_suffix)
        content = response.content
        soup = bs(content, 'html.parser')
        result_links = [[x for x in child.stripped_strings] for child in soup.find('article', class_ ='line').children]
        return result_links
      
    def search_film(self, keywords):
        """Searches for the film
        """
        response = requests.get(self.base_url+self.filmes_prefix+keywords+self.page_suffix)
        content = response.content
        soup = bs(content, 'html.parser')
        mydivs = soup.findAll("div", class_= 'cinema')
        result_links = [[x for x in child.stripped_strings] for child in soup.find('article', class_ ='line').children]
        #TODO fetch stuff correctly
        return result_links      


    def send_link(self, result_links, search_words): 
        send_link = set()
        for link in result_links:
            text = link.text.lower()
            if search_words in text:  
                send_link.add(link.get('href'))
        return send_link

cine = Cine_Movies()