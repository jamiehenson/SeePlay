import watchman
import performer
import mixer
import stabs
import threading

def default(parent, img):
    brightness = watchman.get_brightness(img.histogram(250), 20)
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    motion = watchman.get_motion()

    if performer.bar % 4 == 0:
        facecount = watchman.get_facecount(img)
    # parent.set_user_tempo_modifier(1)

    if motion > 10: 
        watchman.activity_boost = 1
        stabs.multifire(motion)
    else:
        watchman.activity_boost = 0

    watchman.change_activity("bass", red_brightness)
    watchman.change_activity("drums", green_brightness)
    watchman.change_activity("melody", red_brightness)
    watchman.change_activity("chords", green_brightness)

    if blue_brightness > 0.5: 
        if parent.user_mode == "+": parent.set_user_mode("Minor")
    else:
        if parent.user_mode == "-": parent.set_user_mode("Major")

    mixer.set_volume(parent, "bass", 127 * (1 - brightness))
    mixer.set_volume(parent, "drums", 127 * (1 - brightness))
    mixer.set_volume(parent, "chords", 127 * brightness)
    mixer.set_volume(parent, "melody", 127 * brightness)