from .models import *


def insert_relation_node_data(Relations):
    graph_nodes_temp  = ['s','a','b','c','d','e','g']
    for (x,y) in Relations:
        # print (x,y)

        b  = Node_Relations(source = graph_nodes_temp.index(x),target=graph_nodes_temp.index(y))
        b.save()
def __init__insert_node_data():
    graph_nodes_temp  = ['s','a','b','c','d','e','g']
    for a in graph_nodes_temp:
        print (a)
        b = Node_Data(name = a,group=1)
        b.save()
def update_data_node(executed_nodes,l,remaining_nodes):
    for exec in executed_nodes:
        b = Node_Data(name=exec,group=3)
        b.save()
    for curr in l:
        b = Node_Data(name=curr,group=2)
        b.save()


def deleteAllentries(flag):
    if flag:
        Node_Relations.objects.all().delete()
    else:
        Node_Data.objects.all().delete()


def database_init(Relations):
    deleteAllentries(True)
    insert_relation_node_data(Relations)
    deleteAllentries(False)
    __init__insert_node_data()




