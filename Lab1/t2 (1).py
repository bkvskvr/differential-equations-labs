import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def g(y):
    return (y + 2) * (y + 1)


def constant(y0):
    if y0 == -2:
        raise ValueError("Для y0=-2 є окремий сталий розв'язок")
    return (y0 + 1) / (y0 + 2)


def asymptote(y0):
    if y0 < -2 or y0 > -1:
        return np.log((y0 + 2) / (y0 + 1))
    return None


def maximal_interval(y0):
    star = asymptote(y0)
    if star is None:
        return (-np.inf, np.inf)
    return (star, np.inf) if y0 < -2 else (-np.inf, star)


def solution(x, y0):
    x = np.asarray(x, dtype=float)
    if y0 in (-2, -1):
        return np.full_like(x, y0)
    C = constant(y0)
    low, high = maximal_interval(y0)
    within = (x > low) & (x < high)
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        result = -2 + 1 / (1 - C * np.exp(x))
    return np.where(within, result, np.nan)


def threshold():
    t = (3998 + np.sqrt(3998**2 + 12)) / 6
    return np.log(t)


def print_analysis():
    print("ЛАБОРАТОРНА РОБОТА №1 | ЗАДАЧА 2 | ВАРІАНТ 1")
    print("Рівняння: y' = g(y) = y²+3y+2 = (y+2)(y+1)")
    print("1. Векторне поле на прямій y (початок -> кінець):")
    for y0 in (-4, -3, -2, -1, 0, 1, 2, 3, 4):
        print(f"   y={y0:2d}: g(y)={g(y0):2d}; {y0:2d} -> {y0+g(y0):2d}")
    print("2. Стаціонарні розв'язки: y=-2 і y=-1.")
    print("   Зростають при y<-2 та y>-1, спадають при -2<y<-1.")
    print("   y'' = (2y+3)(y+2)(y+1).")
    print("   Справжні точки перегину НЕсталих кривих: y=-3/2.")
    print("   Рівні y=-2 і y=-1 дають сталі криві, це НЕ перегини.")
    print("3. 1/[(y+2)(y+1)] = 1/(y+1)-1/(y+2).")
    print("   ln|(y+1)/(y+2)| = x + const;")
    print("   y(x,y0) = -2 + 1/[1 - ((y0+1)/(y0+2))*exp(x)], y0 != -2.")
    print("   y(x,-2)=-2; y(x,-1)=-1.")
    print("   y0<-2:  x*=ln((y0+2)/(y0+1))<0; I=(x*,+∞).")
    print("   -2<=y0<=-1: I=R.")
    print("   y0>-1:  x*=ln((y0+2)/(y0+1))>0; I=(-∞,x*).")
    print("4. Графіки: y0=-3, -2, -3/2, -1, 0 (по різних областях).")
    print("5. Межа b=-2 (стійка рівновага).")
    print("   y+(x)=y(x,-3/2)=-2+1/(1+e^x);")
    print("   y-(x)=y(x,-5/2)=-2+1/(1-3e^x).")
    print("   |y+(x)-y-(x)|=4e^x/[(1+e^x)(3e^x-1)], x>=0.")
    print("   Для <10^-3: 3t²-3998t-1>0, t=e^x>=1.")
    print("   Отже, x > ln((3998+sqrt(3998²+12))/6).")
    xcrit = threshold()
    print(f"   Числовий поріг x > {xcrit:.9f}.")
    for test_x in (0, xcrit, xcrit + 0.001, 8):
        gap = abs(solution(test_x, -1.5) - solution(test_x, -2.5))
        print(f"   x={test_x:.9f}: |y+ - y-| = {gap:.12f}")


