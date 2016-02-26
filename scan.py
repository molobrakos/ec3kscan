#!/usr/bin/python

from datetime import timedelta
from time import sleep
from random import randint

MIN_FREQ = 868.200  # MHz
MAX_FREQ = 868.403  # MHz
SAMPLE_TIME = timedelta(minutes=15)
FILE_SAMPLES = "samples.csv"

MOCK = True

SPECTRUM = range(int(MIN_FREQ*1e6),
                 int(MAX_FREQ*1e6),
                 int(1e3))


def listen(callback, freq, timeout):
    import ec3k
    my_ec3k = ec3k.EnergyCount3K(callback=callback, freq=freq)
    my_ec3k.start()
    sleep(timeout)
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


if MOCK:
    listen = mock_listen


def receive(freq, timeout):
    def mhz():
        return "%3.3f MHz" % (freq / 1e6)
    print("receving at %s" % mhz())
    samples = []

    def callback(state):
        samples.append(dict(frequency=freq,
                            id="%04x" % state.id,
                            device_on_flag=state.device_on_flag,
                            time_total=state.time_total,
                            time_on=state.time_on,
                            energy=state.energy,
                            power_current=state.power_current,
                            power_max=state.power_max,
                            reset_counter=state.reset_counter))
    listen(callback, freq, timeout)
    return samples


def scan():
    time_estimate = SAMPLE_TIME * len(SPECTRUM)
    print("warning: this will take approx %s" % time_estimate)
    samples = [sample
               for freq in SPECTRUM
               for sample in
               receive(freq, time_estimate.seconds)]
    from pandas import DataFrame
    samples = DataFrame(samples)
    samples.to_csv(FILE_SAMPLES, index=None)
    print("done, wrote %d samples to %s" % (len(samples), FILE_SAMPLES))


if __name__ == '__main__':
    scan()