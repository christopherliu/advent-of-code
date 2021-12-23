import itertools


class RegionV2():
    def __init__(self, x_start, x_end, y_start, y_end, z_start, z_end, is_on):
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.z_start = z_start
        self.z_end = z_end
        self.is_on = is_on

    def get_volume(self):
        if self.is_on:
            return ((self.x_end + 1 - self.x_start)
                    * (self.y_end + 1 - self.y_start)
                    * (self.z_end + 1 - self.z_start))

    def __str__(self):
        return "(%s, %s) x (%s, %s) x (%s, %s) %s" % (self.x_start, self.x_end, self.y_start, self.y_end, self.z_start, self.z_end, self.is_on)

    def __hash__(self) -> int:
        return hash((self.x_start, self.x_end, self.y_start, self.y_end, self.z_start, self.z_end, self.is_on))

    def __eq__(self, other):
        return (self.x_start == other.x_start
                and self.x_end == other.x_end
                and self.y_start == other.y_start
                and self.y_end == other.y_end
                and self.z_start == other.z_start
                and self.z_end == other.z_end
                and self.is_on == other.is_on)

    @classmethod
    def make(cls, xr, yr, zr, is_on):
        return RegionV2(xr[0], xr[1], yr[0], yr[1], zr[0], zr[1], is_on)

    @classmethod
    def list_str(cls, regions):
        return "\n".join(str(r) for r in sorted(regions, key=lambda region: (region.x_start, region.x_end, region.y_start, region.y_end, region.z_start, region.z_end, region.is_on)))

    @classmethod
    def find_overlap_volume(cls, region1, region2):
        (existing_x_ranges, new_x_ranges, overlapping_x_ranges) = separate_into_new_ranges(
            region1.x_start, region1.x_end, region2.x_start, region2.x_end)
        (existing_y_ranges, new_y_ranges, overlapping_y_ranges) = separate_into_new_ranges(
            region1.y_start, region1.y_end, region2.y_start, region2.y_end)
        (existing_z_ranges, new_z_ranges, overlapping_z_ranges) = separate_into_new_ranges(
            region1.z_start, region1.z_end, region2.z_start, region2.z_end)

        return sum([RegionV2.make(xr, yr, zr, region1.is_on).get_volume()
                    for xr, yr, zr in itertools.product(overlapping_x_ranges,
                                                        overlapping_y_ranges,
                                                        overlapping_z_ranges)
                    if xr[1] >= xr[0] and yr[1] >= yr[0] and zr[1] >= zr[0]])


def overlaps(region1, region2):
    # Returns true if 2 regions overlap
    return ((region2.x_start <= region1.x_end and region2.x_end >= region1.x_start)
            and (region2.y_start <= region1.y_end and region2.y_end >= region1.y_start)
            and (region2.z_start <= region1.z_end and region2.z_end >= region1.z_start))


def separate_into_new_ranges(existing_start, existing_end, new_start, new_end):
    existing_ranges = []
    new_ranges = []
    overlapping_ranges = []
    if new_start < existing_start:
        new_ranges.append((new_start, existing_start - 1))
        if new_end < existing_end:
            overlapping_ranges.append((existing_start, new_end))
            existing_ranges.append((new_end + 1, existing_end))
        elif new_end == existing_end:
            overlapping_ranges.append((existing_start, new_end))
        elif new_end > existing_end:
            overlapping_ranges.append((existing_start, existing_end))
            new_ranges.append((existing_end + 1, new_end))
    elif new_start == existing_start:
        if new_end < existing_end:
            overlapping_ranges.append((existing_start, new_end))
            existing_ranges.append((new_end + 1, existing_end))
        elif new_end == existing_end:
            overlapping_ranges.append((existing_start, new_end))
        elif new_end > existing_end:
            overlapping_ranges.append((existing_start, existing_end))
            new_ranges.append((existing_end + 1, new_end))
    elif new_start > existing_start:
        existing_ranges.append((existing_start, new_start - 1))
        if new_end < existing_end:
            overlapping_ranges.append((new_start, new_end))
            existing_ranges.append((new_end + 1, existing_end))
        elif new_end == existing_end:
            overlapping_ranges.append((new_start, new_end))
        elif new_end > existing_end:
            overlapping_ranges.append((new_start, existing_end))
            new_ranges.append((existing_end + 1, new_end))
    return (existing_ranges, new_ranges, overlapping_ranges)

# '(-45, 0) x (-44, 9) x (-39, 10) True' , '(-22, 26) x (-21, 25) x (-2, 43) True'


