from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

out = Path.cwd() / 'figure_replay_outputs'
out.mkdir(parents=True, exist_ok=True)
plt.style.use(Path(__file__).resolve().parent / 'academic.mplstyle')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'svg.fonttype': 'none', 'pdf.fonttype': 42})
blue, teal, purple, orange, ink = '#24577C', '#237B75', '#6C6295', '#C77A2B', '#263238'
fig = plt.figure(figsize=(7.1, 4.8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
ax.text(.03, .95, 'Descriptive evidence categories', fontsize=12, fontweight='bold', color=ink)
ax.text(.03, .90, 'Not a mandatory sequence', fontsize=9, fontweight='bold', color=ink)
ax.text(.03, .855, 'Classify the claim and the tested use; report missing design attributes.', color=ink)
ax.text(.03, .79, 'Distinct evaluation designs (Tiers 0–2)', fontsize=9, fontweight='bold', color=ink)
blocks = [
    (.03, blue, 'Tier 0', 'Internal evaluation', 'Held-out records within\nthe development source'),
    (.345, teal, 'Tier 1', 'External or temporal test', 'Document source, date,\noverlap and assay match'),
    (.66, purple, 'Tier 2', 'Prospective evaluation', 'Freeze the model and rule;\nrecord new measurements\nand blinding status'),
]
for x, color, tier, heading, body in blocks:
    ax.add_patch(Rectangle((x, .49), .28, .25, facecolor=color, edgecolor='none'))
    ax.text(x + .015, .695, tier, color='white', fontsize=10, fontweight='bold')
    ax.text(x + .015, .645, heading, color='white', fontsize=8.2, fontweight='bold')
    ax.text(x + .015, .60, body, color='white', fontsize=8, va='top', linespacing=1.45)
ax.text(.03, .445, 'Parallel placement does not imply equivalent evidential strength.', fontsize=7.7, color=ink)
ax.text(.03, .39, 'Across categories: uncertainty, calibration, domain retention and assay repeatability', fontweight='bold', color=ink)
ax.add_patch(Rectangle((.03, .17), .91, .16, facecolor='#F3F0E9', edgecolor=orange, lw=1))
ax.text(.045, .287, 'Tier 3  Regulatory use for a named context', fontweight='bold', fontsize=9, color=ink)
ax.text(.045, .239, 'Separate regulatory status', fontweight='bold', fontsize=8, color=ink)
ax.text(.045, .195, 'Assessment follows the applicable pathway; it is not an automatic next step or a universal model certificate.', fontsize=7.6, color=ink)
ax.text(.03, .105, 'Different pathways: ICH M7 impurity assessment; E14/S7B integrated cardiac risk assessment.', fontsize=7.5, color=ink)
ax.text(.03, .045, 'Ranking, paired change and candidate selection need their own comparators. No endpoint-wide tier is assigned.', fontsize=7.5, color=ink)
for ext in ('png', 'pdf', 'svg'):
    fig.savefig(out / f'Figure_5.{ext}', dpi=360, facecolor='white', bbox_inches='tight', pad_inches=.08)
plt.close(fig)
