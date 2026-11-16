import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    angle = np.degrees(np.arctan(3 / 7))
    print("Задача 1. Варіант 1")
    print("x' = x + y; y' = 4x + y")
    print("На прямій y = x: dy/dx = 5/2")
    print(f"Гострий кут перетину з y = x: arctan(3/7) = {angle:.4f}°")
    print("Матриця A = [[1, 1], [4, 1]]")
    print("Власні числа: λ₁ = 3, λ₂ = -1; початок координат — сідло")
    print("Власні напрями: y = 2x і y = -2x")
    print("Кути з додатним напрямком Ox: ±arctan(2) = ±63.4349°")
    print("Загальний розв'язок: x(t) = C₁e^(3t) + C₂e^(-t)")
    print("                      y(t) = 2C₁e^(3t) - 2C₂e^(-t)")

    grid = np.linspace(-5, 5, 220)
    x, y = np.meshgrid(grid, grid)
    u, v = x + y, 4 * x + y

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.streamplot(x, y, u, v, color="#375a85", density=1.35,
                  linewidth=0.9, arrowsize=1, maxlength=5)
    xx = np.linspace(-5, 5, 400)
    ax.plot(xx, xx, color="#db8d2e", linewidth=2, label="Пряма y = x")
    ax.plot(xx, 2 * xx, color="#b74141", linestyle="--",
            linewidth=1.8, label="Власний напрям y = 2x")
    ax.plot(xx, -2 * xx, color="#399273", linestyle="--",
            linewidth=1.8, label="Власний напрям y = -2x")
    ax.scatter([0], [0], c="black", s=45, zorder=5, label="Сідло (0, 0)")
    ax.set(xlim=(-5, 5), ylim=(-5, 5), xlabel="x", ylabel="y",
           title="Лабораторна робота №3. Задача 1, варіант 1")
    ax.set_aspect("equal")
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    if args.save:
        fig.savefig("t01.png", dpi=180)
    else:
        plt.show()


if __name__ == "__main__":
    main()
