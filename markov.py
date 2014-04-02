import random

# First order Markov chains. May extend to second if there is the need.

# Each row must add to 1.

# Test
# markov_choices = [
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0],
# ]

# FIRST ORDER
# markov_choices = [
#     [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
#     [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
#     [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
#     [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
#     [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
#     [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
#     [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
#     [0.4, 0.05, 0.05, 0.05, 0.1, 0.25, 0.1],  # Leading
# ]

# SECOND ORDER
markov_choices = [
    # Prev: tonic
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: supertonic
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: mediant
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: subdominant
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: dominant
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: submediant
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ],
    # Prev: subtonic
    [
        [0.3, 0.05, 0.1, 0.2, 0.25, 0.05, 0.05],    # Tonic
        [0.1, 0.05, 0.1, 0.3, 0.35, 0.05, 0.05],  # Supertonic
        [0.3, 0.05, 0.1, 0.1, 0.35, 0.05, 0.05],  # Mediant
        [0.3, 0.05, 0.05, 0.2, 0.3, 0.05, 0.05],  # Sub-dominant
        [0.4, 0.05, 0.15, 0.2, 0.1, 0.05, 0.05],  # Dominant
        [0.05, 0, 0.1, 0.25, 0.2, 0.25, 0.15],  # Sub-mediant
        [0, 0, 0.2, 0.05, 0.25, 0.2, 0.3],  # Subtonic
    ]
]

def check():
    for i in xrange(len(markov_choices)):
        for j in xrange(len(markov_choices)):
            if sum(markov_choices[i][j]) != 1:
                print "Badly configured Markov values. Index:", markov_choices.index(row), "Total:", sum(row)
                return False

    return True

def markov_choice(row):
    total = sum(row)
    r = random.uniform(0, total)
    upto = 0
    for val in row:
        if upto + val > r:
            return val, row.index(val)
        upto += val
    return val, row.index(0)

def get(current):
    if check() == False:
        return

    val, index = markov_choice(markov_choices[int(current)])

    return str(index)

def get_second(current, prev):
    if check() == False:
        return

    val, index = markov_choice(markov_choices[int(prev)][int(current)])

    return str(index)

# QUICK TEST 
# print get_second(3, 4)