import threading
import sys


def spike_watch(firsttime):
    global r2, g2, b2, y2, w2, t2, p2, k2
    if firsttime is True:
        r2 = g2 = b2 = y2 = w2 = t2 = p2 = k2 = 0

    threshold = 100
    if abs(r2 - red) >= threshold:
        print "\nSpike: Red"
    elif abs(g2 - green) >= threshold:
        print "\nSpike: Green"
    elif abs(b2 - blue) >= threshold:
        print "\nSpike: Blue"
    elif abs(y2 - yellow) >= threshold:
        print "\nSpike: Yellow"
    elif abs(w2 - white) >= threshold:
        print "\nSpike: White"
    elif abs(t2 - teal) >= threshold:
        print "\nSpike: Teal"
    elif abs(p2 - purple) >= threshold:
        print "\nSpike: Purple"
    elif abs(k2 - black) >= threshold:
        print "\nSpike: Black"

    r2 = red
    g2 = green
    b2 = blue
    y2 = yellow
    w2 = white
    t2 = teal
    p2 = purple
    k2 = black

    threading.Timer(1, spike_watch, [False]).start()

def set_counters(col):
    global red, green, blue, yellow, white, teal, purple, black
    if col == "r":
        red += 1
    elif col == "b":
        blue += 1
    elif col == "k":
        black += 1
    elif col == "g":
        green += 1
    elif col == "y":
        yellow += 1
    elif col == "w":
        white += 1
    elif col == "p":
        purple += 1
    elif col == "t":
        teal += 1
    elif col == "wipe":
        red = black = blue = green = yellow = white = teal = purple = black = 0
        r2 = g2 = b2 = y2 = w2 = t2 = p2 = k2 = 0

def print_counters():
    sys.stdout.write("Colour count:" + 
        " | R: " + str(red) + 
        " | G: " + str(green) + 
        " | B: " + str(blue) + 
        " | K: " + str(black) + 
        " | Y: " + str(yellow) + 
        " | P: " + str(purple) + 
        " | T: " + str(teal) + 
        " | W: " + str(white) + " |\n")
    sys.stdout.flush()
