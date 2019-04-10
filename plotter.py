import matplotlib.pyplot as plt


def plot_cache_hits(self_hits, d2d_hits, bs_hits, sat_hits, universal, interval):
    plt.plot(self_hits)     # self cache hit
    plt.plot(d2d_hits)    # d2d cache hit
    plt.plot(bs_hits)    # base station cache hit
    plt.plot(sat_hits)    # satellite cache hit
    plt.plot(universal)    # get from universal resource


    plt.xlabel('number of contents')
    plt.xlabel('cache hit ratio')

    plt.xticks([0,1,2,3,4], interval)
    plt.legend(['y = self cache hits', 'y = d2d cache hits', 'y = bs cache hit', 'y = satellite cache hit', 'y = cache miss'], loc='upper left')

    plt.show()
