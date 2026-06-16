import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "report_diagrams")
MPLCONFIG = os.path.join(BASE_DIR, ".mplconfig")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MPLCONFIG, exist_ok=True)
os.environ["MPLCONFIGDIR"] = MPLCONFIG

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates


BG = "#F7FAFC"
BOX = "#E8F1FF"
BOX_ALT = "#E9F9F2"
BOX_DARK = "#DDEBFF"
BORDER = "#2C5282"
TEXT = "#1A202C"
ARROW = "#2D3748"
ACCENT = "#2F855A"


def setup_ax(fig_w=16, fig_h=9):
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def add_box(ax, x, y, w, h, label, fc=BOX, fontsize=10, lw=1.6):
    rect = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=lw,
        edgecolor=BORDER,
        facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2,
        y + h / 2,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=TEXT,
        wrap=True,
        weight="semibold",
    )


def add_arrow(ax, x1, y1, x2, y2, text=None, text_offset=(0, 0), color=ARROW):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", lw=1.8, color=color, shrinkA=8, shrinkB=8),
    )
    if text:
        ax.text(
            (x1 + x2) / 2 + text_offset[0],
            (y1 + y2) / 2 + text_offset[1],
            text,
            fontsize=9,
            color=TEXT,
            weight="bold",
            ha="center",
            va="center",
        )


