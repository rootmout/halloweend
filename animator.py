import random
import time
from enum import Enum

# The refresh rate for computing the LED brightness (cycles per second).
CYCLES_PER_SECOND = 10
# The time took by a LED to pass from OFF to ON (second)
ON_TRANSITION_SPEED = 0.1
# The time took by a LED to pass from ON to OFF (second)
OFF_TRANSITION_SPEED = 0.2
# Start and end of the day (hours)
# During day all leds are turned off.
DAY_START = 7  # 7:00 AM
DAY_END = 18  # 6:00 PM


# `random_cycle_duration` accepts minimum and maximum time values in seconds,
# and converts them into a range of cycles before selecting a random value within that range.
# This approach expands the range of possibilities and ensures that it's not limited to discrete values.
def random_cycle_duration(min_duration, max_duration):
    min_duration *= CYCLES_PER_SECOND
    max_duration *= CYCLES_PER_SECOND
    return random.randint(min_duration, max_duration)


# `ChannelStatus` represent the phase in which each channel (grp of leds) can be.
# A typical histogram is :
# | - LOW - | INCREASE | ----- HIGH ----- | BLINK_DECREASE | BLINK_INCREASE | -- HIGH - | BLINK_DECREASE
# | BLINK_INCREASE | --- HIGH --- | DECREASE | ---- LOW ---- ect
class ChannelStatus(Enum):
    HIGH = 0
    LOW = 1
    INCREASE = 2
    DECREASE = 3
    BLINK_DECREASE = 4
    BLINK_INCREASE = 5


# `Channel` represent a group of leds.
class Channel:
    # Cycles before turning the channel ON
    timeBeforeOn = 0
    # Cycles before turning the channel OFF
    timeBeforeOff = 0
    # Cycles before next blink of the channel
    timeBeforeNextBlink = 0
    status = ChannelStatus.LOW
    # Brightness level (between 0 and 1.0)
    level = 0

    # `__update_timers` decrease the number of cycle remaining before turning ON/OFF or blinking when relevant.
    def __update_timers(self):
        if self.status == ChannelStatus.LOW:
            self.timeBeforeOn -= 1
        elif self.status == ChannelStatus.HIGH:
            self.timeBeforeOff -= 1
            self.timeBeforeNextBlink -= 1

    # `__update_status` update the channel status when relevant (eg: INCREASE is complete, a BLINK should be done,
    # etc...)
    def __update_status(self):
        if self.status == ChannelStatus.LOW and self.timeBeforeOn <= 0:
            self.status = ChannelStatus.INCREASE
            self.timeBeforeOff = random_cycle_duration(10, 15)
        elif self.status == ChannelStatus.INCREASE and self.level >= 1:
            self.status = ChannelStatus.HIGH
        elif self.status == ChannelStatus.HIGH and self.timeBeforeOff <= 0:
            self.status = ChannelStatus.DECREASE
            self.timeBeforeOn = random_cycle_duration(3, 5)
        elif self.status == ChannelStatus.DECREASE and self.level <= 0:
            self.status = ChannelStatus.LOW
        elif self.status == ChannelStatus.HIGH and self.timeBeforeNextBlink <= 0:
            self.status = ChannelStatus.BLINK_DECREASE
        elif self.status == ChannelStatus.BLINK_DECREASE and self.level <= 0:
            self.status = ChannelStatus.BLINK_INCREASE
        elif self.status == ChannelStatus.BLINK_INCREASE and self.level >= 1:
            self.status = ChannelStatus.HIGH
            self.timeBeforeNextBlink = random_cycle_duration(6, 8)

    # `__update_levels` increase of decrease the brightness level is relevant
    def __update_levels(self):
        if self.status == ChannelStatus.INCREASE or self.status == ChannelStatus.BLINK_INCREASE:
            self.level += 1.0 / (ON_TRANSITION_SPEED * CYCLES_PER_SECOND)
        elif self.status == ChannelStatus.DECREASE or self.status == ChannelStatus.BLINK_DECREASE:
            self.level -= 1.0 / (OFF_TRANSITION_SPEED * CYCLES_PER_SECOND)
        # Make sure the level is always within the 0 - 1.0 range.
        if self.level < 0:
            self.level = 0
        if self.level > 1.0:
            self.level = 1.0

    # `cycle` apply a new cycle to the Channel.
    def cycle(self):
        self.__update_timers()
        self.__update_status()
        self.__update_levels()

    # `get_level` return the current Channel level.
    def get_level(self):
        return self.level


# `Animator` manage multiple channels and also make sure to turn off leds during day.
class Animator:
    timeBeforeNextDayCheck = 0

    def __init__(self):
        self.channels = []
        for channel in range(16):
            self.channels.append(Channel())

    # `__is_day` check if the current hour is within the day range setup by DAY_START and DAY_END
    def __is_day(self):
        self.timeBeforeNextDayCheck -= 1
        if self.timeBeforeNextDayCheck <= 0:
            current_hour = time.localtime().tm_hour
            is_day_time = DAY_START <= current_hour < DAY_END
            if is_day_time:
                print("now: ", current_hour, " | is day time: all leds OFF")
                self.timeBeforeNextDayCheck = 0
                return True
            self.timeBeforeNextDayCheck = 10 * CYCLES_PER_SECOND
            print("now: ", current_hour, "h | is night")
            return False

    # `cycle` refresh all channels values. If it's day time will also return a null level array (will turn off the leds)
    def cycle(self):
        if self.__is_day():
            # return a value of 10 seconds for delay before next cycle to reduce the CPU usage during day as it's not
            # relevant to do so many refresh when leds are OFF.
            return 10, [0] * 16

        levels = []
        for _, channel in enumerate(self.channels):
            channel.cycle()
            levels.append(channel.get_level())
        return 1 / CYCLES_PER_SECOND, levels
