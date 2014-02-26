import general_composer
import performer
import conductor

# Ambient
def ambient(parent,threshold):
	key = conductor.relativekey
	mode = conductor.relativemode
	bar = ""
	octave = str(1)

	scale = general_composer.make_scale(key,mode,octave)

	if threshold == 0:
		for b in xrange(0,15):
			if b == 0:
				bar += str(scale[0] + "S1" + " ") 
			else:
				bar += ". "
	elif threshold == 1:
		for b in xrange(0,15):
			if b % 4 == 0:
				if b == 0: val = 0
				if b == 4: val = 2
				if b == 8: val = 4
				if b == 12: val = 2

				bar += str(scale[val] + "cr" + " ") 
			else:
				bar += ". "

	bar += "."

	while len(performer.basslines) <= performer.buff: performer.add_bass(bar)
