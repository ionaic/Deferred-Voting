class DeferNode:
    def __init__(self, name, vote, defer):
        self.name = name
        self.vote = vote
        self.defer = defer # essentially the next node
        self.treeID = -1
    def __str__(self):
        return str((self.name, self.vote, self.defer, self.treeID))

    def __repr__(self):
        return self.__str__()

class DeferTree:
    def __init__(self, data=None):
        """ Should be a directed cyclic graph of connections """
        self.Nodes = []
        self.Edges = []
        if data:
            self.multiAddNode(data)

    def __str__(self):
        return str(zip(self.Nodes, self.Edges))
    def __repr__(self):
        return self.__str__()
    
    def addNode(self, name, vote, defer):
        self.Nodes.append(DeferNode(name, vote, defer))
        #TODO ignores connections to objects not found in list, should add a filler node for write-in candidates
        if self.getNodeIdx(defer):
            self.Edges.append((self.getNodeIdx(name), self.getNodeIdx(defer)))

    def multiAddNode(self, tuplist):
        self.Nodes += [DeferNode(*tup) for tup in tuplist]
        # rebuilds the edges entirely
        self.Edges += [(idx, self.getNodeIdx(node.defer)) for idx,node in enumerate(self.Nodes) if self.getNodeIdx(node.defer) >=0]

    def getNodeIdx(self, nodeName):
        lst = filter(lambda n: n[1].name == nodeName, enumerate(self.Nodes))
        print "getNodeIdx %s" % str(lst)
        return lst[0][0] if len(lst) > 0 else -1
    
    def storeTreeInDB(self):
        """ Store the tree in the database 
            -associate each user with a treeID
            -associate each tree ID with controlling users (the ones who are
            deferred to) """

    def pullTreeFromDB(self):
        """ Build the tree from database entries """

    def identifyTrees(self):
        """ Find the seperate voting entities in the tree """
        cur_tree_idx = 0
        # every edge where the idx is the destination
        neighbors = [filter(lambda e: idx in e, self.Edges) for idx in range(len(self.Nodes))]
        tree_idx_filter = [1] * len(self.Nodes)
        [[lst for idx,lst in neighbors if idx in nbhd] for nbhd in neighbors]
        #tree_list = [[]]
        #for nbhd in neighbors:
        #    tree_list[cur_tree_idx] +=
        #[[neighbors[idx] for idx in nbrhd] for nbrhd in neighbors]
        #[ [  for nbr in neighbors] for tree_idx in len(self.Nodes)]

    def findRoots(self):
        """ Calculate the roots of the tree, requires detection of cycles the
        tree root may be a single node or a cycle of nodes """
