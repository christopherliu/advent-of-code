scanner_coordinates = [
    [[404,-588,-901],
     [528,-643,409]],
    [[-336,658,858],
     [-460,603,-452]]
]

def diff(c1, c2):
    return [c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2]]

delta = diff(scanner_coordinates[0][0], scanner_coordinates[0][1])
delta2 = diff(scanner_coordinates[1][0], scanner_coordinates[1][1])

print(delta, delta2)

all_known_beacons = set()

other_scanner = 1
for beacon in scanner_coordinates[0]:
    for beacon2 in scanner_coordinates[0]:
        if beacon == beacon2:
            continue
        delta = diff(beacon, beacon2)
        for beaconA in scanner_coordinates[other_scanner]:
            for beaconB in scanner_coordinates[other_scanner]:
                delta2 = diff(beaconA, beaconB)
                if sanity_check(delta, delta2):
                    if apply_transformation(transformation, delta2) == delta:
                        # Found a potential match.
                        #TODO tomorrow: in what order do I apply translate vs. rotate again?
                        # go remember all of linear algebra.

for transformation in poss_transformations:
    if apply_transformation(transformation, delta2) == delta:
        print("Found a potential match from scanner 0.0:1 to scanner 1.0:2")
        candidate_map = { 0: 1 }
        potential_transformation = transformation
        # Using potential_transformation, try to map the rest of scanner 1 to scanner 0.
        # If there is > 12 overlap, then this transformation is correct and we can
        # add the beacons to the set of all beacons
        
        
print(len(all_known_beacons))