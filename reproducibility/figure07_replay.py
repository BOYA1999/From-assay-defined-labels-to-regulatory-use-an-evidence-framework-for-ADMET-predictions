from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

ROOT = Path(__file__).resolve().parent
OUT = Path.cwd() / 'figure07_replay_outputs'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
INK='#203647'; BLUE='#37758F'; PALE='#EAF2F6'; ORANGE='#BC7946'; GREY='#73828B'; EDGE='#B9CCD5'


def canvas(lang,title,height=5.15):
    fig=plt.figure(figsize=(7.2,height),facecolor='white')
    ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    font=FontProperties(family='DejaVu Sans')
    def text(x,y,s,size=8.2,bold=False,ha='left',color=INK,va='center'):
        return ax.text(x,y,s,fontproperties=font,fontsize=size,fontweight='bold' if bold else 'normal',ha=ha,va=va,color=color,linespacing=1.35)
    text(.04,.957,title,11,True)
    return fig,ax,text,font

def save(fig,num,lang):
    stem=OUT/f'figure{num:02d}_{lang}'
    fig.savefig(str(stem)+'.png',dpi=600,metadata={'Software':'Scientific figure'})
    fig.savefig(str(stem)+'.svg')
    fig.savefig(str(stem)+'.pdf',metadata={'Creator':'Scientific figure','Author':''})
    plt.close(fig)

def fig8(lang):
    zh=lang=='zh'
    data=json.loads((ROOT/'figure07_plot_data.json').read_text(encoding='utf-8'))
    rows={r['compound_id']:r for r in data['all_five_compounds']}
    fig,ax,t,font=canvas(lang,'工业优化案例中的实测多属性取舍' if zh else 'Measured property trade-offs in an industrial optimization case',4.15)
    t(.04,.872,'a  肝微粒体半衰期' if zh else 'a  Liver microsomal half-life',9,True)
    t(.555,.872,'b  MDCK外排比' if zh else 'b  MDCK efflux ratio',8.6,True)
    t(.794,.867,'c  靶标作用读数' if zh else 'c  Target engagement\n    assay readout',8.3,True)
    specs=[([.085,.22,.38,.54],['HLM_t_half_min','RLM_t_half_min','dog_LM_t_half_min'],['人','大鼠','犬'] if zh else ['Human','Rat','Dog'],100,'min'),([.58,.22,.14,.54],['MDCK_ER'],[''],3.2,'比值' if zh else 'Ratio'),([.82,.22,.14,.54],['target_engagement_nM'],[''],150,'nM')]
    for j,(rect,fields,labs,top,unit) in enumerate(specs):
        q=fig.add_axes(rect);q.set_ylim(0,top);q.spines[['top','right']].set_visible(False);q.spines[['left','bottom']].set_color(EDGE);q.tick_params(labelsize=7,length=2,color=EDGE)
        for k,f in enumerate(fields):
            for ident,shift,color,marker in [('2',-.12,BLUE,'o'),('5',.12,ORANGE,'s')]:
                val=rows[ident][f];xx=k+shift
                q.plot([xx,xx],[0,val],color=color,alpha=.28,lw=1.4)
                q.scatter([xx],[val],color=color,marker=marker,s=24,zorder=3)
                q.text(xx,val+top*.065,str(val),ha='center',va='center',fontproperties=font,fontsize=7.4,color=color)
        q.set_xlim(-.42,len(fields)-.58 if len(fields)>1 else .42)
        q.set_xticks(range(len(fields)),labs,fontproperties=font,fontsize=7.4)
        q.set_ylabel(unit,fontproperties=font,fontsize=7.4,labelpad=3)
        if j:q.set_xticks([-.12,.12],['2','5'],fontproperties=font,fontsize=7.3)
        q.yaxis.grid(True,color='#E9EFF2',lw=.5);q.set_axisbelow(True)
        for tick in q.get_yticklabels():tick.set_fontproperties(font);tick.set_fontsize(7)
    ax.scatter([.15],[.134],c=BLUE,s=25,marker='o');t(.177,.134,'化合物2' if zh else 'Compound 2',7.8)
    ax.scatter([.405],[.134],c=ORANGE,s=25,marker='s');t(.434,.134,'化合物5' if zh else 'Compound 5',7.8)
    t(.5,.074,'报告点估计；原表未提供重复数或误差。' if zh else 'Reported point estimates; replicate counts and errors were not provided.',7.2,ha='center',color=GREY)
    t(.5,.035,'所选项目化合物比较；不分离AI的增量贡献。' if zh else 'Selected project compounds; the comparison does not isolate incremental AI benefit.',7.2,ha='center',color=GREY)
    save(fig,7,lang)

if __name__ == '__main__':
    fig8('en')
