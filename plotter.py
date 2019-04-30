import matplotlib.pyplot as plt


def ploty(lru, mlplru, cache_me_cache, values, xlabel, ylabel):
    plt.plot(lru, marker="o")
    plt.plot(mlplru, marker="o")
    plt.plot(cache_me_cache, marker="o")

    plt.xticks(range(len(values)), values)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(['LRU', 'MLPLRU', 'Cache-me-Cache'], loc='best')
    plt.grid()
    plt.show()


def plot_content_comparison(lru_results, mlplru_results, cache_me_cache_results, num_contents):

    ploty(lru_results[0], mlplru_results[0], cache_me_cache_results[0], num_contents, "number of contents", "self hit ratio")  # self cache hits
    ploty(lru_results[1], mlplru_results[1], cache_me_cache_results[1], num_contents, "number of contents", "d2d hit ratio")  # d2d cache hits
    ploty(lru_results[2], mlplru_results[2], cache_me_cache_results[2], num_contents, "number of contents", "base station hit ratio")  # bs cache hits
    ploty(lru_results[3], mlplru_results[3], cache_me_cache_results[3], num_contents, "number of contents", "satellite hit ratio")  # sat cache hits
    ploty(lru_results[4], mlplru_results[4], cache_me_cache_results[4], num_contents, "number of contents", "miss count")  # cache misses


def plot_zipf_distribution(lru_results, mlplru_results, cache_me_cache_results, zipf_values):

    ploty(lru_results[0], mlplru_results[0], cache_me_cache_results[0], zipf_values, "zipf parameter", "self hit ratio")  # self cache hits
    ploty(lru_results[1], mlplru_results[1], cache_me_cache_results[1], zipf_values, "zipf parameter", "d2d hit ratio")  # d2d cache hits
    ploty(lru_results[2], mlplru_results[2], cache_me_cache_results[2], zipf_values, "zipf parameter", "base station hit ratio")  # bs cache hits
    ploty(lru_results[3], mlplru_results[3], cache_me_cache_results[3], zipf_values, "zipf parameter", "satellite hit ratio")  # sat cache hits
    ploty(lru_results[4], mlplru_results[4], cache_me_cache_results[4], zipf_values, "zipf parameter", "miss count")  # cache misses
