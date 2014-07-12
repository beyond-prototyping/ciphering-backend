PIXELDIGITS = {
    '0': [
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1]
    ],
    '1': [
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1]
    ],
    '2': [
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,0,0],
        [1,1,1]
    ],
    '3': [
        [1,1,1],
        [0,0,1],
        [0,1,1],
        [0,0,1],
        [1,1,1]
    ],
    '4': [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1]
    ],
    '5': [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1]
    ],
    '6': [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ],
    '7': [
        [1,1,1],
        [0,0,1],
        [0,0,1],
        [0,0,1],
        [0,0,1]
    ],
    '8': [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ],
    '9': [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1]
    ],
    '.': [
        [0],
        [0],
        [0],
        [0],
        [1]
    ]
}


def create_pattern(digits):
    pattern = [[],[],[],[],[]]

    for i, digit in enumerate(digits):
        for j, row in enumerate(PIXELDIGITS[digit]):
            pattern[j] += row
            if i < 4: # 1px spacing between digits except for the last digit
                pattern[j].append(0)

    # fill up the rows with zeros
    for i in range(len(pattern)):
        if len(pattern[i]) < 17:
            filler = [0 for n in range(1, 18-len(pattern[i]))]
            pattern[i] += filler

    return pattern
