from __future__ import division
from collections import deque

class DeferNode:
    def __init__(self, name, vote, defer):
        self.name = name # voter name
        self.vote = vote # actual content of your vote
        self.vote_count = 1 # number of votes
        self.defer = defer # essentially the next node
        self.deferral_count = 1 # how many people defer to you
        self.treeID = -1
    def __str__(self):
        return str((self.name, self.vote, self.vote_count, self.defer, self.deferral_count, self.treeID))
        #return str({"name":self.name, "vote":self.vote, "vote count":self.vote_count, "defer":self.defer, "deferral_count":self.deferral_count, "tree":self.treeID})

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
        mod_edges = self.Edges + [(idx, idx) for idx in range(len(self.Nodes))]

        neighbors = [[tup[0] if tup[0] != idx else tup[1] for tup in filter(lambda e: idx in e, mod_edges)] for idx in range(len(self.Nodes))]
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

    def getSubtreeLeaves(self, treeIdx=-1, tree=[]):
        return filter(lambda x: x not in self.getTargetNodes(), \
                self.TreeList[treeIdx] if treeIdx >= 0 else tree)

    def getSourceNodes(self):
        return zip(*filter(lambda x: not x[0] == x[1], self.Edges))[0]

    def getTargetNodes(self):
        return zip(*filter(lambda x: not x[0] == x[1], self.Edges))[1]

    def findRoots(self):
        """ Calculate the roots of the tree, requires detection of cycles the
        tree root may be a single node or a cycle of nodes """
        self.identifyTrees()
        self.TreeVoters = []
        # loopback edges ignored
        target_nodes = self.getTargetNodes()
        for tree in self.TreeList:
            # pick a leaf to start at (doesn't matter which)
            #leaves = filter(lambda x: x not in target_nodes, tree)
            leaves = self.getSubtreeLeaves(tree=tree)
            if len(leaves) > 0:
                cur_idx = leaves[0]
                traverse_list = []
                # traverse upwards pushing into a list
                # if you encounter a node that's in the list already...
                while cur_idx >= 0 and cur_idx not in traverse_list:
                    traverse_list.append(cur_idx)
                    cur_idx = self.getNodeIdx(self.Nodes[cur_idx].defer)
                # then everything in the list in between that element and the
                # current element is the loop
                self.TreeVoters.append(traverse_list[cur_idx:])

            # if no leaves then everything's in the "head" connected component
            else:
                self.TreeVoters.append(tree)

        return self.TreeVoters
    
    def countDeferrals(self):
        """ Count up the deferrals and pass along votes once the tree is built
            fully """
        # clear the existing data in the nodes
        for node in self.Nodes:
            node.vote_count = 1
            node.deferral_count = 1

        for idx,tree in enumerate(self.TreeList):
            # counts the actual votes
            votes = len(tree)/len(self.TreeVoters[idx])
            for voter_idx in tree:
                self.Nodes[voter_idx].vote_count = \
                   votes if voter_idx in self.TreeVoters[idx] else 0
            
            # propagate the deferrals
            traversal_queue = deque(self.getSubtreeLeaves(treeIdx=idx))
            while len(traversal_queue) > 0:
                print(str(traversal_queue))
                cur_node_idx = traversal_queue.popleft()
                # get the next node in BFS
                nxt_idx = self.getNodeIdx(self.Nodes[cur_node_idx].defer)

                # if the next node is in the tree and not a voter, add for traversal
                if nxt_idx >= 0:
                    if nxt_idx not in self.TreeVoters[idx] and nxt_idx not in traversal_queue:
                        traversal_queue.append(nxt_idx)
                    # increase the next node's number of defers by cur node's number of defers
                    self.Nodes[nxt_idx].deferral_count += self.Nodes[cur_node_idx].deferral_count
