import simulation


def main():
    simulator = simulation.Simulator()
    simulator.simulate()

    """
    These two methods comparing different zipf parameters and
    different number of contents for 3 algorithms and plot their
    performance. You can uncomment them if you want.
    """
    # simulator.compare_zipf_parameter()
    # simulator.compare_num_contents()


if __name__ == "__main__":
    main()
