from pathlib import Path
import csv, json

BUILD = Path(__file__).resolve().parent
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = Path.cwd() / 'figure_replay_outputs'
OUT.mkdir(parents=True, exist_ok=True)
DATA = BUILD / 'figure04_source_data.csv'
with DATA.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
for row in rows:
    row['value'] = float(row['value'])

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':8.2, 'axes.titlesize':9.2, 'axes.labelsize':8.5, 'xtick.labelsize':8.2, 'ytick.labelsize':8.2, 'svg.fonttype':'none', 'pdf.fonttype':42, 'axes.spines.top':False, 'axes.spines.right':False, 'figure.facecolor':'white'})
fig, axes = plt.subplots(2, 3, figsize=(7.1, 5.2))
fig.subplots_adjust(left=.09, right=.985, bottom=.17, top=.90, wspace=.56, hspace=.83)
blue, orange = '#3B6F8F', '#CF9650'
def tidy(ax, panel, title, subtitle, ylabel, ymax):
    ax.set_title(panel+'  '+title, loc='left', fontweight='bold', pad=10)
    ax.set_ylabel(ylabel); ax.set_ylim(0, ymax)
    ax.set_axisbelow(True); ax.grid(axis='y', color='#E4E8EB', linewidth=.7)
    ax.tick_params(axis='x', length=0)
def label(ax, bars, offset):
    for bar in bars:
        v = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, v+offset, f'{v:g}', ha='center', va='bottom', fontsize=8.2)

for ax, panel, measure, ylabel, ymax in [(axes[0,0], 'a', 'Mouse microsomal half-life', 'MLM half-life (min)', 360), (axes[0,1], 'b', 'FRET IC50', r'FRET IC$_{50}$ (nM)', 1000)]:
    x = np.arange(2); width=.31
    first = [next(r['value'] for r in rows if r['panel']==panel and r['comparison']==p and r['compound']=='Nearest training compound') for p in ['P1', 'P5']]
    second = [next(r['value'] for r in rows if r['panel']==panel and r['compound']==p) for p in ['P1', 'P5']]
    b1=ax.bar(x-width/2, first, width, color=blue, label='Neighbour')
    b2=ax.bar(x+width/2, second, width, color=orange, label='Generated')
    label(ax,b1,ymax*.018);label(ax,b2,ymax*.018)
    ax.set_xticks(x,['P1','P5'])
    tidy(ax,panel,'METTL3','Retrospective nearest-neighbour comparators',ylabel,ymax)
axes[0,0].legend(loc='upper left',fontsize=8.2,frameon=False,bbox_to_anchor=(-.03,-.17),borderaxespad=0,handlelength=1.1,handletextpad=.45,labelspacing=.25)

ax=axes[0,2]
vals=[next(r['value'] for r in rows if r['panel']=='c' and r['compound'].startswith(c)) for c in ['14 ', '13 ']]
bars=ax.bar([0,1],vals,color=[blue,orange],width=.55)
label(ax,bars,130);ax.set_xticks([0,1],['14\nIntermediate','13\nTarget'])
tidy(ax,'c',r'A$_{2A}$','Synthetic intermediate and target',r'hA$_{2A}$ $K_i$ (nM)',7100)

ax=axes[1,0];x=np.arange(3);width=.31
for i,comp in enumerate(['2','5']):
    vals=[next(r['value'] for r in rows if r['panel']=='d' and r['compound']==comp and r['measure'].startswith(sp)) for sp in ['Human','Rat','Dog']]
    bars=ax.bar(x+(i-.5)*width, vals,width,color=[blue,orange][i],label='Compound '+comp)
    for j,bar in enumerate(bars):
        label(ax,[bar],6.5 if i==1 and j==0 else 1.6)
ax.set_xticks(x,['Human','Rat','Dog'])
tidy(ax,'d','Industrial','Selected project compounds 2 and 5','LM half-life (min)',100)
ax.legend(loc='upper left',fontsize=8.2,frameon=False,bbox_to_anchor=(-.03,-.17),borderaxespad=0,handlelength=1.1,handletextpad=.45,labelspacing=.25)
for ax,panel,ylabel,ymax in [(axes[1,1],'e','MDCK efflux ratio',3.2),(axes[1,2],'f','Target engagement (nM)',150)]:
    vals=[next(r['value'] for r in rows if r['panel']==panel and r['compound']==c) for c in ['2','5']]
    bars=ax.bar([0,1],vals,color=[blue,orange],width=.55);label(ax,bars,ymax*.018)
    ax.set_xticks([0,1],['Cmpd 2','Cmpd 5'])
    tidy(ax,panel,'Industrial','Selected project compounds 2 and 5',ylabel,ymax)
for ext in ['png','pdf','svg']:
    fig.savefig(OUT/('Figure_4.'+ext),dpi=300)
plt.close(fig)
caption = 'Figure 4. Reported measurements across three case studies. (a,b) METTL3 P1 and P5 and their retrospective nearest training neighbours: mouse microsomal half-life and FRET IC50. (c) A2A synthetic intermediate 14 and generated target 13: human A2A Ki. (d–f) Industrial project compounds 2 and 5: species-specific microsomal half-lives, MDCK efflux ratio and target engagement assay. Point estimates are shown without confidence intervals, which were not supplied for these plotted comparisons. Comparator definitions differ; these are not tests of a common selector. The reported METTL3 half-life of 309 min is fitted beyond the 60-min sampling window. A2A PAMPA values are omitted because SI Table S8 does not state the unit. Numerical data are replotted from Matter and Caflisch, Figure 4 (10.1021/acsbiomedchemau.5c00198), Persico et al., Table 1 (10.1021/acs.jmedchem.6c00231), and Rich et al., Table 1 (10.1021/acsmedchemlett.4c00290); all three main articles state CC BY 4.0. The source CSV retains explicitly labelled v13 reference identifiers; DOI identifiers establish the source independently of manuscript numbering.'
(OUT/'Figure_4_caption_and_provenance.txt').write_text(caption+'\n',encoding='utf-8')
print(json.dumps({'outputs':[str(OUT/('Figure_4.'+e)) for e in ['png','pdf','svg']], 'source_csv':str(DATA), 'data_rows':len(rows)},ensure_ascii=False))
