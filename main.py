import sys
import animator
import time

mainAnimator = animator.Animator()

if "--dry-run" in sys.argv:
    while True:
        cycleSleep, levels = mainAnimator.cycle()
        width = 50
        print("\033c", end="")
        for channel, level in enumerate(levels):
            print(round(level * (65535 * 0.2)))
        #print(levels)
        # print("\033c", end="")
        # for channel, level in enumerate(levels):
        #     bar_length = int(level * width / 100)
        #     bar = "#" * bar_length + " " * (width - bar_length)
        #     print(f"{bar} {level}")
        time.sleep(cycleSleep)
else:
    from board import SCL, SDA
    import busio
    from adafruit_pca9685 import PCA9685

    i2c_bus = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c_bus)
    pca.frequency = 60
    print("start process")
    while True:
        cycleSleep, levels = mainAnimator.cycle()
        for channel, level in enumerate(levels):
            pca.channels[channel].duty_cycle = round(level * (65535 * 0.2))
        time.sleep(cycleSleep)




