import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ============================================================
#  DATA
# ============================================================

sex = {
    # Gen 4 children
    "Victoriah Joson": "F",
    "Aurelio Joson (also Jr.)": "M",
    "Jing Joson": "M",
    "Vincent Joson": "M",
    "Mary Joson": "F",

    "Suzette (Jesuzette) Joson": "F",
    "Vito Joson": "M",
    "Joseph Joson (Jojo)": "M",
    "Judith Joson": "F",
    "Joey Joson": "M",
    "Joel Joson": "M",
    "Jorge Joson": "M",
    "Julius Joson (Jay)": "M",
    "Jhannete Joson": "F",
    "Jenny Joson": "F",

    "Dennis Joson": "M",
    "Bernard Joson": "M",
    "Gina Joson": "F",

    "Westmont Joson": "M",
    "Lerie Joson": "F",
    "Mon Joson": "M",
    "Joy Joson": "F",
    "Sheryl Joson": "F",
    "Mayra Joson": "F",
    "Wyeth Joson": "M",

    "Jizzle Joson": "F",
    "Jillian Joson": "F",

    # Gen 3 parents
    "Aurelio Joson": "M",
    "Nita Joson": "F",

    "Domingo Joson": "M",
    "Apolonia Joson": "F",

    "Consolacion Joson": "F",

    "Angel Joson (Jr.)": "M",
    "Nena Joson": "F",

    "Remie Joson": "M",
    "Malaya Joson": "F",

    "Pete Joson": "M",
    "Evelyn Joson": "F",

    # Domingo Gen4 spouses
    "I don't remember the name (Suzette husband)": "M",
    "I don't remember the name (Vito spouse)": "F",
    "I don't remember the name (Jenny spouse)": "M",

    "Chona Joson": "F",
    "Chris Manuel": "M",

    # Domingo → GEN5 kids (your data)
    "Jason": "M",
    "Joshua": "M",
    "I don't remember the name (3rd Suzette son)": "M",

    "Pauline": "F",
    "Kim": "F",

    "Anthony": "M",
    "Alexis": "F",

    "CJ": "M",
    "Jhazmin": "F",
    "Jhanelle": "F",

    "Louis": "M",
    "I don't remember Jenny son name": "M",

    # Gen 2
    "Angel Joson": "M",
    "Primitiva Joson": "F",

    # Gen 1
    "Santiago Joson": "M",
    "Gertrudes Joson": "F",
}

# children[(parent1, parent2)] = [...] lists kids
children = {
    ("Aurelio Joson", "Nita Joson"): [
        "Victoriah Joson",
        "Aurelio Joson (also Jr.)",
        "Jing Joson",
        "Vincent Joson",
        "Mary Joson",
    ],

    ("Domingo Joson", "Apolonia Joson"): [
        "Suzette (Jesuzette) Joson",
        "Vito Joson",
        "Joseph Joson (Jojo)",
        "Judith Joson",
        "Joey Joson",
        "Joel Joson",
        "Jorge Joson",
        "Julius Joson (Jay)",
        "Jhannete Joson",
        "Jenny Joson",
    ],

    ("Angel Joson (Jr.)", "Nena Joson"): [
        "Dennis Joson",
        "Bernard Joson",
        "Gina Joson",
    ],

    ("Remie Joson", "Malaya Joson"): [
        "Westmont Joson",
        "Lerie Joson",
        "Mon Joson",
        "Joy Joson",
        "Sheryl Joson",
        "Mayra Joson",
        "Wyeth Joson",
    ],

    ("Pete Joson", "Evelyn Joson"): [
        "Jizzle Joson",
        "Jillian Joson",
    ],

    # GEN5 children for Domingo → GEN4 individuals
    ("Suzette (Jesuzette) Joson", "I don't remember the name (Suzette husband)"): [
        "Jason", "Joshua", "I don't remember the name (3rd Suzette son)"
    ],
    ("Vito Joson", "I don't remember the name (Vito spouse)"): [
        "Pauline", "Kim"
    ],
    ("Julius Joson (Jay)", "Chona Joson"): [
        "Anthony", "Alexis"
    ],
    ("Jhannete Joson", "Chris Manuel"): [
        "CJ", "Jhazmin", "Jhanelle"
    ],
    ("Jenny Joson", "I don't remember Jenny spouse"): [
        "Louis", "I don't remember Jenny son name"
    ],
}

ROOT_COUPLE = ("Santiago Joson", "Gertrudes Joson")
GEN2_COUPLE = ("Angel Joson", "Primitiva Joson")

GEN3_FAMILIES = [
    ("Aurelio Joson", "Nita Joson"),
    ("Domingo Joson", "Apolonia Joson"),
    ("Consolacion Joson", None),
    ("Angel Joson (Jr.)", "Nena Joson"),
    ("Remie Joson", "Malaya Joson"),
    ("Pete Joson", "Evelyn Joson"),
]

# ============================================================
# LAYOUT CONSTANTS
# ============================================================

BOX_W = 9.0
BOX_H = 2.6
SPOUSE_DY = 3.0
CHILD_DY = 4.0
FAMILY_GAP = 6.0

X_GEN1 = 0.0
X_GEN2 = 25.0
X_GEN3 = 50.0
X_GEN4 = 75.0
X_GEN5 = 100.0

P2M = 2.0   # parent to marriage node
M2T = 4.0   # marriage node to trunk

# ============================================================
# DRAWING HELPERS
# ============================================================

