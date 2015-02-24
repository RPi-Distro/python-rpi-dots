from RPi import GPIO

GPIO.setmode(GPIO.BCM)

num_pins = 28

pins = range(num_pins)

for pin in pins:
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

pin_states = {pin: GPIO.input(pin) for pin in pins}

print()
for pin, state in pin_states.items():
    print("%2d: %s" % (pin, state))

active = sum(pin_states.values())
inactive = num_pins - active

print()
print("Total active: %i" % inactive)
print("Total inactive: %i" % active)
