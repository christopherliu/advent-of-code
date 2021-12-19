from itertools import *
import math
import numpy as np

scanner_coordinates = [
    [(404,-588,-901),
     (528,-643,409)],
    [(-336,658,858),
     (-460,603,-452)]
]

def readfile(filename = "Day 19 sample input.txt"):
    lines = open(filename, "r").readlines()
    scanner_coordinates = []
    current_scanner = None
    for line in lines:
        line = line.strip()
        if line.startswith("---"):
            if current_scanner != None: scanner_coordinates.append(current_scanner)
            current_scanner = []
        elif line != "":
            #print("line %s" % line)
            current_scanner.append(tuple([int(n) for n in line.split(",")]))
    scanner_coordinates.append(current_scanner)
    #print(scanner_coordinates[0])
    return scanner_coordinates

def diff(c1, c2):
    # delta = diff(scanner_coordinates[0][0], scanner_coordinates[0][1])
    # delta2 = diff(scanner_coordinates[1][0], scanner_coordinates[1][1])
    # print(delta, delta2)
    return [c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2]]

# This generates 6 orders of coordinates, 8 xyz directions. That's 48 transformation matrices, unlike the 24 the instructions said.
# I guess my program will be 0.5x as fast unless I figure out which half I can exclude. ¯\_(ツ)_/¯
all_possible_rotations = [np.array(rotation) for rotation_list in [list(permutations([(x, 0, 0),
                          (0, y, 0),
                          (0, 0, z)])) for x, y, z in product((-1, 1), (-1, 1), (-1, 1))]
                          for rotation in rotation_list]
# print(all_possible_rotations)

def sanity_check(delta1, delta2):
    # Returns true if delta1 and delta2 could conceivably be rotated/reflected onto each other.
    return sum([abs(coord) for coord in delta1]) == sum([abs(coord) for coord in delta2])

scanner_locations = [
    [0,0,0]
]
def find_possible_transformation_to_base_space(all_known_beacons, x):
    global scanner_locations
    print("Transforming coordinates from scanner %s onto base space" % x)
    # Possible optimization: keep track of new coordinates vs old so that we don't try to transform on the ones that we know won't be novel.
    # I actually don't understand why this is so slow -- sanity check should be a fast operation, and that should gate most of the matrix mults.
    for (beaconW_A, beaconW_B), (beaconX_A, beaconX_B) in product(
        combinations(all_known_beacons, 2),
        list(combinations(scanner_coordinates[x], 2)) + list(combinations(reversed(scanner_coordinates[x]), 2))):
        deltaW = diff(beaconW_A, beaconW_B)
        deltaX = diff(beaconX_A, beaconX_B)
        if sanity_check(deltaW, deltaX):
            possible_rotations = list(filter(lambda rotation: (np.matmul(rotation, deltaX) == deltaW).all(), all_possible_rotations))
            for possible_rotation in possible_rotations:
                # Greedy evaluation:
                # Using potential_transformation, try to map the rest of scanner x to scanner W.
                # If >= 12 beacons overlap, then this transformation is presumed correct and we can
                # add the beacons to the set of all beacons.
                translation = np.subtract(beaconW_A, np.matmul(possible_rotation, beaconX_A))
                all_coordinates_transformed = set(map(tuple, [
                    np.add(translation, np.matmul(possible_rotation, beaconX))
                    for beaconX in scanner_coordinates[x]]))
                if len(all_known_beacons.intersection(all_coordinates_transformed)) >= 12:
                    print("Applying rotation %s, then translation %s converts scanner %s to base coordinate system!" % (possible_rotation, translation, x))
                    scanner_locations.append(translation)
                    return all_known_beacons.union(all_coordinates_transformed)
    print ("Did not find an appropriate transformation from %s to base coordinate system." % x)
    return False

scanner_coordinates = readfile("Day 19 input.txt")
#print(scanner_coordinates)
all_known_beacons = set(scanner_coordinates[0])

# Order in which my scanners mapped: 2, 20, 25, 6, 8, 16, 18, 7, 12, 27, 10, 19, 26, 4, 13, 17, 21, 22, 3, 5, 11, 14, 15, 24, 1, 9, 23
# Saves time if you're doing it again
unmapped_scanners = list(range(1, len(scanner_coordinates)))
unmapped_scanners = [2, 20, 25, 6, 8, 16, 18, 7, 12, 27, 10, 19, 26, 4, 13, 17, 21, 22, 3, 5, 11, 14, 15, 24, 1, 9, 23]
while len(unmapped_scanners) > 0:
    next = unmapped_scanners.pop(0)
    new_space = find_possible_transformation_to_base_space(all_known_beacons, next)
    if new_space:
        all_known_beacons = new_space
    else:
        unmapped_scanners.append(next)
    print("Beacons known so far: %s" % len(all_known_beacons))
    print("Scanners remaining not transformed onto the base coordinate system: %s" % len(unmapped_scanners))

# Part 2
def manhattan(distance):
    return abs(distance[0]) + abs(distance[1]) + abs(distance[2])

print("Largest Manhattan distance:")
print(max(
    [manhattan(diff(s1, s2)) for s1, s2 in permutations(scanner_locations, 2)]
    ))

print("OK")