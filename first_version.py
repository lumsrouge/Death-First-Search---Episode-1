import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Node:
    def __init__(self, dataval, index, linkedNodeList):
        self.isPass = dataval
        self.index = index
        self.linkedNodes = linkedNodeList
        self.visited = False
        self.priority = -1
    def addLink(self, newNode):
        self.linkedNodes.append(newNode)
    def removeLink(self, index):
        i = 0
        for node in self.linkedNodes:
            if node.index == index:
                self.linkedNodes.pop(i)
                return 0
            i = i + 1
    def mark(self):
        self.visited = True

def get_full_graph():

    # n: the total number of nodes in the level, including the gateways
    # l: the number of links
    # e: the number of exit gateways
    first_line = input().split()
    n, l, e = [int(i) for i in first_line]
    nodeList = []
    for i in range(n):
        nodeList.append(Node(False, i, []))
    for i in range(l):
        line = input().split()
        n1, n2 = [int(j) for j in line]
        nodeList[n1].addLink(nodeList[n2])
        nodeList[n2].addLink(nodeList[n1])
    for i in range(e):
        ei = int(input())  # the index of a gateway node
        nodeList[ei].isPass = True
    return nodeList

def debug(*arg):
    print(arg, file=sys.stderr, flush=True)


def breadth_first_search(nodeList, root):
    closestNodesList = []
    visited = []
    closestNodesList.append(nodeList[root])
    visited.append(nodeList[root])
    closestNodesList[0].mark()

    i = 0
    closestNodesList[0].priority = 0
    i = i + 1
    while closestNodesList:
        s = closestNodesList.pop(0)
        for neighbour in s.linkedNodes:
            if neighbour.visited == False:
                closestNodesList.append(neighbour)
                visited.append(neighbour)
                neighbour.mark()
                neighbour.priority = i
        i = i + 1
    return visited

def find_closest_gate(queue):
    i = 0
    for node in queue:
        if node.isPass:
            return(queue[i].index)
        i = i + 1
    debug("no gateway found")

def get_link_to_cut(gate_i, queue, si, node_list):
    for neighbour in node_list[gate_i].linkedNodes:
        if neighbour.priority < node_list[gate_i].priority:
            return neighbour.index

def cut_link(node_list, node_index, gate_index):
    node_list[node_index].removeLink(gate_index)
    node_list[gate_index].removeLink(node_index)
    print(f"{node_index} {gate_index}")

def reset_node_priority(node_list):
    for node in node_list:
        node.priority = -1
        node.visited = False

nodeList = get_full_graph()
# game loop
while True:
    si = int(input())
    queue = breadth_first_search(nodeList, si)
    gate_index = find_closest_gate(queue)
    node_index = get_link_to_cut(gate_index, queue, si, nodeList)
    cut_link(nodeList, node_index, gate_index)
    reset_node_priority(nodeList)
