from collections import defaultdict

cave_system_raw = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

cave_system_raw ="""um-end
pk-um
FE-il
ay-FE
pk-start
end-jt
um-FE
RO-il
xc-ay
il-end
start-EZ
pk-FE
xc-start
jt-FE
EZ-um
pk-xc
xc-EZ
pk-ay
il-ay
jt-EZ
jt-om
pk-EZ"""

cave_system_rawg = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

cave_network = defaultdict(lambda: set())

for line in cave_system_raw.splitlines():
    (start,end) = line.split("-")
    cave_network[start].add(end)
    cave_network[end].add(start) # two way network

def is_big(node):
    return node[0].isupper()

def find_paths(prior_path, selected_small_cave):
    """Finds all paths starting with the prior path and ending on end."""
    # This will return some duplicates
    known_paths = []
    for next_node in cave_network[prior_path[-1]]:
        if next_node == "end":
            known_paths += [prior_path + [next_node]]
            continue
        if next_node == "start":
            continue
        if next_node not in prior_path or is_big(next_node):
            known_paths += find_paths(prior_path + [next_node], selected_small_cave)
        elif selected_small_cave is None and len(list(filter(lambda node: node == next_node, prior_path))) < 2:
            known_paths += find_paths(prior_path + [next_node], True)
    return known_paths
    

paths = list(map(lambda path: "-".join(path), find_paths(["start"], None)))
print("\n".join(list(sorted(paths))))
print(len(set(paths)))