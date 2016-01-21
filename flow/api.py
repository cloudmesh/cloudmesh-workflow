
from __future__ import absolute_import

import traits.api as T
from traits.api import HasTraits

import networkx as nx
import time
from functools import wraps
from concurrent import futures
from multiprocessing import cpu_count


Graph = nx.DiGraph

DiGraphT = T.Trait(nx.DiGraph)
ExecutorT = T.Trait(futures.Executor)


class Task(HasTraits):
    G = DiGraphT()
    executor = ExecutorT()
    name = T.String()

    def __init__(self, fn, graph=None, executor=None):
        self.function = fn
        self.name = fn.func_name

        if graph is not None:
            self.G = graph

        if executor is not None:
            self.executor = executor
    
    def __call__(self, *args, **kwargs):
        future = self.executor.submit(self.function, *args, **kwargs)
        self.G.add_node(self.function.func_name, future=future)
        return future


    def __add__(self, other):
        assert self.G is not None
        other.G = self.G
        return other

    def __and__(self, other):

        # self.G and other.G reference the same object
        G = self.G

        # create a boundary
        if self.name != '--BOUNDARY--' and other.name != '--BOUNDARY--':
            b = boundary(G)
            G.add_edge(self.function, b.function)
            G.add_edge(other.function, b.function)
            return b

        # merge boundaries
        elif self.name == '--BOUNDARY--' and other.name == '--BOUNDARY--':
            incomming = G.predecessors(other.function)
            G.remove_node(other.function)
            for n in incomming:
                G.add_edge(n, self.function)
            return self

        # either self or other is a boundary
        else:
            b = self if self.name == '--BOUNDARY--' else other
            o = self if self.name != '--BOUNDARY--' else other
            assert b.name == '--BOUNDARY--', b.name
            assert o.name != '--BOUNDARY--', o.name
            G.add_edge(o.function, b.function)
            return b



def boundary(graph):
    def _boundary(): return
    t = Task(_boundary, graph=graph)
    t.name = '--BOUNDARY--'
    return t


def inject(graph, task, **kws):
    task.G = graph
    return task


def task(fn):
    return Task(fn)


@task
def A():
    for i in xrange(4):
        # print 'A', i
        time.sleep(5)

@task
def B():
    for i in xrange(3):
        # print 'B', i
        time.sleep(2)

@task
def C():
    for i in xrange(2):
        time.sleep(4)


def main():
    # g = namespace_get('.')
    # g.add_node('START')
    # g.add_edge('START', 'A')
    # g.add_edge('START', 'B')
    A()
    B()


# main()

# while True:
#     for n in G.nodes():
#         print n, G.node[n]['future'].done()
#     if all(map(lambda n: G.node[n]['future'].done(), G.nodes())):
#         break
#     else:
#         time.sleep(2)
#         print


G = nx.DiGraph()
