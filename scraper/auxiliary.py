from bs4 import BeautifulSoup
import urllib2
import re


class FindMovieError(Exception):
        def __init__(self, title):
            self.title = title
        def _str__(self):
            return 'Movie scrape error: ' + self.title

class FindMatchError(Exception):
        def __init__(self, title):
            self.title = title
        def _str__(self):
            return 'Find Match Error On: ' + self.title

class Build(object):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', 'tt')
        self.imdbURL = ''


    def searchTitle(self, title):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 '
                                           '(KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')]
        search_term = title.replace(' ', '+').replace('_','+').replace('.','+')
        #print self.type
        url = 'http://www.imdb.com/find?q=%s&s=%s' % (search_term, self.type)
        f = opener.open(url)
        result = f.read()
        soup = BeautifulSoup(result)

        firstMatch = soup.find('table', 'findList').find('tr').find_all('td')[1]

        m = re.search('href="(.+?)">', str(firstMatch))

        if m:
            found = m.group(1)
            self.imdbURL = "http://www.imdb.com"+found

        else:
            raise FindMatchError(title)


    def getDetails(self):
        kwargs = {}
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 '
                                           '(KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')]
        f = opener.open(self.imdbURL)
        result = f.read()
        soup = BeautifulSoup(result)

        imdbtop = soup.find('td', id='overview-top')
        imdbbottom = soup.find('div', id='titleStoryLine')

        kwargs['title'] = soup.find(itemprop="name").get_text()
        kwargs['year'] = soup.find('span', 'nobr').get_text().replace('(', '').replace(')', '')
        kwargs['rating'] = imdbtop.find('span', attrs={'itemprop': 'ratingValue'}).get_text()
        kwargs['userrate'] = imdbtop.find('span', attrs={'itemprop': 'ratingCount'}).get_text()
        kwargs['outline'] = imdbtop.find(itemprop="description").get_text()
        kwargs['time'] = imdbtop.find(itemprop='duration').get_text().replace('\n', '').replace(' ', '')
        kwargs['director'] = imdbtop.find_all('span', itemprop='name')[1].get_text()
        kwargs['votes'] = imdbtop.find('span', itemprop='ratingCount').get_text()
        temp_string = imdbtop.find('a', attrs={'title': 'See all release dates'}).get_text()
        kwargs['premiered'] = temp_string[:temp_string.index('\n')]
        kwargs['country'] = temp_string[temp_string.index('\n'):].replace('\n', '').replace('(', '').replace(')', '')

        kwargs['mpaa'] = imdbbottom.find('span', itemprop='contentRating').get_text()
        kwargs['plot'] = imdbbottom.find('div', attrs={'class': 'inline canwrap'}).find('p').get_text()
        cast = soup.find('table', 'cast_list')
        cast_names = []
        cast_character = []
        cast_stars = []
        genres = []

        for item in imdbtop.find('div', attrs={'itemprop': 'actors'}):
            try:
                actors = item.find('span', itemprop='name').get_text()
                cast_stars.append(actors)
            except:
                pass

        for item in cast.find_all('tr'):
            try:
                cast_name = item.find('td', attrs={'class': 'itemprop'}).get_text().replace('\n', '')
                cast_character = item.find('td', attrs={'class': 'character'}).get_text().replace('\n', '').replace(' ', '')
                cast_names.append(cast_name)
                cast_names.append(cast_character)
            except:
                pass

        for item in imdbbottom.find('div', attrs={'itemprop': 'genre'}).find_all('a'):
            try:
                genres.append(item.get_text())
            except:
                pass

        kwargs['name'] = cast_names
        kwargs['role'] = cast_character
        kwargs['stars'] = cast_stars
        kwargs['genres'] = genres

        return kwargs