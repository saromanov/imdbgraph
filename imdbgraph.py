from imdbpie import Imdb
import networkx as nx


class IMDBGraph:
    def __init__(self, anonymize=True):
        self._imdb = Imdb(anonymize=anonymize, cache=True)
        self._graph = nx.Graph()

    def _add_node(self, name, nodetype):
        ''' Add simple node without attributes
        '''
        if name not in self._graph.nodes():
            self._graph.add_node(name, nodetype=nodetype)

    def addPerson(self, idname):
        ''' add New actor/actress no the graph
        '''
        actor = self._imdb.get_person_by_id(idname)
        self._graph.add_node(actor.name)

    def addMovie(self, idname):
        movie = self._imdb.get_title_by_id(idname)
        self._add_node(movie.title, 'movie')
        self._add_node(movie.year, 'year')
        print(movie.tagline, movie.rating,  movie.cast_summary)
        for genre in movie.genres:
            self._add_node(genre, 'genre')
            self._graph.add_edge(movie.title, genre)
        for person in movie.credits:
            self._add_node(person.name, 'actor')
            self._graph.add_edge(movie.title, person.name, weight=movie.rating + movie.votes)
        for person in movie.cast_summary:
            self._add_node(person.name, "actor")
            self._graph.add_edge(movie.title, person.name)

    def addPopular(self, limit=10):
        ''' Add popular movies and shows
        '''
        shows = self._imdb.popular_shows()
        #movies = self._imdb.top_250()
        if limit > len(shows):
            limit = len(shows)
        for show in shows[:limit]:
            self.addMovie(show['tconst'])

    def save(self, outpath):
        ''' save graph to the file
        '''
        pass
