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

def get_full_graph(gate_list):
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
        gate_list.append(nodeList[ei])
    return nodeList

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

def get_path_to_bobnet(gate, bobnet):
    one_path = []
    current_node = gate
    one_path.append(gate)
    while current_node is not bobnet and current_node.priority != -1:
        for neighbour in current_node.linkedNodes:
            if (neighbour.priority < current_node.priority):
                one_path.append(neighbour)
                current_node = neighbour
    return one_path

def select_paths(paths): #pb here
    i = 0
    current_length = -1
    selected_index = 0
    for path in paths:
        if (len(path) < current_length and len(path) > 1) or current_length == -1:
            selected_index = i
            current_length = len(path)
        i = i + 1
    return (paths[selected_index])

def get_other_link_to_cut(gate_list, queue, si, node_list):
    paths = []
    for gate in gate_list:
        new_path = get_path_to_bobnet(gate, node_list[si])
        paths.append(new_path)
    path_selected = select_paths(paths)
    return path_selected[-2].index

def alternative_cut_link(node_list, node_index, si):
    node_list[node_index].removeLink(si)
    node_list[si].removeLink(node_index)
    print(f"{node_index} {si}")

def reset_node_priority(node_list):
    for node in node_list:
        node.priority = -1
        node.visited = False

gate_list = []
nodeList = get_full_graph(gate_list)
while True:
    si = int(input())
    queue = breadth_first_search(nodeList, si)
    gate_index = find_closest_gate(queue)
    node_index = get_other_link_to_cut(gate_list, queue, si, nodeList)
    alternative_cut_link(nodeList, node_index, si)
    reset_node_priority(nodeList)
