import general_composer
import performer
import conductor

def make_phrase(template, scale):
	bar = ""
	sequence = template.split()
	for note in sequence:
		if note != ".":
			note = str(scale[int(note[:1])] + str(note[-2:]))
		bar += (note + " ")

	return bar

# Ambient
def ambient(parent, threshold):
	key = conductor.relativekey
	mode = conductor.relativemode
	octave = str(1)

	scale = general_composer.make_scale(key,mode,octave)

	template1 = "0S1 . . . . . . . . . . . . . . ."
	template2 = "0cr . . . . . . . 1mi . . . . . ."
	template3 = "0cr . . 1cr . . 4cr . . . 0cr . 0cr . . ."

	if threshold == 0:
		bar = make_phrase(template1, scale)

	elif threshold == 1:
		bar = make_phrase(template2, scale)

	elif threshold == 2:
		bar = make_phrase(template3, scale)

	while len(performer.basslines) <= performer.buff: 
		performer.add_bass(bar)
