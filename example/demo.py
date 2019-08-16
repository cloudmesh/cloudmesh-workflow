from cloudmesh.workflow.workflow import Graph
from cloudmesh.workflow.workflow import PythonTask
from cloudmesh.workflow.workflow import evaluate
from cloudmesh.common.Shell import Shell
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import time
import os

sleep_time = 1

def test():

    @PythonTask()
    def A():
        print ('A START')
        # for i in xrange(10):
        #     print 'A', i
        time.sleep(sleep_time)
        # print 'A STOP'

    @PythonTask()
    def B():
        print ('B START')
        time.sleep(sleep_time)
        # print 'B STOP'

    @PythonTask()
    def C():
        print ('C START')
        time.sleep(sleep_time)
        # print 'C STOP'

    @PythonTask()
    def D():
        print ('D START')
        time.sleep(sleep_time)
        # print 'D STOP'

    @PythonTask()
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
    #nx.write_dot(H, '/tmp/test.dot')
    data = {
        'file': "/tmp/example"
    }
    write_dot(H, '{file}.dot'.format(**data))
    Shell.dot2svg("{file}.dot".format(**data))
    #os.system("open {file}.svg".format(**data))
    Shell.browser("{file}.svg".format(**data))

test()

