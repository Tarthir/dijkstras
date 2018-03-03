#!/usr/bin/python3


from CS312Graph import *
import time

#Return the correct type of queue
def makeQueue(use_heap):
    return MyHeapQueue() if use_heap else UnsortedArrayQueue()


class NetworkRoutingSolver:
    def __init__( self, display ):
        pass



    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network


    # get the path after dijkstra;s is run
    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0

        node = self.network.nodes[self.source]
        edges_left = 3

        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length

            node = edge.dest
            edges_left -= 1

        return {'cost':total_length, 'path':path_edges}



    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        # make queue
        list_of_nodes = self.network.nodes
        list_shortest_path = []
        #graph = CS312Graph.__init__(self,list_of_nodes)
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        # set distances and prevs
        for u in list_of_nodes:
            u.dist = float('inf')
            u.prev = None
        list_of_nodes[srcIndex].dist = 0
        #make the queue
        p_queue = makeQueue(use_heap)
        #add starting node to our path list
        p_queue.insert(list_of_nodes[0])
        #while we still have more nodes to visit
        while p_queue.getSize() is not 0:
            u = p_queue.deleteMin()
            # for every neighbor see if it is in our shortest path
            if u is not None:
                for indx in range (0,len(u.neighbors)):
                    edge = u.neighbors[indx]
                    if edge.dest.dist > (u.dist + edge.length):
                        edge.dest.dist = (u.dist + edge.length)
                        edge.dest.prev = u
                        p_queue.decreaseKey(indx)
                        p_queue.insert(edge.dest)
        t2 = time.time()

        return (t2-t1)


# Base class for the priority queues
class PriorityQueue(object):
    def __init__(self):
        self.path = []
        self.queue = []

    def getMin(self):
        pass

    def insert(self,node):
        self.path.append(node)

    # Accommodate the decrease in key value of a particular element
    # if you find a new shorter path to a node, you need to update that node's distance.
    #  In a min heap, that might actually change the node's position in the heap.
    # decreaseKey() is what lets the heap know that a node has been updated and (potentially) needs to sift up
    def decreaseKey(self):
        pass

    def deleteMin(self):
        pass

    def getSize(self):
        return len(self.queue)


class UnsortedArrayQueue(PriorityQueue):
    # Gets the node with the smallest distance
    def getMin(self):
        smallest = self.queue[0].dist
        node = None
        for i in range(len(self.queue)):
            if self.queue[i].dist <= smallest:
                smallest = self.queue[i].dist
                node = self.queue[i]
        return node

    # appends a new node to the queue
    def insert(self,node):
        super(UnsortedArrayQueue, self).insert(node)
        self.queue.append(node)

    def decreaseKey(self,indx):
        super().decreaseKey()

    # deletes the smallest node from the list
    def deleteMin(self):
        node = self.getMin()
        self.queue.remove(node)
        return node


class MyHeapQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.queue.append(None)

    def getMin(self):
        return self.queue[0]

    def insert(self,node):
        super(MyHeapQueue, self).insert(node)
        #if only the null left
        if len(self.queue) is 1:
            self.queue.append(node)
        else:
            self.queue.append(node)
            self.bubbleUpwards(len(self.queue)-1)

    def bubbleUpwards(self,length):
        parent = length//2
        child = length
        # while the newly inserted node is smaller than its parent
        while length > 0 and (self.queue[parent].dist > self.queue[child].dist):
            self.swapNodes(parent,child)
            child = parent
            parent = parent // 2

    def swapNodes(self, parent, child):
        temp = self.queue[parent]
        self.queue[parent] = self.queue[child]
        self.queue[child] = temp

    def deleteMin(self):
        # This will only be true when we have no more nodes to check
        if len(self.queue) == 1:
            self.queue.pop(0)
            return None
        minimum = self.queue[1]
        # replace min with last node
        self.queue[1] = self.queue[len(self.queue)-1]
        # pop off last node
        self.queue.pop(len(self.queue)-1)
        # sink the node down to its proper spot
        self.decreaseKey(1)

        return minimum

    def decreaseKey(self, indx):
        if indx != 0:
            newindx = indx
            left = indx * 2
            right = left + 1
            if (left) < len(self.queue) and self.queue[newindx].dist > self.queue[left].dist:
               newindx = left
            if (right) < len(self.queue) and self.queue[newindx].dist > self.queue[right].dist:
                newindx = right
            if newindx != indx:
               self.swapNodes(indx,newindx)
               self.decreaseKey(newindx)