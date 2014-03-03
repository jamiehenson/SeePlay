import general_composer
import performer
import conductor

# AMBIENT
def ambient(parent, threshold):
    bar = ""
    drumtacet = "H................ S................ K................"

    while len(performer.chords) <= performer.buff: performer.add_drums(drumtacet)
