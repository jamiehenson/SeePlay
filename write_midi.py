from midiutil.MidiFile import MIDIFile

MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.
track = 0   
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

# Now add the note.
MyMIDI.addNote(0,0,60,0,1,127)
MyMIDI.addNote(0,0,60,1,1,127)

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()