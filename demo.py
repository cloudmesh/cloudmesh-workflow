from cloudmesh_workflow.workflow import Graph
from cloudmesh_workflow.workflow import delayed
import networkx as nx

def test():

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
