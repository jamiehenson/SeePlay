import watchman
import performer
import mixer
import stabs
import threading
import tools
import extractor

motion = None

# Standard profile (motion drives tempo)
def standard_a(parent, img):
    global motion

    # b_detail = 3 # NEEDS TO BE AN ODD NUMBER
    # b_grid = watchman.get_brightness_grid(img, b_detail)
    # b_totals = watchman.get_brightness_totals(b_grid)
    # brightness = watchman.get_brightness(img.histogram(255), 20)
    # brightness = watchman.get_avg_brightness(img)
    brightness = watchman.get_luminosity(img, "a")
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    # motion = watchman.get_motion()
    # motion = extractor.edge()
    motion = tools.clamp(0, 100, extractor.hue() * 100000)

    # watchman.get_avg_brightness(img)
    # watchman.get_luminosity(img, "a")
    # watchman.get_luminosity(img, "b")
    # watchman.get_luminosity(img, "c")

    lower_vol = 5
    higher_vol = 120
    old_faces = 0

    # if performer.bar % 4 == 0:
    #     facecount = watchman.get_facecount(img)
    #     if facecount > old_faces:
    #         stabs.multifire(100)
    #     old_faces = facecount

    # print motion

    if motion > 40: 
        watchman.activity_boost = 0.5 # 1
        stabs.multifire(motion / 2)
    else:
        watchman.activity_boost = 0

    if motion >= 0 and motion <= 0.03:
        mixer.set_volume(parent, "bass", lower_vol)
        mixer.set_volume(parent, "drums", lower_vol)
        mixer.set_volume(parent, "chords", lower_vol)
        mixer.set_volume(parent, "melody", lower_vol)
        mixer.set_volume(parent, "stabs", lower_vol)
    else:
        mixer.set_volume(parent, "bass", tools.clamp(lower_vol, higher_vol - 40, 127 * (1 - brightness)))
        mixer.set_volume(parent, "drums", tools.clamp(lower_vol, higher_vol - 20, 127 * brightness))
        mixer.set_volume(parent, "chords", tools.clamp(lower_vol, higher_vol, 127 * brightness))
        mixer.set_volume(parent, "melody", tools.clamp(lower_vol, higher_vol, 127 * brightness))
        mixer.set_volume(parent, "stabs", tools.clamp(lower_vol, higher_vol, 60 * brightness))

    watchman.change_activity("bass", red_brightness, 2)
    watchman.change_activity("drums", brightness, 4)
    watchman.change_activity("melody", blue_brightness, 2)
    watchman.change_activity("chords", green_brightness, 2)
    watchman.change_activity("section", brightness, 2)

    # tools.adjust_mode(parent, brightness)

# Alternate profile (motion drives volume)
def standard_b(parent, img):
    brightness = watchman.get_brightness(img.histogram(250), 20)
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    motion = watchman.get_motion()

    # if performer.bar % 4 == 0:
        # facecount = watchman.get_facecount(img)

    motion_threshold = 10

    if motion > motion_threshold:  
        watchman.activity_boost = 1
        stabs.multifire(motion)
    else:
        watchman.activity_boost = 0
        
    mixer.set_volume(parent, "bass", 127 * tools.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "drums", 127 * tools.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "chords", 127 * tools.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "melody", 127 * tools.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "stabs", 127 * tools.invlerp(motion_threshold, 200, motion))

    parent.set_user_tempo_modifier(0.5 + brightness)

    watchman.change_activity("bass", red_brightness, 16)
    watchman.change_activity("drums", green_brightness, 16)
    watchman.change_activity("melody", red_brightness, 8)
    watchman.change_activity("chords", blue_brightness, 16)

    if blue_brightness > 0.5: 
        if parent.user_mode == "major": parent.set_user_mode("Minor")
    else:
        if parent.user_mode == "minor": parent.set_user_mode("Major")

# COPY OF A, BUT WITH LOWER SENSITIVITY
def sparse(parent, img):
    global motion

    brightness = watchman.get_brightness(img.histogram(250), 20)
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    motion = watchman.get_motion()

    # if performer.bar % 4 == 0:
        # facecount = watchman.get_facecount(img)

    if motion > 5: 
        watchman.activity_boost = 1
        stabs.multifire(motion)
        
        #tempomod = tools.clamp(1, 1.5, (motion / 100))
        tempomod = 1 + (tools.invlerp(0, 0.5, (motion / 100) / 2))
        parent.set_user_tempo_modifier(tempomod)
    else:
        watchman.activity_boost = 0
        parent.set_user_tempo_modifier(1)

    watchman.change_activity("bass", red_brightness, 16)
    watchman.change_activity("drums", green_brightness, 16)
    watchman.change_activity("melody", red_brightness, 8)
    watchman.change_activity("chords", max(green_brightness, blue_brightness), 16)

    if blue_brightness > 0.5: 
        if parent.user_mode == "major": parent.set_user_mode("Minor")
    else:
        if parent.user_mode == "minor": parent.set_user_mode("Major")

    mixer.set_volume(parent, "bass", 100 * (1 - brightness))
    mixer.set_volume(parent, "drums", 100 * (1 - brightness))
    mixer.set_volume(parent, "chords", 100 * brightness)
    mixer.set_volume(parent, "melody", 127 * brightness)
    mixer.set_volume(parent, "stabs", 127 * brightness)
