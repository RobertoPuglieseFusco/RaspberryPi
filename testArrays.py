keyframesColors = [[2, 0, 0, 0], [10, 243,216,216], [20, 47,44,44], [30, 185,196,187], [40, 187,205,71], [50, 217,250,3], [60, 250,168,3]]

print(keyframesColors[1][0])

print(len(keyframesColors))

def lerp(a, b, f):
   return a + f*(b-a)

print(lerp(25,17, 0.7))