import math
import matplotlib.pyplot as plt

def plot_e554_profile():
    with open("mesh/e554.dat") as f:
        # Skip title lines
        next(f)
        next(f)
        upper, lower = [], []
        for _ in range(37):
            line = next(f).strip()
            if line:
                parts = line.split()
                if len(parts) == 2:
                    x, y = map(float, parts)
                    upper.append((x, y))
        for _ in range(37):
            line = next(f).strip()
            if line:
                parts = line.split()
                if len(parts) == 2:
                    x, y = map(float, parts)
                    lower.append((x, y))
    plt.plot([p[0] for p in upper], [p[1] for p in upper],
             [p[0] for p in lower], [p[1] for p in lower])
    plt.axis('equal')

    def curve_length(coords):
        length = 0
        for i in range(len(coords) - 1):
            length += math.dist(coords[i], coords[i+1])
        return length

    upper_length = curve_length(upper)
    lower_length = curve_length(lower)
    total_length = upper_length + lower_length
    print(f"Upper line length: {upper_length}")
    print(f"Lower line length: {lower_length}")
    print(f"Total profile length: {total_length}")

    plt.show()

if __name__ == "__main__":
    plot_e554_profile()
