#
# Copyright 2016 Badi' Abdul-Wahid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Author: Badi' Abdul-Wahid <badi@iu.edu>
# Organization: Indiana University / FutureSystems
#


"""\n
Description
===========

This module provides an api for building a workflow graph of labeled
functions which can then be evaluated. Nodes connected with a desired
ordering or run sequentially, others can be run in parallel.

Syntax is inspired by the parallel (||) and sequential (;) operators.
For example:

::

  (A || B) ; (C || D)

means that A and B can be evaluated in parallel, and likewise C and D,
but both A and B must be completed before C or D may begin.

The python implementation overrides the bitwise **OR** (|) and **AND**
(&) operators to provide a similar syntactic feel. The example above
should be defined as such:

::

  (A() | B()) & (C() | D())

.. note::

  The python operator precedence for ``|`` and ``&`` is unchanged:
  ``&`` has higher precedence than ``|``.

Usage
=====

The first part is to mark top-level functions as ``delayed()``.  The
``delayed()`` decoration wraps the function so that calling the
function inserts the node, without applying the parameters, into the
call graph. You can access the ``graph`` property of any node to get
the current call graph.

For instance

.. code-block :: python

  @delayed()
  def A(x): print x*2

  @delayed()
  def B(x, y): return x ** y

  def main():
    node = A(24) | B(40, 2)


Once the graph has been built, it must be explicitly evaluated

.. code-block :: python

  evaluate(node.graph)


"""



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


__all__ = [
    'delayed', 'evaluate',
    'Node', 'OpNode', 'AndNode', 'OrNode', 'Graph',
]

class Graph(nx.DiGraph):
    """A NetworkX DiGraph where the ordering of edges/nodes is
    preserved"""

    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict


TExecutor = T.Trait(futures.Executor)


def nodeid(): return uuid.uuid4()


class delayed(object):
    def __init__(self, graph=None, **kws):
        self.G = graph
        self.kws = kws

    def __call__(self, f):

        @wraps(f)
        def g(*args, **kwargs):
            return Node((f, args, kwargs),
                        graph=self.G,
                        **self.kws)

        return g


def find_root_node(graph):
    """Graph -> Node"""

    i = nx.topological_sort(graph)[0]
    n = graph.node[i]['node']
    return n


def evaluate(graph):

    node = find_root_node(graph)
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


    def _init_graph(self, graph=None):
        if self.graph is None and graph is None:
            self.graph = Graph()

        elif self.graph is None and graph is not None:
            self.graph = graph


    def _merge_graph(self, other):
        if not self.graph == other.graph:
            for s, t, data in other.graph.edges_iter(data=True):
                sn = other.graph.node[s]
                tn = other.graph.node[t]
                self.graph.add_node(s, sn)
                self.graph.add_node(t, tn)
                self.graph.add_edge(s, t, data)
            other.graph = self.graph


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


        self._init_graph()
        other._init_graph(self.graph)
        self._merge_graph(other)

        assert self.graph is not None, self.name
        assert other.graph is not None, other.name
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


@delayed()
def A():
    print 'A START'
    # for i in xrange(10):
    #     print 'A', i
    time.sleep(3)
    # print 'A STOP'

@delayed()
def B():
    print 'B START'
    time.sleep(3)
    # print 'B STOP'

@delayed()
def C():
    print 'C START'
    time.sleep(3)
    # print 'C STOP'

@delayed()
def D():
    print 'D START'
    time.sleep(3)
    # print 'D STOP'

@delayed()
def F():
    print 'F START'
    time.sleep(3)
    # print 'F STOP'


def clean(G):
    H = G.copy()
    N = {}
    E = {}

    for n in H.nodes():
        node = H.node[n]['node']
        del H.node[n]['node']
        N[n] = node.name


    return H, N, E

def test():
    # node = ( A() | B() | C() )
    # node = ( A() & B() | C() )
    # node = ( A() | (B() & C()) )
    # node = ( ((A() & B()) | C()) & (D() | F()) )
    node = (A() | B() | C()) & (D() | F())

    G = node.graph
    H, N, E = clean(G)
    evaluate(G)
    nx.write_dot(H, '/tmp/test.dot')

test()
