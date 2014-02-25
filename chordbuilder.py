def get_chord(chord):
	if len(chord) == 5:
		pitch = chord[:2]
	else:
		pitch = chord[:1]

	octave = int(chord[-2:-1]) * 12
	mode = str(chord[-3:-2])

	roots = {
	   "C" : 24,
	   "Db" : 25,
	   "D" : 26,
	   "Eb" : 27,
	   "E" : 28,
	   "F" : 29,
	   "Gb" : 30,
	   "G" : 31,
	   "Ab" : 32,
	   "A" : 33,
	   "Bb" : 34,
	   "B" : 35,
	}

	pitch = roots[pitch]
	minoroffset = 3 if mode == "-" else 4
	chord = [pitch+octave, pitch+minoroffset+octave, pitch+7+octave, pitch+12+octave, pitch+12+minoroffset+octave, pitch+19+octave, pitch+24+octave]
	return chord