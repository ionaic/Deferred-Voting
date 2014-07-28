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
        self.TreeList = []
        self.TreeVoters = []
        if data:
            self.multiAddNode(data)

    def __str__(self):
        return str((self.Nodes, self.Edges, self.TreeList, self.TreeVoters))
    def __repr__(self):
        return self.__str__()
    
    def addNode(self, name, vote, defer):
        self.Nodes.append(DeferNode(name, vote, defer))
        #TODO ignores connections to objects not found in list, should add a
        # filler node for write-in candidates
        #
        # is this an undesirable behavior?
        if self.getNodeIdx(defer):
            self.Edges.append((self.getNodeIdx(name), self.getNodeIdx(defer)))

    def multiAddNode(self, tuplist):
        self.Nodes += [DeferNode(*tup) for tup in tuplist]
        # rebuilds the edges entirely
        self.Edges += [(idx, self.getNodeIdx(node.defer)) for idx,node in enumerate(self.Nodes) if self.getNodeIdx(node.defer) >=0]

    def getNodeIdx(self, nodeName):
        lst = filter(lambda n: n[1].name == nodeName, enumerate(self.Nodes))
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
        self.Edges += [(idx, idx) for idx in range(len(self.Nodes))]

        neighbors = [[tup[0] if tup[0] != idx else tup[1] for tup in filter(lambda e: idx in e, self.Edges)] for idx in range(len(self.Nodes))]
        tree_list = [[]]
        cur_tree_idx = 0
        for nbhd in neighbors:
            for idx in nbhd:
                tree_list[cur_tree_idx] += neighbors[idx]
            cur_tree_idx += 1
            tree_list.append([])

        self.TreeList = list(set([tuple(sorted(set(lst))) for lst in tree_list if lst != []]))
        self.markUsersWithTrees()

        return self.TreeList

    def markUsersWithTrees(self):
        for tree_idx,tree in enumerate(self.TreeList):
            for node_idx in tree:
                self.Nodes[node_idx].treeID = tree_idx

    def findRoots(self):
        """ Calculate the roots of the tree, requires detection of cycles the
        tree root may be a single node or a cycle of nodes """
        self.identifyTrees()
        self.TreeVoters = []
        # loopback edges ignored
        target_nodes = zip(*filter(lambda x: not x[0] == x[1], self.Edges))[1]
        for tree in self.TreeList:
            # pick a leaf to start at (doesn't matter which)
            leaves = filter(lambda x: x not in target_nodes, tree)
            if len(leaves) > 0:
                cur_idx = leaves[0]
                traverse_list = []
                # traverse upwards pushing into a list
                # if you encounter a node that's in the list already...
                while cur_idx >= 0 and cur_idx not in traverse_list:
                    traverse_list.append(cur_idx)
                    print("%s GetIDX for " % cur_idx + self.Nodes[cur_idx].defer)
                    cur_idx = self.getNodeIdx(self.Nodes[cur_idx].defer)
                # then everything in the list in between that element and the
                # current element is the loop
                self.TreeVoters.append(traverse_list[cur_idx:])

            # if no leaves then everything's in the "head" connected component
            else:
                self.TreeVoters.append(tree)

        return self.TreeVoters
