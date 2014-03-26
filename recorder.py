from midiutil.MidiFile import MIDIFile
import lily
import performer
import tools
import mixer

sp_midi = None

def init(parent):
    global sp_midi

    sp_midi = MIDIFile(5)
    time = 0

    sp_midi.addTrackName(mixer.channels["drums"], time, "Drums")
    sp_midi.addProgramChange(mixer.channels["drums"], 10, 0, 118)

    sp_midi.addTrackName(mixer.channels["bass"], time, "Bass")
    sp_midi.addProgramChange(mixer.channels["bass"], mixer.channels["bass"], 0, 34)    

    sp_midi.addTrackName(mixer.channels["chords"], time, "Chords")
    sp_midi.addProgramChange(mixer.channels["chords"], mixer.channels["chords"], 0, 88)

    sp_midi.addTrackName(mixer.channels["melody"], time, "Melody")
    sp_midi.addProgramChange(mixer.channels["melody"], mixer.channels["melody"], 0, 26)
    print performer.bpm
    sp_midi.addTempo(0,0,parent.user_tempo)

# Note framework: track,channel,pitch,time,duration,volume
def add_chords_bar(bar):
    global sp_midi

    track = mixer.channels["chords"]
    channel = track
    volume = mixer.get_volume("chords")

    sequence = list(bar)
    beat_ref = (performer.bar - 1) * performer.timing

    for i in xrange(len(sequence)):
        chord = sequence[i]
        if chord != "." and chord.startswith("r") == False:
            chordnotes = tools.get_chord(chord)

            if len(chord) == 5:
                pitch = chord[:2]
            else:
                pitch = chord[:1]

            length = tools.lengths[str(chord[-2:])]
            time = beat_ref + ((i+1)/performer.timing)

            for note in chordnotes:    
                sp_midi.addNote(track, channel, note, time, length, volume)

def add_bass_bar(bar):
    global sp_midi

    track = mixer.channels["bass"]
    channel = track
    volume = mixer.get_volume("bass")

    sequence = list(bar)
    beat_ref = (performer.bar - 1) * performer.timing

    for i in xrange(len(sequence)):
        note = sequence[i]
        if note != "." and note.startswith("r") == False:
            if len(note) == 5:
                pitch = note[:2]
            else:
                pitch = note[:1]

            octave = int(note[-3:-2])
            length = tools.lengths[str(note[-2:])]
            pitch = tools.letter_to_midi(pitch, octave)
            time = beat_ref + ((i+1)/performer.timing)
            sp_midi.addNote(track, channel, pitch, time, length, volume)

def add_melody_bar(bar):
    global sp_midi

    track = mixer.channels["melody"]
    channel = track
    volume = mixer.get_volume("melody")

    sequence = list(bar)
    beat_ref = (performer.bar - 1) * performer.timing

    for i in xrange(len(sequence)):
        note = sequence[i]
        if note != "." and note.startswith("r") == False:
            if len(note) == 5:
                pitch = note[:2]
            else:
                pitch = note[:1]

            octave = int(note[-3:-2])
            length = tools.lengths[str(note[-2:])]
            pitch = tools.letter_to_midi(pitch, octave)
            time = beat_ref + ((i+1)/performer.timing)
            sp_midi.addNote(track, channel, pitch, time, length, volume)

def add_drums_bar(bar):
    global sp_midi

    track = mixer.channels["drums"]
    channel = 10
    volume = mixer.get_volume("drums")

    beat_ref = (performer.bar - 1) * performer.timing

    for i in xrange(len(bar[0])):
        hat = bar[0][i]
        snare = bar[1][i]
        kick = bar[2][i]

        time = beat_ref + ((i+1)/performer.timing)
        
        if hat != ".":
            sp_midi.addNote(track, channel, 42, time, 0.01, volume)
        if snare != ".":
            sp_midi.addNote(track, channel, 40, time, 0.01, volume)
        if kick != ".":
            sp_midi.addNote(track, channel, 36, time, 0.01, volume)

def make(parent):
    global sp_midi

    filename = parent.user_score_title
    filename = filename.replace(" ","").lower() + ".mid"

    print "Exporting MIDI file to " + filename + "..."

    binfile = open(filename, 'wb')
    sp_midi.writeFile(binfile)
    binfile.close()

    print "MIDI file written."