import tools
import performer
import conductor
import random
import watchman

current_drums = "H................ S................ K................"

# AMBIENT
def gen_drumline(type):
    # Rhythm
    template = []

    if type == "hats":
        template.append("H")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % (performer.timing) == 0:
                template.append ("x")
            elif random.random() < watchman.activities["drums"]:
                template.append("x")
            else:
                template.append(".")

    elif type == "snare":
        template.append("S")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % (performer.timing * 2) == 4:
                template.append ("x")
            elif random.random() < watchman.activities["drums"]:
                template.append("x")
            else:
                template.append(".")

    elif type == "kick":
        template.append("K")

        for i in xrange(int(performer.tsig * performer.timing)):
            if i % (performer.timing * 2) == 0:
                template.append ("x")
            elif random.random() < watchman.activities["drums"]:
                template.append("x")
            else:
                template.append(".")

    return "".join(template)

def gen():
    global current_drums

    hats = gen_drumline("hats")
    snare = gen_drumline("snare")
    kick = gen_drumline("kick")

    current_drums = hats + " " + snare + " " + kick

def play():
    while len(performer.drumlines) <= performer.buff:
        performer.add_drums(current_drums)
