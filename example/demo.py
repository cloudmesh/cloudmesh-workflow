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
<<<<<<< HEAD:example/demo.py
        print ('B START')
=======
        print 'B START'
>>>>>>> master:example/demo.py
        time.sleep(sleep_time)
        # print 'B STOP'

    @delayed()
    def C():
<<<<<<< HEAD:example/demo.py
        print ('C START')
=======
        print 'C START'
>>>>>>> master:example/demo.py
        time.sleep(sleep_time)
        # print 'C STOP'

    @delayed()
    def D():
<<<<<<< HEAD:example/demo.py
        print ('D START')
=======
        print 'D START'
>>>>>>> master:example/demo.py
        time.sleep(sleep_time)
        # print 'D STOP'

    @delayed()
    def F():
<<<<<<< HEAD:example/demo.py
        print ('F START')
=======
        print 'F START'
>>>>>>> master:example/demo.py
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
<<<<<<< HEAD:example/demo.py
    # nx.write_dot(H, '/tmp/test.dot')
=======
    #nx.write_dot(H, '/tmp/test.dot')
>>>>>>> master:example/demo.py
    data = {
        'file': "/tmp/example"
    }
    nx.drawing.nx_pydot.write_dot(H, '{file}.dot'.format(**data))
    dot2svg("{file}.dot".format(**data))
<<<<<<< HEAD:example/demo.py
    # os.system("open {file}.svg".format(**data))
    # browser("{file}.svg".format(**data))
=======
    #os.system("open {file}.svg".format(**data))
    browser("{file}.svg".format(**data))
>>>>>>> master:example/demo.py
test()

