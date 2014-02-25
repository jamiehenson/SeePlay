import general_composer
import performer

# Ambient
def ambient_bass(parent,threshold):
	key = parent.user_key
	mode = parent.user_mood
	bar = ""
	octave = str(1)
	buff = int(parent.user_tsig)

	scale = general_composer.make_scale(key,mode,octave)

	for b in xrange(0,15):
		if b % 4 == 0:
			if b == 0: val = 0
			if b == 4: val = 2
			if b == 8: val = 4
			if b == 12: val = 2

			bar += str(scale[val] + " ") 
		else:
			bar += ". "

	bar += "."

	while len(performer.basslines) <= buff: performer.add_bass(bar)
