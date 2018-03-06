#!/usr/bin/python3


from CS312Graph import *
import time

#Return the correct type of queue
def makeQueue(use_heap):
    return MyHeapQueue() if use_heap else UnsortedArrayQueue()



class NetworkRoutingSolver:
    def __init__( self, display ):
        self.nodes = []



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
        # total_length = 0
        # grab the src and destination nodes
        src = self.network.nodes[self.source]
        dst = self.network.nodes[self.dest]
        # see if the src and dst nodes are in the path i got back from Dijkstras
        if src in self.nodes and dst in self.nodes:
             self.getPath(dst,path_edges)
        # else:
        #     return
        # while edges_left > 0:
        #     edge = node.neighbors[2]
        #     path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
        #     total_length += edge.length
        #
        #     node = edge.dest
        #     edges_left -= 1
        return {'cost': dst.dist, 'path': path_edges}
    def getPath(self, node,path_edges):
        # start at the dst node and work backwards to the src node
        while node.prev != None:
            path_edges.append((node.prev.loc, node.loc, '{:.0f}'.format(node.dist)))
            node = node.prev

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        # make queue
        list_of_nodes = self.network.nodes
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
        p_queue.insert(list_of_nodes[srcIndex])
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
        self.nodes = p_queue.path
       # p_queue.path = list(set(p_queue.path))
        return (t2-t1)



# Base class for the priority queues
class PriorityQueue(object):
    def __init__(self):
        self.path = [] # the list that is holding the updated nodes
        self.queue = []

    def getMin(self):
        pass

    def insert(self,node):
        #just ad the node to the path
        self.path.append(node)

    # Accommodate the decrease in key value of a particular element
    # if you find a new shorter path to a node, you need to update that node's distance.
    #  In a min heap, that might actually change the node's position in the heap.
    # decreaseKey() is what lets the heap know that a node has been updated and (potentially) needs to sift up
    def decreaseKey(self,indx):
        pass

    def deleteMin(self):
        pass

    def getSize(self):
        return len(self.queue)


class UnsortedArrayQueue(PriorityQueue):
    # Gets the node with the smallest distance
    def getMin(self):
        # grab the min
        smallest = self.queue[0].dist
        node = None
        # check to see if there is another smaller
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
        pass

    # deletes the smallest node from the list
    def deleteMin(self):
        node = self.getMin()
        self.queue.remove(node)
        return node

#node id key, update the map as you change things positions
class MyHeapQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.queue.append(None)

    def getMin(self):
        return self.queue[0]

    def insert(self,node):
        super(MyHeapQueue, self).insert(node)
        self.queue.append(node)
        #if only the null left
        if len(self.queue) >  2:
            self.bubbleUpwards(len(self.queue) - 1)

    def bubbleUpwards(self,length):
        # grab the parent and child indices
        parent = length//2
        child = length
        # while the newly inserted node is smaller than its parent
        while length > 0 and (self.queue[parent].dist > self.queue[child].dist):
            self.swapNodes(parent,child)
            #reset
            child = parent
            parent = parent // 2
            # there is nothing at index zero
            if parent == 0:
                break
    #swaps parent/child
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
    #TIME: O(Logn) as it will only every travel as far down as logn. Logn is the depth of our heap
    def decreaseKey(self, indx):
        if indx != 0:
            newindx = indx
            left = indx * 2
            right = left + 1
            # If the decreases key value of a node is greater than parent of the node, then we don’t need to do anything.
            # Otherwise, we need to traverse up to fix the heap
            if (left) < len(self.queue) and self.queue[newindx].dist > self.queue[left].dist:
               newindx = left
            if (right) < len(self.queue) and self.queue[newindx].dist > self.queue[right].dist:
                newindx = right
            if newindx != indx:
               self.swapNodes(indx,newindx)
               self.decreaseKey(newindx)

               #100000 points unsorted = 885.916 seconds. 312,100000,1 to 3.  path of 1253.837