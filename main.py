
import simulation



def main():
    simulator = simulation.Simulator()
    simulator.simulate_LRU()

    # simulator.test_for_zipf_parameter()
    # simulator.test_for_num_contents()



if __name__ == "__main__":
    main()
