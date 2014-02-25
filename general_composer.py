# UTILITIES

roots = {
	   "C" : 0,
	   "C#" : 1,
	   "D" : 2,
	   "Eb" : 3,
	   "E" : 4,
	   "F" : 5,
	   "F#" : 6,
	   "G" : 7,
	   "Ab" : 8,
	   "A" : 9,
	   "Bb" : 10,
	   "B" : 11
	}


def midi_to_letter(scale, dicto, octave):
	newscale = []

	for note in scale:
		newscale.append(dicto[note % 12] + str(octave))

	return newscale

def make_scale(key, mode, octave):
	root = roots[key]
	majscale = [root, root+2, root+4, root+5, root+7, root+9, root+11, root+12]
	minscale = [root, root+2, root+3, root+5, root+7, root+8, root+10, root+12]

	revroots = dict((v,k) for k,v in roots.iteritems())

	if mode == "Major":
		return midi_to_letter(majscale,revroots, octave)
	else:
		return midi_to_letter(minscale,revroots, octave)

def make_chord(key, mode, octave):
	modesign = "+" if mode == "Major" else "-"
	chordname = key + str(octave) + modesign
	return chordname

def get_chord(chord):
	if len(chord) == 5:
		pitch = chord[:2]
	else:
		pitch = chord[:1]

	octave = int(chord[-2:-1]) * 12
	mode = str(chord[-1:])

	pitch = roots[pitch] + 24
	minoroffset = 3 if mode == "-" else 4
	chord = [pitch+octave, pitch+minoroffset+octave, pitch+7+octave, pitch+12+octave, pitch+12+minoroffset+octave, pitch+19+octave, pitch+24+octave]
	return chord

