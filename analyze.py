#!/usr/bin/python

from pandas import read_csv, MultiIndex

from scan import FILE_SAMPLES, SPECTRUM


def analyze():
    samples = read_csv(FILE_SAMPLES)
    devices = samples["id"].unique()
    
    print("got %d samples for %d devices" % (len(samples), len(devices)))

    samples = samples.groupby(["frequency", "id"]).size()
    index = [SPECTRUM, samples.index.get_level_values("id").unique()]
    ids = samples.index.get_level_values("id").unique()
    samples = samples.reindex(MultiIndex.from_product([SPECTRUM, ids],
                                                      names=samples.index.names))
    samples = samples.unstack("id")
    samples = samples.reset_index("frequency")

    import matplotlib.pyplot as plt
    plt.style.use("ggplot")
    p=samples.plot(x="frequency",
                   kind="barh",
                   stacked=True)
    from matplotlib.ticker import MaxNLocator
    p.set_yticklabels([SPECTRUM[f] / 1e6 for f in samples.index.tolist()])
    p.yaxis.set_major_locator(MaxNLocator(10)) 
    plt.savefig("spectrum.png", dpi=600)
        
    # select frequency with most signals for sensor with weakest signal
    # and then maximum number of total signals
    appropriate_freq = 0
    print("suggesting frequency %d" % appropriate_freq)


if __name__ == '__main__':
    analyze()
