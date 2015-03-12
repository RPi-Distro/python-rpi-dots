from __future__ import absolute_import
import re
import math
import random, pygame, sys
from pygame.locals import *
from .vec2d import Vec2d

try:
    from RPi import GPIO
    print("Select some colours and connect the dots!")
except ImportError:
    GPIO = None
    print("Not running on a Raspberry Pi. Press Space to show and hide the plane.")

MINIMUM_DOTS_REQUIRED = 2

NUM_PINS = 28
PINS = list(set(list(range(NUM_PINS))) - set([2, 3]))

FPS = 5
WINDOWWIDTH = 780
WINDOWHEIGHT = 480

SCALE = 1

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
ORANGE    = (255,  65,   0)
RED       = (204,   0,   0)
GREEN     = (  0, 153,   0)
BLUE      = (  0, 128, 255)
BGCOLOR = WHITE

# 0     left tailfin
# 1     left wing
# 2     upper fuselage
# 3     lower fuselage
# 4     right tailfin
# 5     engine bit
# 6     right wing
# 7     door
# 8     door
# 9     door
# 10    door
# 11    tail highlight
# 12    right wing highlight
# 13    left wing highlight
# 14    engine bit
# 15    window (always cyan)
# 16    engine bit (always black)

COLOR_PINS = {
    27: RED,
    10: GREEN,
    0: BLUE,
    19: ORANGE,
}

DOT_PINS = list(set(PINS) - set(COLOR_PINS.items()))

CMAP = [0, 1, 2, 3, 0, 4, 1, 5, 5, 5, 5, 6, 7, 7, 4, 8, 9]

