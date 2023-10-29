import random
import time
from enum import Enum

CYCLES_PER_SECOND = 10
ON_TRANSITION_SPEED = 0.1
OFF_TRANSITION_SPEED = 0.2
DAY_START = 7
DAY_END = 18


def random_cycle_duration(min_duration, max_duration):
    min_duration *= CYCLES_PER_SECOND
    max_duration *= CYCLES_PER_SECOND
    return random.randint(min_duration, max_duration)


class ChannelStatus(Enum):
    HIGH = 0
    LOW = 1
    INCREASE = 2
    DECREASE = 3
    BLINK_DECREASE = 4
    BLINK_INCREASE = 5


class Channel:
    timeBeforeOn = 0
    timeBeforeOff = 0
    timeBeforeNextBlink = 0
    status = ChannelStatus.LOW
    level = 0

    def __update_timers(self):
        if self.status == ChannelStatus.LOW:
            self.timeBeforeOn -= 1
        elif self.status == ChannelStatus.HIGH:
            self.timeBeforeOff -= 1
            self.timeBeforeNextBlink -= 1

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

    def __update_levels(self):
        if self.status == ChannelStatus.INCREASE or self.status == ChannelStatus.BLINK_INCREASE:
            self.level += 1.0 / (ON_TRANSITION_SPEED * CYCLES_PER_SECOND)
        elif self.status == ChannelStatus.DECREASE or self.status == ChannelStatus.BLINK_DECREASE:
            self.level -= 1.0 / (OFF_TRANSITION_SPEED * CYCLES_PER_SECOND)
        if self.level < 0:
            self.level = 0
        if self.level > 1.0:
            self.level = 1.0

    def cycle(self):
        self.__update_timers()
        self.__update_status()
        self.__update_levels()

    def get_level(self):
        return self.level


class Animator:
    timeBeforeNextDayCheck = 0

    def __init__(self):
        self.channels = []
        for channel in range(16):
            self.channels.append(Channel())

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

    def cycle(self):
        if self.__is_day():
            return 10, [0] * 16

        levels = []
        for _, channel in enumerate(self.channels):
            channel.cycle()
            levels.append(channel.get_level())
        return 1 / CYCLES_PER_SECOND, levels
