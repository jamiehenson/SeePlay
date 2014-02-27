import general_composer
import performer
import conductor

def make_phrase(template, scale):
	bar = ""

	sequence = template.split()
	for note in sequence:
		if note != ".":
			note = str(scale[int(note[:1])] + note[-2:])
		bar += (note + " ")

	return bar

# Ambient
def ambient(parent, threshold):
	key = conductor.relativekey
	mode = conductor.relativemode
	bar = ""
	octave = str(3)

	chordscale = general_composer.make_chordscale(key,mode,octave)

	template1 = "0S1 . . . . . . . . . . . . . . ."
	template2 = "0cr . . . . . . . 1mi . . . . . ."
	template3 = "0cr . . 1cr . . 4cr . . . 0cr . 0cr . . ."

	if threshold == 0:
		bar = make_phrase(template1, chordscale)
	elif threshold == 1:
		bar = make_phrase(template2, chordscale)
	elif threshold == 2:
		bar = make_phrase(template3, chordscale)

	bar += "."

	while len(performer.chords) <= performer.buff: 
		performer.add_chords(bar)