DATA = [
    "m223.147446,199.808777l-1.940414,-13.582901l-10.672272,-0.9702l-0.970215,5.821228l13.582901,8.731873z",
    "m437.563019,200.778976l-21.344543,-56.271973l-16.4935,-2.910614c0,0 0.970215,33.957214 0,48.510315c-0.970215,14.553101 -0.970215,15.5233 -0.970215,15.5233l38.808258,-4.851028z",
    "m169.786102,217.272476c4.851028,-2.910614 14.553085,-2.910614 14.553085,-2.910614l-34.927429,-58.212372l18.433914,-1.940414l68.884659,55.301758l322.108475,-14.553101c0,0 29.106201,0.9702 40.748657,3.880829c11.642517,2.910614 18.433899,10.672272 23.284973,12.612671c4.851013,1.94043 14.553101,4.851044 15.523254,10.672272c0.970215,5.821243 1.94043,6.791458 -4.851013,10.672272c-6.791443,3.880829 -33.957214,10.672272 -41.718872,11.642487c-7.761658,0.9702 -128.06723,2.910614 -132.918243,4.851028c-4.851044,1.940414 -25.225372,6.791428 -31.0466,6.791428c-5.821228,0 -66.944244,0.970215 -73.735657,-0.970184c-6.791473,-1.94043 -93.139801,-4.851044 -102.841888,-6.791458c-9.702057,-1.940399 -45.599686,-9.702057 -51.420929,-11.642471c-5.821243,-1.940414 -24.255157,-5.821228 -28.135971,-9.702072c-3.880844,-3.880814 -1.940414,-9.702057 -1.940414,-9.702057z",
    "m205.579956,238.374023c0,0 35.612289,7.025421 50.990326,7.727982c15.378021,0.70253 66.368317,0.70253 125.452332,1.405075c59.083984,0.702545 265.473297,-15.455933 237.954742,-8.430511c-27.518555,7.025436 -24.281067,6.322876 -34.802917,7.025436l-127.071045,4.21524c0,0 -12.140564,3.512711 -19.424896,4.215256c-7.284332,0.702545 -80.127625,0.702545 -80.127625,0.702545l-39.659119,-2.810181c0,0 -57.465271,-1.40509 -65.55896,-2.810165c-8.093704,-1.405075 -47.752838,-11.240677 -47.752838,-11.240677z",
    "m182.398773,227.944748l-36.867828,23.284958l18.433914,-1.940414c0,0 49.480515,-19.404129 50.450714,-20.374329c0.970215,-0.970215 10.672272,-2.910629 0,-4.851044c-10.672256,-1.940414 -32.0168,3.880829 -32.0168,3.880829z",
    "m380.36557,278.046661c2.575409,-1.144653 10.854919,-3.294922 19.872925,-4.613953c-0.42511,0.397888 24.868317,-5.42334 27.778931,-0.062683c2.910614,3.357574 3.420258,4.265106 3.831757,11.51712c-0.733124,4.962769 -1.765991,12.165741 -6.554352,13.0242c-6.791443,0 -25.748596,-0.111755 -41.271912,-3.022369c-15.523285,-2.910614 -21.344543,-3.880829 -21.344543,-3.880829l0.970215,-8.731842l16.71698,-4.229645z",
    "m365.767761,252.199905c-7.761658,11.642471 -17.463715,22.314743 -17.463715,22.314743l-94.110001,70.825073c0,0 2.910599,5.821228 12.612686,1.940399c9.702057,-3.880829 120.305573,-68.884644 120.305573,-68.884644l43.659271,-29.106186c0,0 6.791443,-1.940414 0,-4.851028c-6.791443,-2.910629 -20.374329,-1.94043 -33.957214,0c-13.582886,1.940414 -31.0466,7.761642 -31.0466,7.761642z",
    "m234.789917,234.492355c-0.708191,-3.237488 -0.119339,0.809372 -1.089539,-5.011871c-0.262009,-3.898987 0.077835,-4.88736 0.68486,-7.517807l7.6008,0.363174c0,0 -0.404678,0.767868 -0.404678,5.618896c0,4.851028 0.928696,5.071533 1.636902,7.297302l-8.428345,-0.749695z",
    "m349.07193,238.515854c0,0 -1.333405,-1.559082 -2.303619,-8.350525c-0.970215,-6.791443 0.565521,-9.172852 0.869049,-9.577545l9.440063,-0.243851c0,0 -0.970215,4.672043 -0.202362,9.743561c0.565521,3.756332 1.857422,7.154633 2.464417,8.469849l-10.267548,-0.041489z",
    "m468.609619,237.646805c0,0 -2.101227,-4.892532 -2.101227,-9.743561c0,-4.851028 0.869019,-9.458221 0.869019,-9.458221l10.309113,-0.101166c-0.202362,1.517578 -0.505859,5.071533 -0.505859,8.952362c0,3.880814 2.101227,10.088593 2.101227,10.088593l-10.672272,0.261993z",
    "m572.320557,235.664902c0,0 -1.476074,-3.029968 -2.303589,-10.428436c-0.119385,-6.791443 -0.041565,-11.743637 0.464294,-11.844803l9.803284,-0.565536c0.606995,2.32695 0.041504,4.851028 1.011658,11.642471c0.160828,6.791458 2.142761,11.44014 0.827576,11.237808l-9.803223,-0.041504z",
    "m186.155075,213.147812l-12.949905,-22.662369c0,0 10.521805,16.187408 16.996765,18.615524c6.47496,2.428101 42.896606,0.809357 42.896606,0.809357l-46.943466,3.237488z",
    "m420.872345,247.950714c0,0 -29.137299,21.852997 -85.793182,55.03717c-56.655914,33.184143 -66.368347,41.277863 -71.224548,41.277863c-4.856232,0 0,-4.046844 0,-4.046844c0,0 114.930511,-66.368347 157.017731,-92.268188z",
    "m416.3974,151.207581l16.996765,49.371567l-30.756042,1.618744c0,0 5.665588,0.809372 21.04361,-4.046844c15.378021,-4.856232 -7.284332,-46.943466 -7.284332,-46.943466z",
    "m368.077209,290.719635c23.625366,5.992371 54.05899,6.674042 55.876831,5.992371c-1.590607,-3.635681 -3.720093,-4.786957 -3.365173,-11.218658c0.809357,-10.52179 1.774567,-9.824951 2.683472,-12.778961c-2.045074,1.590637 -3.492859,5.027191 -5.111603,9.883423c0.426331,5.992371 2.683502,7.810211 -4.60083,10.238312c-7.284332,2.428101 -45.482697,-2.116486 -45.482697,-2.116486z",
    "m593.772644,215.565308l0.286133,9.729279c0,0 3.433899,0.286163 10.587769,-2.003082c7.15387,-2.289246 16.883179,-11.446228 16.883179,-12.018539c0,-0.572311 -7.726196,-5.150787 -7.726196,-5.150787c0,0 0.572266,1.716934 -3.147705,4.00618c-3.720032,2.28923 -16.883179,5.436951 -16.883179,5.436951z",
    "m425.808624,295.975006c-3.720032,-3.433868 -3.720032,-6.009277 -3.720032,-10.015442c0,-4.006195 0.286163,-10.301605 2.289246,-11.446228c2.003113,-1.144623 1.430786,-1.716949 3.433868,0.286163c2.003082,2.003082 2.861572,5.723114 2.861572,8.012329c0,2.289276 -0.286163,6.295441 -1.430786,8.870819c-1.144623,2.575409 -2.289246,4.292358 -3.433868,4.292358z"
]

