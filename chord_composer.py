import general_composer
import performer
import conductor

# AMBIENT
def ambient(parent, threshold):
	key = conductor.relativekey
	mode = conductor.relativemode
	bar = ""
	octave = str(3)

	chord = general_composer.make_chord(key,mode,octave)

	if threshold == 0:
		for b in xrange(0,15):
			if b == 0 and performer.bar % 4 == 0:
				bar += str(chord + "S4" + " ") 
			else:
				bar += ". "
	if threshold == 1:
		for b in xrange(0,15):
			if b == 0 and performer.bar % 4 == 0:
				bar += str(chord + "S4" + " ") 
			else:
				bar += ". "

	bar += "."

	while len(performer.chords) <= performer.buff: performer.add_chords(bar)
