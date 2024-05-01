import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from src.simulator.simulation import Simulation
from src.systems.base_system import BaseSystem
from src.systems.computed_system import ComputedSystem


def make_3D_figure(save_filename):
    fig = plt.figure()
    axs = [fig.add_subplot(3, 2, i, projection="3d") for i in range(1,7)]
    zipper = zip(
        axs,
        ["L1_tracking_5", "L2", "L3_longer", "L4_longer", "L5", "L2"],
        ["a)", "b)", "c)", "d)", "e)", "f)"]
    )

    best_bodies_info = []
    for ax, name, letter in list(zipper)[:]:
        current_sim = Simulation.load_from_folder(f"simulations/{name}")
        if name in ["L1_tracking_5", "L2", "L3"]:
            factors = (1, 1e3)
            ax.set_xlabel(r"$D_{\odot x}$ [Gm]")
            ax.set_ylabel(r"$D_{\odot y}$ [Mm]")
        else:
            factors = (1, 1)
            ax.set_xlabel(r"$D_{\odot x}$ [Gm]")
            ax.set_ylabel(r"$D_{\odot y}$ [Gm]")
        
        if letter == "f)":
            plot_best_body = False
        else:
            plot_best_body = True
        
        best_bodies_info.append(current_sim.system.create_subplot(axis=ax, multiplication_factors=factors, bar3d=True,
                                plot_best_body=plot_best_body))
        ax.set_zlabel(r"$t_{survie}$ [a]")
        ax.set_title(letter, loc="left")
        ax.xaxis.set_major_locator(MaxNLocator(3))
        ax.yaxis.set_major_locator(MaxNLocator(3))
        ax.zaxis.set_major_locator(MaxNLocator(4))
        # plt.show()

    fig.set_size_inches(7.5, 9)
    fig.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
    plt.savefig(save_filename, dpi=600)
    # plt.show()
    print(np.array(best_bodies_info))


# make_3D_figure("figures/3d_survival_time.png")


def make_2D_figure(save_filename, split_figures: bool=False):
    fig = plt.figure()
    axs = [fig.add_subplot(3, 2, i) for i in range(1,7)]
    zipper = zip(
        axs,
        ["L1_tracking_5", "L2", "L3_longer", "L4_longer", "L5", "L2"],
        ["a)", "b)", "c)", "d)", "e)", "f)"]
    )

    best_bodies_info = []
    for ax, name, letter in list(zipper)[:]:
        current_sim = Simulation.load_from_folder(f"simulations/{name}")
        if name in ["L1_tracking_5", "L2", "L3"]:
            factors = (1, 1e3)
            ax.set_ylabel(r"$D_{\odot y}$ [Mm]")
        else:
            factors = (1, 1)
            ax.set_ylabel(r"$D_{\odot y}$ [Gm]")
        
        if letter == "f)":
            plot_best_body = False
        else:
            plot_best_body = True
        
        best_bodies_info.append(current_sim.system.create_subplot(axis=ax, multiplication_factors=factors, bar3d=False,
                                plot_best_body=plot_best_body, cbar_label=r"$t_{survie}$ [a]"))
        
        x_limits = ax.get_xlim()
        y_limits = ax.get_ylim()

        if letter == "a)":
            L1_pos = 450 - 299.42158947147351000240
            ax.plot([L1_pos, L1_pos], y_limits, "k-", alpha=0.75)

        if letter == "b)" or letter == "f)":
            L2_pos = 450 - 296.37841052852644452287
            ax.plot([L2_pos, L2_pos], y_limits, "k-", alpha=0.75)

        if letter == "c)":
            L3_pos = 602.10064717686748281267 - 450
            ax.plot([L3_pos, L3_pos], y_limits, "k-", alpha=0.75)

        if letter == "d)" or letter == "e)":
            earth_pos = 450 - 297.90
            orbit = lambda x: (earth_pos**2 - x**2)**0.5
            x_space = np.linspace(*x_limits, 100)
            ax.plot(x_space, orbit(x_space), "k-", alpha=0.75)

        ax.set_title(letter, loc="left")
        ax.xaxis.set_major_locator(MaxNLocator(3))
        ax.yaxis.set_major_locator(MaxNLocator(3))
        # plt.show()
        if split_figures: ax.set_xlabel(r"$D_{\odot x}$ [Gm]")

    if not split_figures: fig.supxlabel(r"$D_{\odot x}$ [Gm]")
    fig.set_size_inches(7.5, 9)
    fig.subplots_adjust(left=0.1, right=1, top=0.9, bottom=0.1)
    plt.tight_layout()
    # plt.show()
    plt.savefig(save_filename, dpi=600)
    print(np.array(best_bodies_info))


# make_2D_figure("figures/2d_survival_time_r.png", split_figures=True)


def make_distances_figure(filename):
    fig, axs = plt.subplots(3, 1)
    names = [
        ["L1_tracking_5", "L2"],
        ["L3_longer"],
        ["L4_longer", "L5"]
    ]
    letters = ["a)", "b)", "c)"]
    for ax, names, letter in zip(axs, names, letters):
        for i, name in enumerate(names):
            sim = Simulation.load_from_folder(f"simulations/{name}", only_load_best_body=True)
            delta_time = int(sim.system.info["delta_time"])
            save_freq = int(sim.system.info["positions_saving_frequency"])

            b_pos = np.array(sim.system.list_of_bodies[-1].positions)
            L1_pos = np.array(sim.system.fake_bodies[0].positions)[:b_pos.shape[0],:]
            dists = np.sum((L1_pos - b_pos)**2, axis=1)**0.5
            
            times = np.arange(dists.shape[0]) * delta_time * save_freq / (8766*3600)
            if i == 0:
                ax.plot(times, dists, "m-", label=name[:2], linewidth=1)
            else:
                ax.plot(times, dists, "g-", label=name[:2], linewidth=1)
        
        ax.set_title(letter, loc="left")
        ax.tick_params(direction="in")
        # ax.legend(loc="upper left")

    fig.supxlabel("Temps [a]")
    fig.supylabel("Distance entre le meilleur corps\net le point de Lagrange [Gm]")
    fig.set_size_inches(7.5, 5)
    plt.tight_layout()
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    # plt.show()
 

# make_distances_figure("figures/distances.png")


def make_chaos_figure(filename):
    fig, axs = plt.subplots(1, 3)
    for ax, name, letter in zip(axs, ["start", "middle", "end"], ["a)", "b)", "c)"]):
        image = plt.imread(f"figures/chaos/{name}.png")
        ax.imshow(image[135:-155,115:-115])
        ax.axis("off")
        ax.set_title(letter, loc="left")
    fig.set_size_inches(7.5,3)
    fig.tight_layout()
    plt.savefig(filename, dpi=600, bbox_inches="tight")
    # plt.show()


# make_chaos_figure("figures/chaos.png")
