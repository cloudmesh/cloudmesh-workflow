from DjangoApp.stack_list import *
import os
import datetime
from networkx import nx
from threading import Thread
from collections import OrderedDict
import concurrent
from concurrent import futures
from .models import *
from DjangoApp.dbqueries import *
import time

from WorkFlowDjango.settings import *


class Graph(nx.DiGraph):
    """A NetworkX :func:`networkx.DiGraph` where the ordering of edges/nodes is
    preserved
    """
    # print ("inside Grapddh")
    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict

COMMOM_MAP = []
sleep_time = 4
Nodes = []



def S():
    print("EXECUTION STARTED")
def A():
    # i = datetime.datetime.now()
    print ("A START --> Current date & time = %s" % datetime.datetime.now())
    # print ('A START')
    # for i in xrange(10):
    #     print 'A', i
    time.sleep(sleep_time)
    print ("A STOP --> Current date & time = %s" % datetime.datetime.now())
    # print ('A STOP')

def B():
    print ("B START -->  Current date & time = %s" % datetime.datetime.now())
    # print ('B START')
    time.sleep(sleep_time+1)
    print ("B STOP --> Current date & time = %s" % datetime.datetime.now())
    # print ('B STOP')

def C():
    print ("C START --> Current date & time = %s" % datetime.datetime.now())
    # print ('C START')
    time.sleep(sleep_time)
    # print 'C STOP'
    print ("C STOP --> Current date & time = %s" % datetime.datetime.now())
def D():
    print ("D START --> Current date & time = %s" % datetime.datetime.now())
    time.sleep(sleep_time)
    print ("D STOP --> Current date & time = %s" % datetime.datetime.now())


def G():
    print ("G START --> Current date & time = %s" % datetime.datetime.now())
    time.sleep(sleep_time)
    print ("G STOP --> Current date & time = %s" % datetime.datetime.now())

def E():
    print ("E START --> Current date & time = %s" % datetime.datetime.now())
    time.sleep(sleep_time)
    print ("E STOP --> Current date & time = %s" % datetime.datetime.now())

def dot2svg(filename, engine='dot'):
    data = {
        'engine': engine,
        'file': filename.replace(".dot", "")
    }
    command = "{engine} -Tsvg {file}.dot > {file}.svg".format(**data)
    print(command)
    os.system(command)

def calmeth(func,timer):
    c = func.upper()
    eval(c+'()')
    # print(func)

def postpone():
    t = Thread(target = foo, args=("a","n"))
    t.daemon = False
    t.start()

# @postpone
def foo(x,y):
    # print (x,y)
    draw_graph(COMMOM_MAP,Nodes)
    print (Nodes)


def tryparrallel(func):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executer:
        futures = [executer.submit(calmeth,a_var,"10") for a_var in func]
        results = concurrent.futures.wait( futures )


def parse_string(char,str):
    # print "hi"
    s_operator = Stack()
    s_operand = Stack()
    print (str)
    i =0
    list1 =[]
    list1.append(char)
    while i < (len(str)):
        # print i
        k=0
        if str[i] == '(':
            # print "started"
            list2 = list1
            if s_operand.isNotEmpty() and s_operator.isNotEmpty():
                list2 = []
                # print list2," : list2 : ",list1
                list2 = pop_check(s_operator,s_operand,list1)
                # print list2," : after pop_check : "
                if s_operand.pop() == '|':
                    list2 = list1
            k = i
            while str[k]!=')':
                k+=1
            list1 = graph_generate(list2,str[i+1:k])
            s_operator = Stack();
            s_operand = Stack();
            # print (list1,"hello")
            i=k

        elif str[i] != '|' and str[i] != ';':
            s_operator.push(str[i])
        else:
            # print ""
            s_operand.push(str[i])
        i+=1

##########################outside While loop
    if s_operand.isNotEmpty() or s_operator.isNotEmpty():
        print (pop_check(s_operator,s_operand,list1))
    return COMMOM_MAP

