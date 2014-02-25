import general_composer
import performer

# AMBIENT
def ambient_chords(parent, threshold):
	key = parent.user_key
	mode = parent.user_mood
	bar = ""
	octave = str(3)
	buff = int(parent.user_tsig)

	chord = general_composer.make_chord(key,mode,octave)

	for b in xrange(0,15):
		if b % 16 == 0:
			bar += str(chord + " ") 
		else:
			bar += ". "

	bar += "."

	while len(performer.chords) <= buff: performer.add_chords(bar)
