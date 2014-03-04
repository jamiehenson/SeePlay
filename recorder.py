from midiutil.MidiFile import MIDIFile
import lily
import performer
import general_composer
import mixer

sp_midi = None

def init():
    global sp_midi

    sp_midi = MIDIFile(3)
    time = 0

    sp_midi.addTrackName(mixer.channels["drums"], time, "Drums")
    if lily.show_bass: sp_midi.addTrackName(mixer.channels["drums"], time, "Bass")
    if lily.show_piano_lefthand or lily.show_piano_righthand: sp_midi.addTrackName(mixer.channels["drums"], time, "Chords")
    
    sp_midi.addTempo(0,0,127)

# Note framework: track,channel,pitch,time,duration,volume
def add_bass_bar(bar):
    global sp_midi

    track = mixer.channels["bass"]
    channel = track
    volume = 127

    sequence = list(bar)
    beat_ref = (performer.bar - 1) * performer.timing

    for i in xrange(len(sequence)):
        note = sequence[i]
        if note != ".":
            if len(note) == 5:
                pitch = note[:2]
            else:
                pitch = note[:1]

            octave = int(note[-3:-2])
            length = general_composer.lengths[str(note[-2:])]
            pitch = general_composer.letter_to_midi(pitch, octave)
            time = beat_ref + ((i+1)/performer.timing)
            sp_midi.addNote(track, channel, pitch, time, length, volume)

def make(parent):
    global sp_midi

    filename = parent.user_score_title
    filename = filename.replace(" ","").lower() + ".mid"

    print "Exporting MIDI file to " + filename + "..."

    binfile = open(filename, 'wb')
    sp_midi.writeFile(binfile)
    binfile.close()