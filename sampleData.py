import random
import json

names = [
    "Alice", "Bob", "Charlie",
    "Dave", "Ellen", "Frank",
    "Greg", "Hellen", "Irene",
    "John", "Ken", "Larry",
    "Mike", "Nancy", "Oscar",
    "Pat", "Quincy", "Randy",
    "Sandy", "Tom", "Ulysses",
    "Vince", "Will", "Xavier",
    "Yolandi", "Zeke",
    ]

def genData(num=None, vote_ratio=.5, defer_ratio=.75, pretty=False):
    if num is None:
        num = random.randint(3, 26)

    nodes = [{
                "x": i * 2,
                "y": i * 2,
                "name": names[i],
                "votes": 1,
                "vote": random.random() > vote_ratio,
            } for i in range(0, num)]
    links = []

    for i in range(0, num):
        if random.random() < defer_ratio:
            defer = i
            while defer == i:
                defer = random.randint(0, num-1)
            links.append({"source": i, "target": defer})

    data = {"nodes": nodes, "links": links}
    if pretty:
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return json.dumps(data, separators=(',', ': '))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        num = min(int(sys.argv[1]), 26)
    else:
        num = 10

    if len(sys.argv) > 2:
        vote_ratio = float(sys.argv[2])
    else:
        vote_ratio = .75

    if len(sys.argv) > 3:
        defer_ratio = float(sys.argv[3])
    else:
        defer_ratio = .75

    print genData(num, vote_ratio, defer_ratio, True)
