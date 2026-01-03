import matplotlib.pyplot as plt
from numpy.random import normal, uniform


def show_histogram(count: int = 1000, bins: int = 20, low: float = -3, high: float = 3) -> None:
    """Render a Gaussian vs Uniform histogram with default parameters."""
    gaussian_numbers = normal(size=count)
    uniform_numbers = uniform(low=low, high=high, size=count)
    plt.hist(
        gaussian_numbers,
        bins=bins,
        histtype="stepfilled",
        normed=True,
        color="b",
        label="Gaussian",
    )
    plt.hist(
        uniform_numbers,
        bins=bins,
        histtype="stepfilled",
        normed=True,
        color="r",
        alpha=0.5,
        label="Uniform",
    )
    plt.title("Gaussian/Uniform Histogram")
    plt.xlabel("Value")
    plt.ylabel("Probability")
    plt.legend()
    plt.show()


def main() -> None:
    """Run the demo histogram with defaults."""
    show_histogram()


if __name__ == "__main__":
    main()
