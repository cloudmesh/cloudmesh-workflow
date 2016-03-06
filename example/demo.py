from __future__ import print_function
from cloudmesh_workflow.workflow import Graph
from cloudmesh_workflow.workflow import delayed
from cloudmesh_workflow.workflow import evaluate
from cloudmesh_workflow.util import dot2svg, browser
import networkx as nx
import time
import os

sleep_time = 1

def test():

    @delayed()
    def A():
        print ('A START')
        # for i in xrange(10):
        #     print 'A', i
        time.sleep(sleep_time)
        # print 'A STOP'

    @delayed()
    def B():
        print ('B START')
        time.sleep(sleep_time)
        # print 'B STOP'

    @delayed()
    def C():
        print ('C START')
        time.sleep(sleep_time)
        # print 'C STOP'

    @delayed()
    def D():
        print ('D START')
        time.sleep(sleep_time)
        # print 'D STOP'

    @delayed()
    def F():
        print ('F START')
        time.sleep(sleep_time)
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


    # node = ( A() | B() | C() )
    # node = ( A() & B() | C() )
    # node = ( A() | (B() & C()) )
    # node = ( ((A() & B()) | C()) & (D() | F()) )
    node = (A() | B() | C()) & (D() | F())

    G = node.graph
    H, N, E = clean(G)
    evaluate(G)
    # nx.write_dot(H, '/tmp/test.dot')
    data = {
        'file': "/tmp/example"
    }
    nx.drawing.nx_pydot.write_dot(H, '{file}.dot'.format(**data))
    dot2svg("{file}.dot".format(**data))
    # os.system("open {file}.svg".format(**data))
    # browser("{file}.svg".format(**data))

if __name__ == "__main__":
    test()