def diagram_1_overall_flow():
    fig, ax = setup_ax(16, 6)
    ax.text(
        0.5,
        0.94,
        "SDLC Diagram 1: Overall Project Lifecycle",
        ha="center",
        va="center",
        fontsize=18,
        weight="bold",
        color=TEXT,
    )

    labels = [
        "Requirement\nGathering",
        "Feasibility\nStudy",
        "System\nDesign",
        "Coding and\nDevelopment",
        "Implementation\nand Testing",
        "Build and\nDeployment",
        "Maintenance and\nEnhancement",
    ]
    x0, y, w, h, gap = 0.03, 0.42, 0.12, 0.22, 0.02
    centers = []
    for i, lbl in enumerate(labels):
        x = x0 + i * (w + gap)
        add_box(ax, x, y, w, h, lbl, fc=BOX if i % 2 == 0 else BOX_ALT, fontsize=10)
        centers.append((x + w / 2, y + h / 2))

    arrow_y = y + h - 0.03
    for i in range(len(centers) - 1):
        add_arrow(
            ax,
            centers[i][0] + w / 2 - 0.06,
            arrow_y,
            centers[i + 1][0] - w / 2 + 0.06,
            arrow_y,
        )

    out = os.path.join(OUTPUT_DIR, "sdlc_diagram_1_overall_flow.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def diagram_2_iterative_loop():
    fig, ax = setup_ax(11, 11)
    ax.text(
        0.5,
        0.965,
        "SDLC Diagram 2: Iterative Development Loop",
        ha="center",
        va="center",
        fontsize=18,
        weight="bold",
        color=TEXT,
    )

    add_box(ax, 0.35, 0.83, 0.3, 0.09, "Identify Module Scope")
    add_box(ax, 0.35, 0.70, 0.3, 0.09, "Develop Module", fc=BOX_ALT)
    add_box(ax, 0.35, 0.57, 0.3, 0.09, "Test Module")
    add_box(ax, 0.35, 0.44, 0.3, 0.09, "Fix Issues and Refine", fc=BOX_ALT)
    add_box(ax, 0.35, 0.31, 0.3, 0.09, "Integrate with Main System")

    diamond = patches.Polygon(
        [[0.5, 0.25], [0.68, 0.19], [0.5, 0.13], [0.32, 0.19]],
        closed=True,
        edgecolor=BORDER,
        facecolor=BOX_DARK,
        linewidth=1.6,
    )
    ax.add_patch(diamond)
    ax.text(
        0.5,
        0.19,
        "More Modules\nPending?",
        ha="center",
        va="center",
        fontsize=10,
        color=TEXT,
        weight="semibold",
    )

    add_box(ax, 0.35, 0.04, 0.3, 0.07, "Final Integration Testing", fc=BOX_ALT)
    add_box(ax, 0.70, 0.04, 0.24, 0.07, "Deployment Build", fc=BOX_ALT)

    add_arrow(ax, 0.5, 0.83, 0.5, 0.79)
    add_arrow(ax, 0.5, 0.70, 0.5, 0.66)
    add_arrow(ax, 0.5, 0.57, 0.5, 0.53)
    add_arrow(ax, 0.5, 0.44, 0.5, 0.40)
    add_arrow(ax, 0.5, 0.31, 0.5, 0.25)
    add_arrow(ax, 0.5, 0.13, 0.5, 0.11, text="No", text_offset=(0.05, 0))
    add_arrow(ax, 0.65, 0.075, 0.70, 0.075)

    # Loop back for "Yes"
    ax.annotate(
        "",
        xy=(0.35, 0.87),
        xytext=(0.32, 0.19),
        arrowprops=dict(
            arrowstyle="->",
            lw=1.8,
            color=ARROW,
            connectionstyle="angle3,angleA=180,angleB=90",
        ),
    )
    ax.text(0.24, 0.52, "Yes", fontsize=10, weight="bold", color=ACCENT, rotation=90)

    out = os.path.join(OUTPUT_DIR, "sdlc_diagram_2_iterative_loop.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def diagram_3_deliverables_mapping():
    fig, ax = setup_ax(15, 9)
    ax.text(
        0.5,
        0.95,
        "SDLC Diagram 3: Phase-wise Deliverables Mapping",
        ha="center",
        va="center",
        fontsize=18,
        weight="bold",
        color=TEXT,
    )

    phases = [
        "Requirement\nGathering",
        "Feasibility\nStudy",
        "Design",
        "Coding",
        "Implementation\nand Testing",
        "Build and\nDeployment",
    ]
    outputs = [
        "FR and NFR list,\nproject scope,\nmodule plan",
        "Technical,\noperational and\neconomic feasibility",
        "DFD, ER Diagram,\nUse Case, flowcharts",
        "Flask routes, models,\ntemplates, static assets",
        "Validation scripts,\nmanual test outcomes",
        "Dockerfile, compose setup,\nentry-point workflow",
    ]

    y_start = 0.80
    step = 0.12
    for i, (p, o) in enumerate(zip(phases, outputs)):
        y = y_start - i * step
        add_box(ax, 0.06, y, 0.28, 0.08, p, fc=BOX)
        add_box(ax, 0.46, y, 0.48, 0.08, f"Deliverables:\n{o}", fc=BOX_ALT)
        add_arrow(ax, 0.34, y + 0.04, 0.46, y + 0.04)

    out = os.path.join(OUTPUT_DIR, "sdlc_diagram_3_deliverables_mapping.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def diagram_4_timeline_gantt():
    tasks = [
        ("Requirement Gathering and Analysis", "2025-08-01", "2025-08-20"),
        ("Feasibility Study", "2025-08-21", "2025-08-31"),
        ("DFD ER Use Case and Flow Design", "2025-09-01", "2025-09-20"),
        ("Authentication and Package Modules", "2025-09-21", "2025-10-20"),
        ("Transport and Admin Modules", "2025-10-21", "2025-11-24"),
        ("Chatbot Offer and Support Modules", "2025-11-25", "2025-12-14"),
        ("Verification and Refinement", "2025-12-15", "2026-01-13"),
        ("Dockerized Build and Final Packaging", "2026-01-14", "2026-02-03"),
    ]

    fig, ax = plt.subplots(figsize=(16, 8), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(
        "SDLC Diagram 4: Academic Project Timeline (Gantt View)",
        fontsize=18,
        weight="bold",
        color=TEXT,
        pad=18,
    )

    colors = ["#4299E1", "#63B3ED", "#2B6CB0", "#38A169", "#2F855A", "#276749", "#DD6B20", "#C05621"]

    for i, (name, start, end) in enumerate(tasks):
        s = datetime.fromisoformat(start)
        e = datetime.fromisoformat(end)
        ax.barh(
            y=i,
            width=(e - s).days,
            left=s,
            height=0.62,
            color=colors[i % len(colors)],
            edgecolor="#1A202C",
            linewidth=0.7,
        )

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in tasks], fontsize=10)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.set_xlabel("Timeline", fontsize=11, color=TEXT, weight="semibold")

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#4A5568")

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "sdlc_diagram_4_timeline_gantt.png")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def main():
    outputs = [
        diagram_1_overall_flow(),
        diagram_2_iterative_loop(),
        diagram_3_deliverables_mapping(),
        diagram_4_timeline_gantt(),
    ]
    print("Generated SDLC diagrams:")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