def pop_check(s_operator,s_operand,list1):
    return_list = []
    operator_str = s_operand.pop()
    if operator_str == "|":
        # print "pd"
        while s_operator.isEmpty() != True:

            node = s_operator.pop()
            for k in list1:
                return_list.append(node)
                COMMOM_MAP.append((k,node))
                # print (k,node,"in Pop check")
    else:
        # print "sd"
        counter =0
        while s_operator.isEmpty() != True:
            stack_size = s_operator.size()
            child_pop = s_operator.pop()

            if counter==0:
                return_list.append(child_pop)
            counter+=1
            if stack_size !=1:
                parent_pop = s_operator.pop()
                if stack_size>2:
                    # print (parent_pop,child_pop)
                    s_operator.push(parent_pop)
                else:
                    print (parent_pop,child_pop)
                    for k_seq in list1:
                        # print (k_seq,parent_pop)
                        COMMOM_MAP.append((k_seq,parent_pop))
            else:
                for k_seq in list1:
                    # print (k_seq,child_pop)
                    COMMOM_MAP.append((k_seq,child_pop))

    return return_list

def graph_generate(x,y):
    # print("Asd")
    # print y
    # print x
    index = 0
    s= Stack();
    s1 = Stack();
    temp_char = ''
    temp_list = []
    while index < len(y):
        if y[index] != '|' and y[index] != ';':
            s.push(y[index])

        else:
            s1.push(y[index])
            temp_char = y[index]
        index +=1
    # print s1.size()
    temp_list = pop_check(s,s1,x)
    if temp_char == ';':
        temp_list = x
    return temp_list

def draw_graph(node_ends,graph_nodes):
    G = Graph()
    # graph_nodes  = ['s','a','b','c','d','e','f','g']
    executed_nodes = []
    # print (graph_nodes)
    print ("******************")
    # print (Nodes)
    remaining_nodes = graph_nodes
    print(remaining_nodes)
    print("%%%%%%%%%%")
    G.add_nodes_from(graph_nodes, color = 'Red')
    G.add_edges_from(node_ends,dir="forward")
    writedotfile(G)
    k = 's'
    l = []
    tryparrallel(k)
    executed_nodes.append(k)
    remaining_nodes.remove(k)
    while G.successors_iter(k) != None:
        # print(k)
        l = G.successors(k)
        if len(l)==0:
            generate_graph_anime(executed_nodes,l,remaining_nodes,node_ends)
            print (" EXECUTION STOPPED ")
            break
        tryparrallel(l)
        for y in l:
            # print (y)
            executed_nodes.append(y)

        for x in l:
            # print(x +"in remove nodes")
            remaining_nodes.remove(x)
        # remaining_nodes.remove(x for x in l)
        print (executed_nodes,l,remaining_nodes,node_ends)
        # update_data_node(executed_nodes,l,remaining_nodes)
        generate_graph_anime(executed_nodes,l,remaining_nodes,node_ends)
        k = l[0]

def writedotfile(G):
    # nx.draw(G)
    data = {
        'file': STATICFILES_DIRS[0]+"\workflow\\test"
    }
    # print (STATICFILES_DIRS[0])
    # print ("^^^^^^^")

    # print (WORKFLOW_DIR[0])

    nx.drawing.nx_pydot.write_dot(G, '{file}.dot'.format(**data))
    command = "dot -Tsvg {file}.dot > {file}.svg".format(**data)
    print(command)
    os.system(command)
    # dot2svg("{file}.dot".format(**data))

def generate_graph_anime(temp_graph_nodes,current_nodes,remaining_nodes,node_ends):
    # print("inside main metd")
    # print (temp_graph_nodes)
    G = Graph()
    G.add_nodes_from(temp_graph_nodes, color = 'Red')
    G.add_nodes_from(current_nodes, color = 'green')
    G.add_nodes_from(remaining_nodes, color = 'blue')

    G.add_edges_from(node_ends,dir="forward")
    writedotfile(G)
    input("wait to check dot file")


# if __name__ == '__main__':
def entry_point(str):
    # str = input()
    COMMOM_MAP = []
    ret = []
    ret = parse_string('s',str )
    print (str)
    global Nodes
    Nodes = ['s']
    for i in str:
        if i == '(' or i == ')' or i == '|' or i == ';' or i==' ':
            x = 0
        else:
            Nodes.append(i)
    # print ("%%%%%%%%%%")
    print (Nodes)

    # str = str.replace(')',' ').replace('(',' ').replace('|',' ').replace(';',' ').replace('  ',' ').split(' ')
    # print("In Pyparse")
    # print(ret)
    # database_init(ret)
    # draw_graph(COMMOM_MAP)
    postpone()
    print ("***********************")
    print(ret)

