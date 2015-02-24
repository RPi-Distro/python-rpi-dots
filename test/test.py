from RPi import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

num_pins = 28

pins = range(num_pins)

for pin in pins:
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

pin_states = {pin: GPIO.input(pin) for pin in pins}

print()
for pin, state in pin_states.items():
    print("%2d: %s" % (pin, state))

active = [pin for pin, state in pin_states.items() if not state]
inactive = [pin for pin, state in pin_states.items() if state]

print()
print("Total active: %s" % len(active))
print("Total inactive: %s" % len(inactive))
print()
print("Active pins: %s" % str(active))
print("Inactive pins: %s" % str(inactive))

