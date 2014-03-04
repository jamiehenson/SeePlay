channels = {
    "drums" : 0,
    "bass" : 1,
    "chords" : 2
}

def set_channel(chan, val):
    print "Channel", chan.upper(), "set to", val
    channels[chan] = val

def get_channel(chan):
    return channels[chan] + 144

def get_stdchannel(chan):
    return channels[chan]