def calculate_bezier(p, steps = 30):
    """
    Calculate a bezier curve from 4 control points and return a
    list of the resulting points.

    The function uses the forward differencing algorithm described here:
    http://www.niksula.cs.hut.fi/~hkankaan/Homepages/bezierfast.html
    """

    t = 1.0 / steps
    temp = t*t

    f = p[0]
    fd = 3 * (p[1] - p[0]) * t
    fdd_per_2 = 3 * (p[0] - 2 * p[1] + p[2]) * temp
    fddd_per_2 = 3 * (3 * (p[1] - p[2]) + p[3] - p[0]) * temp * t

    fddd = 2 * fddd_per_2
    fdd = 2 * fdd_per_2
    fddd_per_6 = fddd_per_2 / 3.0

    points = []
    for x in range(steps):
        points.append(f)
        f = f + fd + fdd_per_2 + fddd_per_6
        fd += fdd + fddd_per_2
        fdd += fddd
        fdd_per_2 += fddd_per_2
    points.append(f)
    return points

def path2points(d):
    points = []

    parse = re.split("(m|c|l|z)", d)[1:-2]
    parse = [(parse[i], re.split(" |,", parse[i+1])) for i in range(0, len(parse), 2)]

    x = 0
    y = 0

    for p in parse:
        p1 = [float(c) for c in p[1]]

        if p[0] == "m":
            x += p1[0]
            y += p1[1]
            points.append((x*SCALE, y*SCALE))
        elif p[0] == "l":
            x += p1[0]
            y += p1[1]
            points.append((x*SCALE, y*SCALE))
        elif p[0] == "c":
            control_points = [Vec2d(x,y), Vec2d(x+p1[0],y+p1[1]), Vec2d(x+p1[2],y+p1[3]), Vec2d(x+p1[4],y+p1[5])]

            bezier = calculate_bezier(control_points, 20)

            for i in range(1, len(bezier)):
                points.append((round(bezier[i].x*SCALE), round(bezier[i].y*SCALE)))

            x += p1[4]
            y += p1[5]

    return points

def ticked2colors(ticked):
    if len(ticked) == 0:
        ticked.append(WHITE)

    while True:
        colors = [random.choice(ticked) for i in range(8)]

        if len(set(colors)) == len(set(ticked)):     # all colors used
            colors.append(ORANGE)
            colors.append(BLACK)

            return colors

def read_hardware(fake):
    if GPIO:
        if enough_dots_connected():
            return get_selected_colors()
        else:
            return None
    elif fake:
        return [RED, GREEN, BLUE]

def gpio_setup(pins):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pins:
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_OFF)

def get_selected_colors():
    return [COLOR_PINS[pin] for pin in COLOR_PINS if pin_is_active(pin)]

def enough_dots_connected():
    active_pins = sum(pin_is_active(pin) for pin in DOT_PINS)
    return active_pins > MINIMUM_DOTS_REQUIRED

def pin_is_active(pin):
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
    state = GPIO.input(pin)
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_OFF)
    return state == 0

def main():
    global GPIO
    if GPIO:
        try:
            gpio_setup(PINS)
            fake = False
        except RuntimeError:
            GPIO = None
            fake = True
            print("Cannot access GPIO. Try running with sudo.")
    else:
        fake = True

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    if SCALE != 1:
        SCALESURF = pygame.Surface((WINDOWWIDTH*SCALE, WINDOWHEIGHT*SCALE), 0, 32)
    else:
        SCALESURF = DISPLAYSURF

    pygame.display.set_caption('Is it a bird?')

    points = [path2points(d) for d in DATA]

    last = None

    colors = None

    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    fake = not fake
                elif event.key == K_ESCAPE:
                    terminate()

        # handle plug and unplug (and color change) from the hardware

        hardware = read_hardware(fake)

        if hardware and hardware != last:
            colors = ticked2colors(hardware)

        last = hardware

        # clear the buffer, render plane if hardware plugged in

        SCALESURF.fill(BGCOLOR)

        if hardware:
            for j in range(len(DATA)):
                pygame.draw.polygon(SCALESURF, colors[CMAP[j]], points[j])
                if SCALE == 1:
                    pygame.draw.lines(SCALESURF, BLACK, True, points[j], 1)
                else:
                    pygame.draw.lines(SCALESURF, BLACK, True, points[j], SCALE*2)

        if SCALE != 1:
            pygame.transform.smoothscale(SCALESURF, (WINDOWWIDTH, WINDOWHEIGHT), DISPLAYSURF)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
