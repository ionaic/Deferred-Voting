from __future__ import print_function
import json
import sampleData
from deferredvotes import get_vote_info, get_connection_info

data = get_vote_info()
data_tree = get_connection_info(data)

def testGetTrees(tree):
    tree.Edges += [(idx, idx) for idx in range(len(tree.Nodes))]

    neighbors = [[tup[0] if tup[0] != idx else tup[1] for tup in filter(lambda e: idx in e, tree.Edges)] for idx in range(len(tree.Nodes))]
    tree_list = [[]]
    cur_tree_idx = 0

    #tree_list = [[neighbors[idx] for idx in nbhd if cur_tree_idx in 
    for nbhd in neighbors:
        for idx in nbhd:
            tree_list[cur_tree_idx] += neighbors[idx]
        cur_tree_idx += 1
        tree_list.append([])

    thingset = list(set([tuple(sorted(set(lst))) for lst in tree_list if lst != []]))

def testGetCycles(self):
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

print("\ntreevoters " + str(data_tree.findRoots()))
print("\ntree " + str(data_tree))
print(str(data_tree.Nodes[11]))
