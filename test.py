import json
import sampleData
from deferredvotes import get_vote_info, get_connection_info

data = get_vote_info()
tree = get_connection_info(data)

print(str(data))
print(str(tree))
