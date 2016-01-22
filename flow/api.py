
from __future__ import absolute_import

import traits.api as T
from traits.api import HasTraits

import networkx as nx
import time
import uuid
from functools import wraps
from concurrent import futures
from multiprocessing import cpu_count


Graph = nx.DiGraph

TDiGraph = T.Trait(nx.DiGraph)
TExecutor = T.Trait(futures.Executor)


def nodeid(): return uuid.uuid4()


class Edge:
    AND = 'AND'
    OR = 'OR'


class Node(HasTraits):

    id = T.Trait(uuid.UUID)
    graph = T.Trait(Graph)
    executor = T.Trait(futures.ThreadPoolExecutor)
    timeout = T.Any()
    f = T.Function()
    result = T.Trait(futures.Future)
    
    def __init__(self, (f, args, kws), graph=None, executor=None, timeout=None):
        self.id = nodeid()
        self.f = f
        self._args = args
        self._kws = kws
        self.graph = graph
        self.executor = executor or futures.ThreadPoolExecutor(cpu_count())
        self.timeout = timeout


    def start(self):
        if self.result is None:
            self.result = self.executor.submit(self.f, *self._args, **self._kws)
        else:
            # already started
            pass


    def combine(self, other, edge):

        assert self.graph == other.graph
        G = self.graph

        s, t = self.id, nodeid()
        other.id = t
        G.add_node(s, node=self)
        G.add_node(t, node=other)
        G.add_edge(s, t, type=edge)

        # self.start()
        # other.start()

        return other


    def __and__(self, other):
        return self.combine(other, Edge.AND)


    def __or__(self, other):
        return self.combine(other, Edge.OR)


class delayed(object):
    def __init__(self, G, **kws):
        self.G = G
        self.kws = kws

    def __call__(self, f):

        @wraps(f)
        def g(*args, **kwargs):
            return Node((f, args, kwargs),
                        graph=self.G,
                        **self.kws)

        return g



G = Graph()

@delayed(G)
def A():
    # for i in xrange(10):
    #     print 'A', i
    time.sleep(1)

@delayed(G)
def B():
    time.sleep(2)

@delayed(G)
def C():
    time.sleep(3)


def clean(G):
    H = nx.convert_node_labels_to_integers(G)
    N = {}
    E = {}

    for n in H.nodes():
        node = H.node[n]['node']
        del H.node[n]['node']
        N[n] = node.f.func_name

        for s,t,data in H.out_edges([n], data=True):
            E[s,t] = data['type']

    return H, N, E

def test():
    A() | (B() & C())
    H, N, E = clean(G)

    p = nx.spring_layout(H)
    nx.draw_networkx(H, p, with_labels=False)
    nx.draw_networkx_labels(H, p, N)
    nx.draw_networkx_edge_labels(H, p, edge_labels=E)
    import matplotlib.pyplot as plt
    plt.savefig('/tmp/test.png')

    # nx.write_dot(H, '/tmp/test.dot')

test()
