import sys
import animator
import time

# Everytime the Animator is invoked with his cycle() method, it will return
# - cycleSleep (float) the delay before the next call to the method should be made.
# - levels (float array) the brightness level that should be applied to each led group.

mainAnimator = animator.Animator()

# The dry-run flag is for testing the Animator settings on a computer that doesn't provide the I2C interface.
# In this situation, instead of importing the PCA9685 libraries and sending values to the controller, the values
# are printed to stdout in a linear bar format.
if "--dry-run" in sys.argv:
    print("process start in dry run mode")
    while True:
        cycleSleep, levels = mainAnimator.cycle()
        # Clear the screen and print the levels.
        width = 50
        print("\033c", end="")
        for channel, level in enumerate(levels):
            bar_length = int(level * width / 100)
            bar = "#" * bar_length + " " * (width - bar_length)
            print(f"{bar} {level}")
        time.sleep(cycleSleep)
else:
    from board import SCL, SDA
    import busio
    from adafruit_pca9685 import PCA9685

    i2c_bus = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c_bus)
    pca.frequency = 60
    print("process start in normal mode")
    while True:
        cycleSleep, levels = mainAnimator.cycle()
        for channel, level in enumerate(levels):
            # Sent levels to PWM controller.
            pca.channels[channel].duty_cycle = round(level * (65535 * 0.2))
        time.sleep(cycleSleep)




