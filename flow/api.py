
import networkx as nx
import time
from functools import wraps
from concurrent import futures
from multiprocessing import cpu_count

_DEFAULT_EXECUTOR = futures.ThreadPoolExecutor(cpu_count())
_FLOW_NAMESPACE = None

def namespace_clear():
    global _FLOW_NAMESPACE
    _FLOW_NAMESPACE = dict()

def namespace_init(name):
    global _FLOW_NAMESPACE
    _FLOW_NAMESPACE[name] = nx.DiGraph()

def namespace_use(name):
    global _FLOW_NAMESPACE
    if name not in _FLOW_NAMESPACE:
        namespace_init(name)

def namespace_get(name):
    global _FLOW_NAMESPACE
    return _FLOW_NAMESPACE[name]

class task(object):
    def __init__(self, namespace='.', executor=None):
        namespace_use(namespace)
        self._namespace = namespace
        self._G = namespace_get(namespace)

        global  _DEFAULT_EXECUTOR
        self._executor = executor or _DEFAULT_EXECUTOR

    @property
    def namespace(self): return self._namespace

    @property
    def G(self): return self._G

    @property
    def executor(self): return self._executor

    def __call__(self, fn):

        @wraps(fn)
        def work(*args, **kwargs):

            f = self.executor.submit(fn, *args, **kwargs)
            self.G.add_node(fn.func_name, future=f)
            return f

        return work

namespace_clear()

@task()
def A():
    for i in xrange(4):
        # print 'A', i
        time.sleep(5)

@task()
def B():
    for i in xrange(3):
        # print 'B', i
        time.sleep(2)


def main():
    # g = namespace_get('.')
    # g.add_node('START')
    # g.add_edge('START', 'A')
    # g.add_edge('START', 'B')
    A()
    B()

main()
g = namespace_get('.')

while True:
    for n in g.nodes():
        print n, g.node[n]['future'].done()
    if all(map(lambda n: g.node[n]['future'].done(), g.nodes())):
        break
    else:
        time.sleep(2)
        print
