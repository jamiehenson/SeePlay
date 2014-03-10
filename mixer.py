channels = {
    "drums" : 0,
    "bass" : 1,
    "chords" : 2,
    "melody" : 3
}

volume = {
    "drums" : 100,
    "bass" : 100,
    "chords" : 100,
    "melody" : 100
}

def set_channel(chan, val):
    global channels

    print "Channel", chan.upper(), "set to", val
    channels[chan] = val

def get_channel(chan):
    return channels[chan] + 144

def get_channelname(chan):
    revchans = dict((v,k) for k,v in channels.iteritems())
    return revchans[chan - 144]

def get_channelnamestd(chan):
    revchans = dict((v,k) for k,v in channels.iteritems())
    return revchans[chan]

def get_stdchannel(chan):
    return channels[chan]

def set_volume(parent, chan, val):
    global volume

    if volume[chan] != val:
        print "Channel", chan.upper(), "volume set to", val
        volume[chan] = val
        parent.set_volumebar(chan, val)

def get_volume(chan):
    return volume[chan]