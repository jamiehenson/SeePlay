import performer
import watchman
import random

rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]

def gen_rhythm():
    global rhythm
    # Rhythm
    template = []
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < watchman.activities["section"]:
            template.append("x")
        else:
            template.append(".")

    rhythm = template

def gen():
    gen_rhythm()