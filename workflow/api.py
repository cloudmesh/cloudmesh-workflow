
from __future__ import absolute_import

import traits.api as T
from traits.api import HasTraits

import networkx as nx
import time
import uuid
from functools import wraps
from concurrent import futures
from multiprocessing import cpu_count
from collections import OrderedDict

class Graph(nx.DiGraph):
    """A NetworkX DiGraph where the ordering of edges/nodes is
    preserved"""

    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict


TExecutor = T.Trait(futures.Executor)


def nodeid(): return uuid.uuid4()


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



def evaluate(graph):

    s = nx.topological_sort(graph)[0]
    node = graph.node[s]['node']
    return node.eval()


class Node(HasTraits):

    id = T.Trait(uuid.UUID)
    graph = T.Trait(Graph)
    executor = T.Trait(futures.ThreadPoolExecutor)
    timeout = T.Any()
    f = T.Function()
    name = T.String()
    result = T.Trait(futures.Future)
    
    def __init__(self, (f, args, kws), graph=None, executor=None,
                 timeout=None, type=None):
        self.id = nodeid()
        self.f = f
        self._args = args
        self._kws = kws
        self.name = f.func_name
        self.graph = graph
        self.executor = executor or futures.ThreadPoolExecutor(cpu_count())
        self.timeout = timeout


    @property
    def children_iter(self):
        edges = set(self.graph.edges())
        for i in self.graph.successors_iter(self.id):
            child = self.graph.node[i]['node']
            assert (self.id, i) in edges
            yield child

    @property
    def children(self):
        return list(self.children_iter)


    def start(self):
        if self.result is None:
            self.result = self.executor.submit(self.f, *self._args, **self._kws)
        else:
            # already started
            pass


    def wait(self):
        self.result.result(self.timeout)


    def eval(self):
        self.start()
        self.wait()


    def compose(self, other, MkOpNode):

        assert self.graph is not None
        assert other.graph is not None
        assert self.graph == other.graph
        G = self.graph

        # print self.name, operator, other.name

        s, t = self.id, other.id
        other.id = t
        op = MkOpNode(graph=G)
        G.add_node(op.id, node=op, label=op.name)
        G.add_node(s, node=self, label=self.name)
        G.add_node(t, node=other, label=other.name)
        G.add_edge(op.id, s)
        G.add_edge(op.id, t)

        return op


    def __and__(self, other):
        return self.compose(other, AndNode)


    def __or__(self, other):
        return self.compose(other, OrNode)



class OpNode(Node):

    def __init__(self, **kwargs):
        n = self.name
        super(OpNode, self).__init__((lambda: None, (), {}), **kwargs)
        self.name = n

class AndNode(OpNode):

    name = T.String('&')

    def start(self):
        for child in self.children_iter:
            child.start()
            break


    def wait(self):
        self.result = futures.Future()
        for child in self.children_iter:
            child.start()
            child.wait()
        self.result.set_result(None)


class OrNode(OpNode):

    name = T.String('|')

    def start(self):
        for child in self.children_iter:
            child.start()

    def wait(self):
        for child in self.children_iter:
            child.wait()


G = Graph()

@delayed(G)
def A():
    print 'A START'
    # for i in xrange(10):
    #     print 'A', i
    time.sleep(3)
    # print 'A STOP'

@delayed(G)
def B():
    print 'B START'
    time.sleep(3)
    # print 'B STOP'

@delayed(G)
def C():
    print 'C START'
    time.sleep(3)
    # print 'C STOP'

@delayed(G)
def D():
    print 'D START'
    time.sleep(3)
    # print 'D STOP'

@delayed(G)
def F():
    print 'F START'
    time.sleep(3)
    # print 'F STOP'


def clean(G):
    H = G.copy() # nx.convert_node_labels_to_integers(G)
    N = {}
    E = {}

    for n in H.nodes():
        node = H.node[n]['node']
        del H.node[n]['node']
        N[n] = node.name

        # for s,t,data in H.out_edges([n], data=True):
        #     E[s,t] = data['type']

    return H, N, E

def test():
    # A() | B() | C()
    # A() & B() | C()
    # A() | (B() & C())
    # ((A() & B()) | C()) & (D() | F())
    (A() | B() | C()) & (D() | F())

    H, N, E = clean(G)


    evaluate(G)

    # O = Graph()
    # order = nx.topological_sort(H)
    # s = order[0]
    # O.add_node(s, label=G.node[s]['label'])
    # for t in order[1:]:
    #     O.add_node(t, label=G.node[t]['label'])
    #     O.add_edge(s, t)
    #     s = t

    # p = nx.spring_layout(H)
    # nx.draw_networkx(H, p, with_labels=False)
    # nx.draw_networkx_labels(H, p, N)
    # nx.draw_networkx_edge_labels(H, p, edge_labels=E)
    # import matplotlib.pyplot as plt
    # plt.savefig('/tmp/test.png')

    nx.write_dot(H, '/tmp/test.dot')
    # nx.write_dot(O, '/tmp/testo.dot')

test()
