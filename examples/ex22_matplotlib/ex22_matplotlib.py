import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("tkAgg")


def main():
    data = np.random.randn(1000)

    plt.figure()
    plt.hist(data, bins=30)
    plt.title("Simple Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == "__main__":
    main()
