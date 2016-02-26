#!/usr/bin/python

from pandas import read_csv, MultiIndex

from scan import FILE_SAMPLES, SPECTRUM, mhz


def analyze():
    samples = read_csv(FILE_SAMPLES)
    devices = samples["id"].unique()
    
    print("got %d samples for %d devices" % (len(samples), len(devices)))

    samples = samples.groupby(["frequency", "id"]).size()
    samples = samples.reindex(MultiIndex.from_product([SPECTRUM, devices],
                                                      names=samples.index.names))
    samples = samples.unstack("id")

    # let's only keep frequencies with all signals present
    candidates = samples.dropna().copy()
    # total number of signals for each frequency
    total = candidates.sum(axis=1)
    # strength of the weakest signal
    weakest = candidates.min(axis=1)
    candidates["total"] = total
    candidates["weakest"] = weakest
    appropriate_freq = candidates.sort_values(by=["weakest", "total"],
                                              ascending=False).index[0]
    print("suggesting frequency %s" % mhz(appropriate_freq))
        
    import matplotlib.pyplot as plt

    plt.style.use("ggplot")
    p=samples.plot(
                   kind="barh",
                   stacked=True)
    from matplotlib.ticker import MaxNLocator
    p.set_yticklabels([f / 1e6 for f in SPECTRUM])
    p.yaxis.set_major_locator(MaxNLocator(10)) 
    plt.savefig("spectrum.png", dpi=600)


if __name__ == '__main__':
    analyze()
