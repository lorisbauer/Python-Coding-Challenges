from itertools import permutations


def gradient(num_buckets, indicator, start=200, mixture=False):
    a, b, c = indicator
    rgb_codes = []
    step_size = 1024/num_buckets
    first = False
    for step in range(num_buckets):
        value = [0 for _ in range(3)]
        x = int(min(255, 0 + (step_size*step*0.6)))
        if x == 255 and first is False:
            first = True
            stop = step
        if first:
            if mixture is False:
                y = int(min(start, 0 + (step_size*(step - stop)*0.4)))
            else:
                y = int(min(start, 0 + (step_size*(step - stop)*0.4)))
                z = int(min(start, 0 + (step_size*(step - stop)*0.4)))
        else:
            y = 0
            z = 0
        value[a], value[b], value[c] = x, y, z
        rgb_codes.append(value)
    rgb_codes = rgb_codes[::-1]
    return {i: color for i, color in enumerate(rgb_codes)}


def get_surrounding(map, pos, target):
    surrounding = []
    x, y = pos
    directions = list(permutations((0, 1))) + list(permutations((0, -1)))
    for (a, b) in directions:
        x1, y1 = x + a, y + b
        if 0 <= x1 < len(map) and 0 <= y1 < len(map) and map[x1][y1].state != target:
            surrounding.append((x1, y1))
    return surrounding