#!/usr/bin/python

from datetime import timedelta, datetime
from time import sleep
from random import randint

MIN_FREQ = 868.18  # MHz
MAX_FREQ = 868.32  # MHz
SAMPLE_TIME = timedelta(minutes=15)
FILE_SIGNALS = "signals.csv"


SPECTRUM = range(int(MIN_FREQ*1e6),
                 int(MAX_FREQ*1e6),
                 int(1e3))


def ec3k_listen(callback, freq, timeout):
    my_ec3k = ec3k.EnergyCount3K(callback=callback, freq=freq)
    my_ec3k.start()
    sleep(timeout.seconds)
    my_ec3k.stop()


def mock_listen(callback, freq, timeout):
    import random
    ids = [31, 37, 39, 47]
    if randint(0, 10) == 0:
        for i in range(randint(1, 10)):
            class state(object):
                id = random.choice(ids)
                device_on_flag = 1
                time_total = 0
                time_on = 0
                energy = 0
                power_current = 0
                power_max = 0
                reset_counter = 0
            callback(state)


try:
    import ec3k
    print("ec3k successfully found")
    listen = ec3k_listen
except:
    print("ec3k not found, faking it")
    listen = mock_listen


def mhz(f):
    return "%3.3f MHz" % (f / 1e6)


def receive(freq, timeout):
    print("receving at %s" % mhz(freq))
    signals = []

    def callback(state):
        signals.append(dict(frequency=freq,
                            id="%04x" % state.id,
                            device_on_flag=[0,1][state.device_on_flag],
                            time_total=state.time_total,
                            time_on=state.time_on,
                            energy=state.energy,
                            power_current=state.power_current,
                            power_max=state.power_max,
                            reset_counter=state.reset_counter))
    listen(callback, freq, timeout)
    print("got %d signals at %s during %s" % (len(signals), mhz(freq), timeout))
    return signals


def scan():
    time_estimate = SAMPLE_TIME * len(SPECTRUM)
    finish_time = datetime.now().replace(microsecond=0) + time_estimate
    print("warning: this will take approx %s" % time_estimate)
    print("estimated finish time at %s" % finish_time)
    signals = [signal
               for freq in SPECTRUM
               for signal in
               receive(freq, SAMPLE_TIME)]
    from pandas import DataFrame
    signals = DataFrame(signals)
    signals.to_csv(FILE_SIGNALS, index=None)
    print("done, wrote %d signals to %s" % (len(signals), FILE_SIGNALS))


if __name__ == '__main__':
    scan()
