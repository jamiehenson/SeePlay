import general_composer
import performer
import conductor
import random

current_drums = "H................ S................ K................"

# AMBIENT
def gen_drumline(type, threshold):
    # Rhythm
    template = []

    if type == "hats":
        template.append("H")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % (performer.timing / 2) == 0:
                template.append ("x")
            elif random.random() < (0.1 * (threshold)):
                template.append("x")
            else:
                template.append(".")
    elif type == "snare":
        template.append("S")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % (performer.timing * 2) == 4:
                template.append ("x")
            elif random.random() < (0.1 * (threshold)):
                template.append("x")
            else:
                template.append(".")
    elif type == "kick":
        template.append("K")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % performer.timing == 0:
                template.append ("x")
            elif random.random() < (0.1 * (threshold)):
                template.append("x")
            else:
                template.append(".")

    return "".join(template)

def gen(threshold):
    global current_drums

    hats = gen_drumline("hats", threshold)
    snare = gen_drumline("snare", threshold)
    kick = gen_drumline("kick", threshold)

    current_drums = hats + " " + snare + " " + kick

# Ambient
def ambient(parent, threshold):
    while len(performer.drumlines) <= performer.buff:
        performer.add_drums(current_drums)
