from imdbpie import Imdb
import networkx as nx
import logging

logging.basicConfig(level = logging.INFO)

class IMDBGraph:
    def __init__(self, anonymize=True):
        self._imdb = Imdb(anonymize=anonymize, cache=True)
        self._graph = nx.Graph()

    def _add_node(self, name, nodetype):
        ''' Add simple node without attributes
        '''
        if name not in self._graph.nodes():
            self._graph.add_node(name, node=nodetype)

    def addPerson(self, idname):
        ''' add New actor/actress no the graph
        '''
        actor = self._imdb.get_person_by_id(idname)
        self._graph.add_node(actor.name)

    def addMovie(self, idname):
        movie = self._imdb.get_title_by_id(idname)
        self._add_node(movie.title, 'movie')
        self._add_node(movie.year, 'year')
        logging.info("Loading {0}".format(idname))
        for genre in movie.genres:
            self._add_node(genre, 'genre')
            self._graph.add_edge(movie.title, genre)
        for person in movie.credits:
            self._add_node(person.name, 'actor')
            self._graph.add_edge(movie.title, person.name, weight=movie.rating + movie.votes, rating=movie.rating, votes=movie.votes)
        for person in movie.cast_summary:
            self._add_node(person.name, "actor")
            self._graph.add_edge(movie.title, person.name)

    def addPopular(self, limit=2):
        ''' Add popular movies and shows
        '''
        shows = self._imdb.popular_shows()
        #movies = self._imdb.top_250()
        if limit > len(shows):
            limit = len(shows)
        for show in shows[:limit]:
            self.addMovie(show['tconst'])

    def addEdge(self, innode, outnode, prop=None):
        if innode not in self._graph:
            raise Exception("{0} not in graph".format(innode))
        if outnode not in self._graph:
            raise Exception("{0} not in graph".format(outnode))
        self._graph.add_edge(innode,outnode, prop=prop)

    def components(self):
        comp = nx.connected_components(self._graph)
        degree = nx.degree(self._graph)
        print(nx.is_connected(self._graph))
        print(nx.stoer_wagner(self._graph))
        #print(nx.k_components(self._graph))
        #print(nx.clustering(self._graph))

    def avg_degree(self):
        ''' Return average number of degree for each node
        '''
        return nx.average_neighbor_degree(self._graph)

    def avg_degree_connectivity(self):
        return nx.average_degree_connectivity(self._graph)

    def clustering(self):
        ''' Compute a bipartite clustering coefficient for nodes.
        '''
        return nx.clustering(self._graph)

    def get_item(self, item):
        ''' Getting node from the graph
        '''
        return self._graph[item]

    def cliques(self):
        ''' return all cluques from the graph
        '''
        return nx.find_cliques(self._graph)

    def save(self, outpath):
        ''' save graph to the file
        '''
        pass
