import argparse
import numpy as np
import matplotlib.pyplot as plt


def field(x, y):
    return 2 * x * y - 4 * y - 8, 4 * y**2 - x**2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    print("Задача 2. Варіант 1")
    print("x' = 2xy - 4y - 8; y' = 4y² - x²")
    print("Положення рівноваги: (-2, -1) та (4, 2)")
    print("Якобіан: [[2y, 2x - 4], [-2x, 8y]]")
    print("(-2, -1): J = [[-2, -8], [4, -8]]")
    print("             λ = -5 ± i√23 — стійкий фокус")
    print("             ξ' = -2ξ - 8η; η' = 4ξ - 8η")
    print("(4, 2): J = [[4, 4], [-8, 16]]")
    print("          λ₁ = 8, λ₂ = 12 — нестійкий вузол")
    print("          ξ' = 4ξ + 4η; η' = -8ξ + 16η")

    values = np.linspace(-6.5, 6.5, 330)
    x, y = np.meshgrid(values, values)
    u, v = field(x, y)
    fig, ax = plt.subplots(figsize=(9, 8))
    speed = np.hypot(u, v)
    ax.streamplot(x, y, u, v, color="#4577a7", density=1.6,
                  linewidth=0.75, arrowsize=0.9, maxlength=3)

    m, n = np.meshgrid(np.arange(-6, 7), np.arange(-6, 7))
    a, b = field(m, n)
    norm = np.hypot(a, b)
    ax.quiver(m, n, a / np.where(norm == 0, 1, norm),
              b / np.where(norm == 0, 1, norm), color="#a28e46",
              pivot="middle", scale=28, width=0.003)

    ax.scatter([-2], [-1], color="#198c62", marker="o", s=90,
               edgecolor="black", zorder=6, label="Стійкий фокус (-2, -1)")
    ax.scatter([4], [2], color="#c44949", marker="s", s=85,
               edgecolor="black", zorder=6, label="Нестійкий вузол (4, 2)")
    ax.set(xlim=(-6.5, 6.5), ylim=(-6.5, 6.5), xlabel="x", ylabel="y",
           title="Лабораторна робота №3. Задача 2, варіант 1")
    ax.set_aspect("equal")
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    if args.save:
        fig.savefig("t02.png", dpi=180)
    else:
        plt.show()


if __name__ == "__main__":
    main()
