# target area: x=209..238, y=-86..-59
# starting position: x, y = 0, 0

# Based on this, we can already limit the x velocity to a range that we could compute automatically.
# But by hand we can figure that it matches the formula:
# v + v-1 + v-2 + ... + 1 >= 209
# (v+1)*v/2 >= 209, v^2 + v >= 154.5, v >= 12

# Rather than simulate all the vx values from 12 to infinity,
# let's assume that the minimum vx will give us the highest height.
# after all, it worked for the example problem. ;)

def simulate_travel(vx, vy):
    initial_vx = vx
    initial_vy = vy
    max_height = 0
    #print ("simulating velocity %s, %s" % (vx,vy))
    x = 0
    y = 0
    while True:
        x += vx
        y += vy
        max_height = max(y, max_height)

        #Compute next velocity
        vx -= 1
        if (vx < 0): vx = 0 #assuming positive vx
        vy -= 1


        #print("position: %s, %s" % (x, y))
        if x in range(209, 238+1) and y in range (-86, -59+1):
            print ("simulating velocity %s, %s" % (initial_vx,initial_vy))
            print("SUCCESS")
            print(max_height)
            return True
        if y < -86:
            #print("failure")
            return False

# Test a bunch of things to find the right answer.
# Nothing with vx12 works
# for vy in range (0,10000):
#     simulate_travel(12,vy)
# for vy in range (0,1000):
#     simulate_travel(13,vy)
# for vy in range (0,1000):
#     simulate_travel(14,vy)
# for vy in range (0,1000):
#     simulate_travel(15,vy)
# for vx in range(16, 209+1):
#     for vy in range (0,100):
#         simulate_travel(vx,vy)

# Part 2: do a sweep of the most likely range
successes = 0
for vx in range(12, 238+1): # Ugh I had 209 here instead of 238 and missed a bunch of candidates
    for vy in range (-100,200):
        if simulate_travel(vx,vy):
            successes += 1

# Not 635
print(successes)