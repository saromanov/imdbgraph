from imdbpie import Imdb
import networkx as nx


class IMDBGraph:
    def __init__(self, anonymize=True):
        self._imdb = Imdb(anonymize=anonymize, cache=True)
        self._graph = nx.Graph()

    def _add_node(self, name):
        ''' Add simple node without attributes
        '''
        if name not in self._graph.nodes():
            self._graph.add_node(name)

    def addPerson(self, idname):
        ''' add New actor/actress no the graph
        '''
        actor = self._imdb.get_person_by_id(idname)
        self._graph.add_node(actor.name)

    def addMovie(self, idname):
        movie = self._imdb.get_title_by_id(idname)
        self._add_node(movie.title)
        self._add_node(movie.year)
        for genre in movie.genres:
            self._add_node(genre)
            self._graph.add_edge(movie.title, genre)

    def addPopular(self):
        ''' Add popular movies and shows
        '''
        shows = self._imdb.popular_shows()
        movies = self._imdb.top_250()

    def save(self, outpath):
        ''' save graph to the file
        '''
        pass