def apply_new_region(existing_regions, region_to_add):
    # existing_regions: a non-overlapping set of regions
    debug = False
    # Returns a new list of non-overlapping regions.
    new_regions = [region_to_add]
    rechopped_existing_regions = []
    if debug:
        print("*Starting existing regions:\n%s" %
              RegionV2.list_str(existing_regions))
    for existing_region in existing_regions:
        final_new_regions = []
        if debug:
            print("*Starting new regions:\n%s" %
                  RegionV2.list_str(new_regions))
            print("*Merging into:\n%s" % existing_region)
            
        existing_region_not_intersecting_new = True
        for new_region in new_regions:
            if not overlaps(new_region, existing_region):
                final_new_regions.append(new_region)
                continue
            existing_region_not_intersecting_new = False
            # Slice every new_region in new_regions across all areas of overlap.
            (existing_x_ranges, new_x_ranges, overlapping_x_ranges) = separate_into_new_ranges(
                existing_region.x_start, existing_region.x_end, new_region.x_start, new_region.x_end)
            (existing_y_ranges, new_y_ranges, overlapping_y_ranges) = separate_into_new_ranges(
                existing_region.y_start, existing_region.y_end, new_region.y_start, new_region.y_end)
            (existing_z_ranges, new_z_ranges, overlapping_z_ranges) = separate_into_new_ranges(
                existing_region.z_start, existing_region.z_end, new_region.z_start, new_region.z_end)

            # All overlapping = overlap.
            # Combines existing and new = not a region.
            # Only new or only existing with some overlap = new or existing
            rechopped_existing_regions.extend([RegionV2.make(xr, yr, zr, new_region.is_on)
                                               for xr, yr, zr in itertools.product(overlapping_x_ranges,
                                                                                   overlapping_y_ranges,
                                                                                   overlapping_z_ranges)
                                               if xr[1] >= xr[0] and yr[1] >= yr[0] and zr[1] >= zr[0]])

            rechopped_existing_regions.extend([RegionV2.make(xr, yr, zr, existing_region.is_on)
                                               for xr, yr, zr in itertools.chain(itertools.product(existing_x_ranges, existing_y_ranges, existing_z_ranges), itertools.product(existing_x_ranges, existing_y_ranges, overlapping_z_ranges), itertools.product(existing_x_ranges, overlapping_y_ranges, existing_z_ranges), itertools.product(overlapping_x_ranges, existing_y_ranges, existing_z_ranges), itertools.product(existing_x_ranges, overlapping_y_ranges, overlapping_z_ranges), itertools.product(overlapping_x_ranges, overlapping_y_ranges, existing_z_ranges), itertools.product(overlapping_x_ranges, existing_y_ranges, overlapping_z_ranges))
                                               if xr[1] >= xr[0] and yr[1] >= yr[0] and zr[1] >= zr[0]])

            final_new_regions.extend([RegionV2.make(xr, yr, zr, new_region.is_on)
                                      for xr, yr, zr in itertools.chain(itertools.product(new_x_ranges, new_y_ranges, new_z_ranges), itertools.product(new_x_ranges, new_y_ranges, overlapping_z_ranges), itertools.product(new_x_ranges, overlapping_y_ranges, new_z_ranges), itertools.product(overlapping_x_ranges, new_y_ranges, new_z_ranges), itertools.product(new_x_ranges, overlapping_y_ranges, overlapping_z_ranges), itertools.product(overlapping_x_ranges, overlapping_y_ranges, new_z_ranges), itertools.product(overlapping_x_ranges, new_y_ranges, overlapping_z_ranges))
                                      if xr[1] >= xr[0] and yr[1] >= yr[0] and zr[1] >= zr[0]])

            # if len([1 for region in rechopped_existing_regions if region.__eq__(RegionV2(-10, 0, -46, -45, 11, 25, True))]) > 0:
            #     print("Found one of the suspect regions")
            # if len([1 for region in rechopped_existing_regions if region.__eq__(RegionV2(-10, 0, -45, -36, 11, 25, True))]) > 0:
            #     print("Found one of the suspect regions")
            # if len([1 for region in final_new_regions if region.__eq__(RegionV2(-10, 0, -46, -45, 11, 25, True))]) > 0:
            #     print("Found one of the suspect regions")
            # if len([1 for region in final_new_regions if region.__eq__(RegionV2(-10, 0, -45, -36, 11, 25, True))]) > 0:
            #     print("Found one of the suspect regions")

        new_regions = list(set(final_new_regions))
        if debug:
            print("*Ending new regions:\n%s" % RegionV2.list_str(new_regions))
        if existing_region_not_intersecting_new:
            rechopped_existing_regions.append(existing_region)

    rechopped_existing_regions = list(set(rechopped_existing_regions))
    if debug:
        print("*Ending rechopped regions:\n%s" %
              RegionV2.list_str(rechopped_existing_regions))
    return (new_regions, rechopped_existing_regions)


