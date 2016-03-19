#!/usr/bin/env python

from pandas import read_csv, MultiIndex, DataFrame

from scan import FILE_SIGNALS, SPECTRUM, mhz

FILE_SPECTRUM="spectrum.svg"

def analyze():
    signals = read_csv(FILE_SIGNALS)
    devices = signals["id"].unique()
    
    print("got %d signals from %d devices" % (len(signals), len(devices)))

    signals = signals.groupby(["frequency", "id"]).size()
    signals = signals.reindex(MultiIndex.from_product([SPECTRUM, devices],
                                                      names=signals.index.names),
                              fill_value=0)
    signals = signals.unstack("id")
    
    # let's only keep frequencies with all signals present
    candidates = signals.dropna()
    # suggest frequency where the weakest sensor has the most
    # received signals, and then the frequency with most total
    # received signals for all sensors
    candidates = DataFrame({"total":   candidates.sum(axis=1),
                            "weakest": candidates.min(axis=1)})
    appropriate_freq = candidates.sort(["weakest", "total"],
                                       ascending=False).index[0]
    print("suggesting frequency %s" % mhz(appropriate_freq))

    signals.to_csv("spectrum.csv")
    
    import matplotlib.pyplot as plt
    from matplotlib.ticker import EngFormatter

    p=signals.plot(kind="Area")
    p.xaxis.set_major_formatter(EngFormatter(unit='Hz', places=2))
    plt.savefig(FILE_SPECTRUM, dpi=300)
    print("saved spectrum as %s" % FILE_SPECTRUM)
    

if __name__ == '__main__':
    analyze()
