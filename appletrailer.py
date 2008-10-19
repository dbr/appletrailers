import urllib
from BeautifulSoup import BeautifulSoup

class _Trailer(dict):
    def __init__(self, *args, **kwargs):
        self.__dict__.update( kwargs )
    
    def __repr__(self):
        return "<Trailer \"%s\">" % (self.__dict__['info'].title)

class _TrailerInfo:
    def __init__(self, *args, **kwargs):
        self.__dict__.update( kwargs )
    def __repr__(self):
        return "%s" % (self.__dict__)

class Trailers:
    def __init__(self, res = "720"):
        self.config = {}
        
        self.res_lookup = {
            "default" : "http://www.apple.com/trailers/home/xml/current.xml",
            "480" : "http://www.apple.com/trailers/home/xml/current_480p.xml",
            "720" : "http://www.apple.com/trailers/home/xml/current_720p.xml",
        }
        
        if not res in self.res_lookup:
            raise ValueError("Invalid resolution \"%s\". Select from: %s" % (
                res, ", ".join(self.res_lookup.keys())
            ))
        
        self.config['trailer_xml_url'] = self.res_lookup[res]
        
        self.all_movies = self.get_trailers()
    
    def __iter__(self):
        for trailer in self.all_movies:
            yield trailer
    
    def __repr__(self):
        return "<Trailers instance containing %s trailers>" % (len(self.all_movies))
    
    def search(self, search_term):
        for trailer in self.all_movies:
            if str(trailer.info.title).lower().find(search_term) > -1:
                return trailer
    
    def _get_source_soup(self, url):
        src = urllib.urlopen(url).read()
        soup = BeautifulSoup(src)
        return soup
    
    def _parse_list(self, insoup):
        ret = []
        if insoup is None:
            return ret
        for cmem in insoup:
            ret.append(cmem.string)
        return ret
    
    def _parse_dict(self, insoup):
        ret = {}
        for celement in insoup.findChildren():
            ret[str(celement.name)] = celement.string
        ti = _TrailerInfo(**ret)
        return ti
    
    def get_trailers(self):
        soup = self._get_source_soup(self.config['trailer_xml_url'])
        all_movies = []
        for movie in soup.findAll("movieinfo"):
            movie_info = {}
            movie_info['cast'] = self._parse_list(movie.cast)
            movie_info['info'] = self._parse_dict(movie.info)
            movie_info['genre'] = self._parse_list(movie.genre)
            movie_info['poster'] = self._parse_dict(movie.poster)
            movie_info['preview'] = self._parse_dict(movie.preview)
            t = _Trailer(**movie_info)
            all_movies.append(t)
        return all_movies
        

def main():
    """Simply lists"""
    all_trailers = Trailers(res = "720")
    for trailer in all_trailers:
        print "Title:", trailer.info.title
        print "Poster:", trailer.poster.location
        print "Actors:", ", ".join(trailer.cast)
        print "Trailer:", trailer.preview.large
        print "*"*24

if __name__ == '__main__':
    main()