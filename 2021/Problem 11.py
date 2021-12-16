octopus_grid_raw = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
octopus_grid_rawr = """11111
19991
19191
19991
11111"""
octopus_grid_raw2 = """11111
10001
10801
10001
11111"""
octopus_grid_raw = """2264552475
7681287325
3878781441
6868471776
7175255555
7517441253
3513418848
4628736747
1133155762
8816621663"""

octopus_grid = list(map(lambda line: list(map(int, list(line))), octopus_grid_raw.splitlines()))

def model_step():
    number_of_flashes = 0

    # Increase energy level by 1.
    width = len(octopus_grid[0])
    height = len(octopus_grid)
    for y in range(0, height):
        for x in range(0, width):
            octopus_grid[y][x] += 1

    #print_grid()
    
    # Then, any octopus with an energy level greater than 9 flashes.
    def flash(y, x):
        number_of_flashes = 1
        octopus_grid[y][x] = 99 # An octopus can only flash at most once per step.
        # This increases the energy level of all adjacent octopuses by 1
        for (delta_y, delta_x) in [(-1,-1), (-1, 0), (-1, 1), (0,-1), (0, 0), (0, 1), (1,-1), (1, 0), (1, 1)]:
            if y + delta_y < 0 or y + delta_y >= height or x + delta_x < 0 or x + delta_x >= width:
                continue
            octopus_grid[y + delta_y][x + delta_x] += 1
            if octopus_grid[y + delta_y][x + delta_x] > 9 and octopus_grid[y + delta_y][x + delta_x] < 99:
                number_of_flashes += flash(y + delta_y, x + delta_x)
        return number_of_flashes

    for y in range(0, height):
        for x in range(0, width):
            if octopus_grid[y][x] > 9 and octopus_grid[y][x] < 99:
                number_of_flashes += flash(y, x)
                
    #print_grid()

    # Finally, any octopus that flashed during this step has its energy level set to 0
    for y in range(0, height):
        for x in range(0, width):
            if octopus_grid[y][x] > 9:
                octopus_grid[y][x] = 0
                
    #print_grid()
    if number_of_flashes == 100:
        print("nuts, everything flashed")
    return number_of_flashes

def print_grid():
    print("\n".join(list(map(lambda line: "|".join(map(str, line)), octopus_grid))))

number_of_flashes = 0
for i in range(0, 1000):
    print("After step %s" % (i))
    # print_grid()
    number_of_flashes += model_step()
    i += 1

print (number_of_flashes)