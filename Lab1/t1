import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
from scipy.integrate import solve_ivp


def f(x, y):
    return y**2 - 3 * y + x - 2


def fxx(x, y):
    return 1 + (2 * y - 3) * f(x, y)


def zero_isocline(y):
    return 2 + 3 * y - y**2


def inflection_x(y):
    return zero_isocline(y) - 1 / (2 * y - 3)


def integral_curve(y0, xmin=-6, xmax=6, cutoff=9):
    def rhs(x, state):
        return [f(x, state[0])]

    def upper_event(x, state):
        return state[0] - cutoff

    def lower_event(x, state):
        return state[0] + cutoff

    upper_event.terminal = True
    lower_event.terminal = True
    upper_event.direction = 0
    lower_event.direction = 0

    pieces = []
    for finish in (xmin, xmax):
        solution = solve_ivp(
            rhs, (0, finish), [y0],
            events=(upper_event, lower_event),
            max_step=0.018, rtol=1e-9, atol=1e-11,
            dense_output=True,
        )
        if not solution.success:
            raise RuntimeError(f"Не вдалося проінтегрувати з y(0)={y0}: {solution.message}")
        xs = np.linspace(0, solution.t[-1], max(70, int(abs(solution.t[-1]) * 130)))
        ys = solution.sol(xs)[0]
        pieces.append((xs, ys))

    x = np.concatenate((pieces[0][0][::-1], pieces[1][0][1:]))
    y = np.concatenate((pieces[0][1][::-1], pieces[1][1][1:]))
    return x, y


def print_analysis():
    print("ЛАБОРАТОРНА РОБОТА №1 | ЗАДАЧА 1 | ВАРІАНТ 1")
    print("Рівняння: y' = f(x,y) = y² - 3y + x - 2")
    print("1. Поле напрямків: (m, n/2), m = -6,...,6, n = -10,...,10.")
    print("2. y'=0: x = 2+3y-y². Тут y''=f_x=1>0:")
    print("   множина точок максимуму = ∅; крива y'=0 є множиною мінімумів.")
    print("3. Ізокліни: x = k+2+3y-y², k = -3/2, -1, -1/2, 1/2, 1, 3/2.")
    print("4. Зростання: x > 2+3y-y²; спадання: x < 2+3y-y².")
    print("5. y'' = 1 + (2y-3)(y²-3y+x-2).")
    print("   Перегини: x = 2+3y-y² - 1/(2y-3), y != 3/2.")
    print("   Тут y''' = 2(y')² > 0, тому це справжні точки перегину.")
    print("6. Опуклість вгору (за умовою: y''<0):")
    print("   y<3/2: x > 2+3y-y² - 1/(2y-3);")
    print("   y>3/2: x < 2+3y-y² - 1/(2y-3).")
    print("   При y=3/2 друга похідна =1>0, ця пряма не входить.")
    print("7. Початкові точки та нахили:")
    for y0 in (-2, 0, 1):
        print(f"   (0,{y0:+g}): y'(0)={f(0,y0):g}, y''(0)={fxx(0,y0):g}")


def draw_plot():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(12.8, 9.1), dpi=160)

    xg = np.linspace(-6, 6, 540)
    yg = np.linspace(-5, 5, 460)
    xx, yy = np.meshgrid(xg, yg)
    ff, second = f(xx, yy), fxx(xx, yy)

    ax.contourf(xx, yy, ff, levels=[-1e6, 0, 1e6],
                colors=["#f8bbd0", "#a9dfed"], alpha=0.25)
    ax.contourf(xx, yy, second, levels=[-1e6, 0],
                colors=["#f7d85b"], alpha=0.27)

    for m in range(-6, 7):
        for n in range(-10, 11):
            y = n / 2
            slope = f(m, y)
            dx = 0.29 / np.hypot(1, slope)
            dy = slope * dx
            ax.plot([m - dx / 2, m + dx / 2],
                    [y - dy / 2, y + dy / 2],
                    color="#33373c", lw=0.65, alpha=0.7, zorder=2)

    ks = [-1.5, -1, -0.5, 0.5, 1, 1.5]
    isos = ax.contour(xx, yy, ff, levels=ks, colors="#52565d",
                      linewidths=0.82, linestyles="dashed", alpha=0.74)
    ax.clabel(isos, fmt=lambda val: f"k={val:g}", fontsize=7, inline=True)

    ax.contour(xx, yy, ff, levels=[0], colors=["#1c498d"], linewidths=2.15)
    ax.contour(xx, yy, second, levels=[0], colors=["#25834d"], linewidths=2.0)

    curve_colors = { -2: "#e07818", 0: "#8c4dbe", 1: "#cd354b" }
    for y0, color in curve_colors.items():
        xi, yi = integral_curve(y0)
        ax.plot(xi, yi, color=color, lw=2.65, zorder=6)
        ax.scatter([0], [y0], s=51, facecolors="white",
                   edgecolors=color, linewidths=2.4, zorder=7)

    ax.axhline(0, color="#343b46", lw=1.1)
    ax.axvline(0, color="#343b46", lw=1.1)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-5, 5)
    ax.set_xticks(np.arange(-6, 7))
    ax.set_yticks(np.arange(-5, 6))
    ax.grid(alpha=0.12, lw=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y", rotation=0, labelpad=13)
    ax.set_title("Задача 1, варіант 1: y′ = y² − 3y + x − 2\n"
                 "Множина максимумів порожня; синя крива — точки мінімумів",
                 pad=15, fontsize=13)

    handles = [
        Line2D([0], [0], color="#33373c", lw=1.3, label="Поле напрямків"),
        Line2D([0], [0], color="#52565d", ls="--", label="Ізокліни k = ±½, ±1, ±3/2"),
        Line2D([0], [0], color="#1c498d", lw=2.1, label="y′ = 0 (точки мінімумів)"),
        Line2D([0], [0], color="#25834d", lw=2.1, label="y″ = 0 (точки перегину)"),
        Patch(facecolor="#a9dfed", alpha=0.6, label="Зростання: y′ > 0"),
        Patch(facecolor="#f8bbd0", alpha=0.6, label="Спадання: y′ < 0"),
        Patch(facecolor="#f7d85b", alpha=0.7, label="Опуклість вгору: y″ < 0"),
    ] + [Line2D([0], [0], color=color, lw=2.5,
                label=f"Інтегральна крива y(0) = {y0}")
         for y0, color in curve_colors.items()]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=9,
               frameon=True, bbox_to_anchor=(0.50, 0.014))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.89, bottom=0.21)
    return fig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", nargs="?", const="t1.png", default=None,
                        metavar="FILE", help="зберегти графік у PNG")
    args = parser.parse_args()
    print_analysis()
    fig = draw_plot()
    if args.save is not None:
        target = Path(args.save)
        fig.savefig(target, dpi=200, facecolor="white")
        print(f"Графік збережено: {target.resolve()}")
        plt.close(fig)
    else:
        plt.show()


if __name__ == "__main__":
    main()