def contains(containing_region, region):
    return (containing_region != region and (containing_region.x_start <= region.x_start and region.x_end <= containing_region.x_end)
            and (containing_region.y_start <= region.y_start and region.y_end <= containing_region.y_end)
            and (containing_region.z_start <= region.z_start and region.z_end <= containing_region.z_end))


def remove_nested_regions(set_of_regions):
    # There shouldn't be nested regions, but I'm too lazy to figure out why there are. Instead we're removing them.
    final_regions = []
    for region in set_of_regions:
        if not next((True for containing_region in set_of_regions if contains(containing_region, region)), None):
            final_regions.append(region)
    return final_regions

# print(remove_nested_regions(set([RegionV2(2,26,-36,-30,-47,-39,True),
#                                  RegionV2(-20,-36,-30,-47,-39,True)])))


def find_cube_on_count(input_regions):
    print("Starting with %s overlapping regions" % len(input_regions))

    # Add seed region
    nonoverlapping_regions = [input_regions[0]]
    print("First region: %s" % input_regions[0])

    for region_to_merge in input_regions[1:]:
        print("Merging in region: %s" % region_to_merge)
        regions_to_recalculate_idx = [pos
                                      for pos, region in enumerate(nonoverlapping_regions)
                                      if overlaps(region, region_to_merge)]
        print("Need to recalculate %s of %s existing regions" %
              (len(regions_to_recalculate_idx), len(nonoverlapping_regions)))
        nonoverlapping_regions_to_recalculate = [nonoverlapping_regions[i]
                                                 for i in regions_to_recalculate_idx]
        for index in sorted(regions_to_recalculate_idx, reverse=True):
            del nonoverlapping_regions[index]

        rechopped_older_regions = []
        new_regions = [region_to_merge]
        for region_to_recalculate in nonoverlapping_regions_to_recalculate:
            old_region_split = [region_to_recalculate]
            new_regions_updated = []
            for new_region in new_regions:
                (nr, old_region_split) = apply_new_region(
                    old_region_split, new_region)
                new_regions_updated.extend(nr)
            rechopped_older_regions.extend(old_region_split)
            new_regions = new_regions_updated

        # print("New regions: \n %s" % "\n".join(str(region)
        #       for region in new_regions))
        # print("Rechopped older regions: \n %s" % "\n".join(str(region)
        #       for region in rechopped_older_regions))

        # We keep off regions to check if they intersect, but we filter them out at the end.
        nonoverlapping_regions.extend([nr for nr in new_regions if nr.is_on])
        nonoverlapping_regions.extend(
            [r for r in rechopped_older_regions if r.is_on])
        print("Compressing existing %s regions" % len(nonoverlapping_regions))
        nonoverlapping_regions = remove_nested_regions(
            set(nonoverlapping_regions))
        print("%s regions after compression" % len(nonoverlapping_regions))
        print("New volume: %s" % sum([region.get_volume() for region in nonoverlapping_regions]))

    print("%s distinct regions found" % len(nonoverlapping_regions))
    # nonoverlapping_regions.sort(lambda region: (region.x_start, region.y_start, region.z_start))

    total_overlap_volume = 0
    for x, y in itertools.combinations(nonoverlapping_regions, 2):
        if overlaps(x, y):
            volume = RegionV2.find_overlap_volume(x, y)
            total_overlap_volume += volume
            print("Overlap found: volume %s\n%s\n%s" % (volume, x, y))
    print("Overlap check complete")

    print(sum([region.get_volume() for region in nonoverlapping_regions]))
    print(total_overlap_volume)


def parseline(line):
    on_off, coords = line.split(" ")
    x, y, z = coords.split(",")
    [x_start, x_end] = [int(i) for i in x.split("=")[1].split("..")]
    [y_start, y_end] = [int(i) for i in y.split("=")[1].split("..")]
    [z_start, z_end] = [int(i) for i in z.split("=")[1].split("..")]
    return RegionV2(x_start, x_end, y_start, y_end, z_start, z_end, on_off == "on")


def readfile(filename="Day 22 sample input 2.txt"):
    return [parseline(line) for line in open(filename, "r").readlines()]


# input = readfile("Day 22 sample input 1.txt")
# find_cube_on_count(input)  # should be 39 for sample input 1

input = readfile("Day 22 input 1.txt")
# find_cube_on_count(input[0:7]) #overlap found at on x=-31..15,y=-49..-1,z=-18..30
# find_cube_on_count(input[0:20]) # should be 543306 for input 1
find_cube_on_count(input)

# input = readfile("Day 22 sample input 2.txt")
# find_cube_on_count(input) # should be 590784 for input 2

input = readfile("Day 22 sample input 2.txt")
# find_cube_on_count(input[0:9]) # the 9th region, on x=-30..21,y=-8..43,z=-13..34, causes some sort of overlap
