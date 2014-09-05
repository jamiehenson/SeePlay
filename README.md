SeePlay.
A live, general purpose musical composer and performer for visual media.
By Jamie Henson (2014)
==================================

SeePlay is an OS X application that watches your screen, captures its contents, performs visual analysis on the contents to extract important features, and composes music in real time based upon those features that is heavily grounded in musical theory. Users can control what kind of music is made - for example, the key, tempo and chord progression.

SeePlay is written in Python and requires version 2.7.5. To run SeePlay, navigate to the source directory in your terminal, and run the main module by running:

    python main.py

From here, the GUI is loaded, where you can launch and interact with SeePlay's main process. SeePlay is automatically configured to use the IAC Driver on OS X, and any external DAW applications configured to listen to this channel will receive the live output composed by SeePlay from the on-screen visual content. No specific DAW application is required.

However, there are a lot of external packages and libraries that are required to make SeePlay run, which are as follows:

 - SimpleCV - a Python wrapper for OpenCV, which is responsible for a notable portion of the computation for the visual analysis techniques in use.
 - PySide - a Python binding for the cross-platform GUI tool-kit, Qt. Both PySide and Qt are free software.
 - Abjad - a Python interface for the LilyPond musical typesetting language, used to generate sheet music from SeePlay's generated musical data.
 - LilyPond - a free musical typesetting language
 - rtmidi - an audio interfacing library that handles the sending of MIDI information packets. These packets were sent out from SeePlay via internal MIDI channels, facilitated by Apple's IAC driver, part of CoreAudio which is the default audio manager in Mac OS X.
 - MIDIUtil} - a library which facilitates the writing of MIDI files using an API relatively compatible with SeePlay's in-house musical notation.

Enjoy!