def draw_person(ax, name, pos):
    x, y = pos
    color = "#8fc1ff" if sex.get(name) == "M" else "#ffb3d9"
    rect = FancyBboxPatch(
        (x - BOX_W/2, y - BOX_H/2),
        BOX_W, BOX_H,
        boxstyle="round,pad=0.2",
        linewidth=1, edgecolor="black",
        facecolor=color
    )
    ax.add_patch(rect)
    ax.text(x, y, name, ha="center", va="center", fontsize=7)


def child_anchor(c, positions):
    """Return where a trunk should plug into."""
    if isinstance(c, tuple):
        p1, p2 = c
        if p2 is None or p2 not in positions:
            return positions[p1]
        return (positions[p1][0], (positions[p1][1] + positions[p2][1]) / 2)
    else:
        return positions[c]

# ============================================================
# CONNECT FAMILIES CLEANLY
# ============================================================

def connect_family(ax, parents, kids, positions):

    # ---------- Marriage Node ----------
    if isinstance(parents, tuple):
        p1, p2 = parents
        x = positions[p1][0]
        y1 = positions[p1][1]

        if p2 is not None and p2 in positions:
            y2 = positions[p2][1]
            mx = x + BOX_W/2 + P2M

            ax.plot([x+BOX_W/2, mx], [y1, y1], color="black")
            ax.plot([x+BOX_W/2, mx], [y2, y2], color="black")
            ax.plot([mx, mx], [y2, y1], color="black")

            y_mid = (y1 + y2)/2
        else:
            mx = x + BOX_W/2 + P2M
            ax.plot([x+BOX_W/2, mx], [y1, y1], color="black")
            y_mid = y1

    else:
        p = parents
        x, y_mid = positions[p]
        mx = x + BOX_W/2 + P2M
        ax.plot([x+BOX_W/2, mx], [y_mid, y_mid], color="black")

    # ---------- Children Trunk ----------
    trunk_x = mx + M2T
    anchors = [child_anchor(c, positions) for c in kids]
    ys = [y for (_, y) in anchors]

    min_y = min(ys + [y_mid])
    max_y = max(ys + [y_mid])

    ax.plot([mx, trunk_x], [y_mid, y_mid], color="black")
    ax.plot([trunk_x, trunk_x], [min_y, max_y], color="black")

    # lines out to each child box
    for cx, cy in anchors:
        child_left = cx - BOX_W/2
        ax.plot([trunk_x, child_left], [cy, cy], color="black")

# ============================================================
# POSITIONING
# ============================================================

def compute_positions():
    positions = {}

    current_y = 0.0
    family_center = {}

    # ---------- GEN3 + GEN4 ----------
    for parents in GEN3_FAMILIES:
        p1, p2 = parents
        kids = children.get(parents, [])

        if not kids:   # Consolacion
            positions[p1] = (X_GEN3, current_y)
            family_center[parents] = current_y
            current_y -= (BOX_H + FAMILY_GAP)
            continue

        # place GEN4 kids
        n = len(kids)
        height = (n - 1)*CHILD_DY
        top_y = current_y
        kid_ys = [top_y - i*CHILD_DY for i in range(n)]

        for k, y in zip(kids, kid_ys):
            positions[k] = (X_GEN4, y)

        center_y = (kid_ys[0] + kid_ys[-1]) / 2
        positions[p1] = (X_GEN3, center_y + SPOUSE_DY/2)
        if p2:
            positions[p2] = (X_GEN3, center_y - SPOUSE_DY/2)

        family_center[parents] = center_y
        current_y = kid_ys[-1] - FAMILY_GAP

    # ---------- GEN2 ----------
    import statistics
    gen2_center = statistics.mean(family_center[p] for p in GEN3_FAMILIES)
    positions[GEN2_COUPLE[0]] = (X_GEN2, gen2_center + SPOUSE_DY/2)
    positions[GEN2_COUPLE[1]] = (X_GEN2, gen2_center - SPOUSE_DY/2)

    # ---------- GEN1 ----------
    positions[ROOT_COUPLE[0]] = (X_GEN1, gen2_center + SPOUSE_DY/2)
    positions[ROOT_COUPLE[1]] = (X_GEN1, gen2_center - SPOUSE_DY/2)

    # ---------- GEN5 (children of GEN4 parents) ----------
    for (p1, p2), kids in children.items():
        if p1 in positions and positions[p1][0] == X_GEN4:

            px, py = positions[p1]

            # place spouse if missing
            if p2 and p2 not in positions:
                positions[p2] = (px, py - SPOUSE_DY)

            # place GEN5 kids to the right
            for i, kid in enumerate(kids):
                positions[kid] = (X_GEN5, py - i*CHILD_DY)

    return positions

# ============================================================
# MAIN DRAWING
# ============================================================

def build_pedigree(output="joson_pedigree.png"):
    positions = compute_positions()

    fig, ax = plt.subplots(figsize=(20, 14))

    for name, pos in positions.items():
        draw_person(ax, name, pos)

    # GEN1 → GEN2
    connect_family(ax, ROOT_COUPLE, [GEN2_COUPLE], positions)

    # GEN2 → GEN3
    connect_family(ax, GEN2_COUPLE, GEN3_FAMILIES, positions)

    # GEN3 → GEN4
    for parents in GEN3_FAMILIES:
        kids = children.get(parents, [])
        if kids:
            connect_family(ax, parents, kids, positions)

    # GEN4 → GEN5
    for parents, kids in children.items():
        if parents[0] in positions and positions[parents[0]][0] == X_GEN4:
            connect_family(ax, parents, kids, positions)

    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.show()

    print(f"Saved pedigree to {output}")


if __name__ == "__main__":
    build_pedigree()