def draw_plot():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig = plt.figure(figsize=(13.2, 10.1), dpi=160)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.91, 1.10], hspace=0.38, wspace=0.27)
    ax1, ax2, ax3 = (fig.add_subplot(gs[0, :]),
                     fig.add_subplot(gs[1, 0]),
                     fig.add_subplot(gs[1, 1]))

    samples = [-4, -3, -2, -1.5, -1, 0, 1, 2, 3, 4]
    for row, y0 in enumerate(samples):
        val = g(y0)
        color = "#197b58" if val > 0 else ("#c43f49" if val < 0 else "#304b89")
        ax1.plot([-4.7, 35.1], [row, row], color="#e6e8ed", lw=0.65, zorder=0)
        ax1.scatter([y0], [row], color=color, s=25, zorder=3)
        if abs(val) > 1e-12:
            ax1.annotate("", xy=(y0 + val, row), xytext=(y0, row),
                         arrowprops={"arrowstyle": "-|>", "lw": 2.0,
                                     "color": color, "mutation_scale": 11})
        else:
            ax1.scatter([y0], [row], s=68, facecolors="white",
                        edgecolors=color, linewidths=1.8, zorder=3)
        ax1.text(35.7, row, f"{y0:g} → {y0 + val:g}", va="center", fontsize=9,
                 color="#353b48")
    ax1.set_yticks(range(len(samples)), [f"y={y:g}" for y in samples])
    ax1.set_xlim(-5.2, 42.0)
    ax1.set_ylim(-0.8, len(samples) - 0.2)
    ax1.set_xticks([-4, -2, 0, 5, 10, 15, 20, 25, 30, 35])
    ax1.grid(axis="x", alpha=0.18)
    ax1.set_xlabel("Координата на прямій y (стрілка від y₀ до y₀ + g(y₀))")
    ax1.set_title("1. Векторне поле (y=−1.5 додано для ілюстрації спадання)", pad=10)

    xs = np.linspace(-6, 8.5, 5000)
    for y0, color in [(-3, "#c05b24"), (-2, "#266ba5"),
                      (-1.5, "#7452b5"), (-1, "#25915b"), (0, "#bb3b6a")]:
        values = solution(xs, y0)
        values[np.abs(values) > 6.2] = np.nan
        ax2.plot(xs, values, lw=2.35, color=color, label=f"y(0) = {y0:g}")
        ax2.scatter([0], [y0], s=34, color=color, zorder=4)
        star = asymptote(y0)
        if star is not None:
            ax2.axvline(star, ls=":", color=color, lw=1.15, alpha=0.72)
    ax2.axhline(-1.5, ls="--", color="#8f929b", lw=1.15,
                label="y = −1.5 (рівень перегину)")
    ax2.axvline(0, color="#9ba0a6", lw=0.9)
    ax2.set(xlim=(-6, 8.5), ylim=(-6.2, 5.1), xlabel="x", ylabel="y",
            title="2–4. Розв'язки й вертикальні асимптоти")
    ax2.grid(alpha=0.16)
    ax2.legend(fontsize=8, loc="upper right", framealpha=0.95)

    crit = threshold()
    xs = np.linspace(0, 9.2, 1000)
    upper = solution(xs, -1.5)
    lower = solution(xs, -2.5)
    ax3.plot(xs, upper, color="#7f4ac0", lw=2.5, label="y(x, b+1/2), b=−2")
    ax3.plot(xs, lower, color="#df7335", lw=2.5, label="y(x, b−1/2), b=−2")
    ax3.axhline(-2, ls="--", color="#236d8b", lw=1.4, label="Стійка рівновага y=−2")
    ax3.axvline(crit, ls=":", color="#252831", lw=1.6,
                label=f"Поріг x* ≈ {crit:.4f}")
    ax3.fill_between(xs, lower, upper, color="#9aa6c8", alpha=0.13)
    ax3.text(crit + 0.10, -2.37, "різниця < 10⁻³", fontsize=9)
    ax3.set(xlim=(0, 9.2), ylim=(-2.65, -1.37), xlabel="x", ylabel="y",
            title="5. Зближення двох розв'язків")
    ax3.grid(alpha=0.16)
    ax3.legend(fontsize=8.5, loc="upper right", framealpha=0.95)

    fig.suptitle("Задача 2, варіант 1: y′ = (y + 2)(y + 1)", fontsize=15, y=0.993)
    fig.subplots_adjust(top=0.92, bottom=0.075, left=0.09, right=0.97)
    return fig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", nargs="?", const="t2.png", default=None,
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
