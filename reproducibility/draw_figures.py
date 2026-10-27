from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
out=Path.cwd()/'figure_replay_outputs'
out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
blue='#24577C'; teal='#237B75'; orange='#C77A2B'; gray='#EDF0F2'; ink='#263238'
def save(fig,n):
    for ext in ['png','pdf','svg']: fig.savefig(out/f'Figure_{n}.{ext}',dpi=360,facecolor='white',bbox_inches='tight',pad_inches=.08)
    plt.close(fig)
def arrow(ax,a,b): ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=10,color=ink,lw=1))
def matrix(ax,x,y,arr):
    s=.048
    for i,row in enumerate(arr):
        for j,v in enumerate(row):
            ax.add_patch(Rectangle((x+j*s,y-i*s),s*.9,s*.9,facecolor=[gray,blue,teal][v],edgecolor='white',lw=.5))
            if v==2: ax.text(x+(j+.45)*s,y+(.45-i)*s,'p',ha='center',va='center',fontsize=7,color='white')
fig=plt.figure(figsize=(7.1,4.2)); ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
obs=np.array([[1,0,1,0,1],[0,1,1,1,0],[1,1,0,0,1],[0,1,0,1,1],[1,0,1,1,0],[1,1,0,1,1]])
for x,label in [(.03,'a  Masked loss'),(.53,'b  Imputation before refitting')]: ax.text(x,.94,label,fontsize=10,fontweight='bold')
ax.text(.03,.87,'ADMET-AI workflow',color=blue); ax.text(.53,.87,'MIPM workflow',color=teal)
matrix(ax,.08,.75,obs); ax.text(.08,.81,'Endpoint labels (schematic)')
arrow(ax,(.20,.44),(.20,.35)); ax.text(.20,.28,'Loss uses measured entries\nMissing entries are masked',ha='center',va='center',linespacing=1.4)
matrix(ax,.58,.75,obs); arrow(ax,(.83,.62),(.89,.62)); ax.text(.93,.62,'Initial\nmodel',ha='center',va='center')
matrix(ax,.58,.34,np.where(obs==0,2,1)); arrow(ax,(.91,.56),(.91,.24)); arrow(ax,(.89,.24),(.84,.24)); ax.text(.57,.40,'Completed labels for further fitting')
ax.plot([.49,.49],[.17,.91],color='#D9D9D9',lw=1)
for x,c,lab in [(.04,blue,'Observed'),(.31,gray,'Unmeasured'),(.60,teal,'Model-imputed (p)')]:
    ax.add_patch(Rectangle((x,.04),.025,.035,facecolor=c,edgecolor='#BBBBBB',lw=.5)); ax.text(x+.035,.055,lab,va='center')
save(fig,2)
fig=plt.figure(figsize=(7.1,4.1)); ax=fig.add_axes([.10,.22,.43,.61]); rho=np.linspace(-1,1,200)
for a,b,c,lab in [(1,1,blue,r'$\sigma_A=\sigma_B=1$'),(1,2,orange,r'$\sigma_A=1,\ \sigma_B=2$')]: ax.plot(rho,np.sqrt(a*a+b*b-2*rho*a*b),color=c,label=lab,lw=1.7)
ax.set(xlabel=r'Error correlation $\rho$',ylabel='SD of difference error (relative units)',xlim=(-1,1),ylim=(0,3.1)); ax.legend(frameon=False,fontsize=7,loc='lower left'); ax.grid(alpha=.18)
fig.text(.03,.95,'a  Correlation changes variance',fontsize=10,fontweight='bold'); fig.text(.59,.95,'b  Shared-parent measurements',fontsize=10,fontweight='bold')
fig.text(.59,.79,r'$d_1=y_{B_1}-y_A$',fontsize=12); fig.text(.59,.65,r'$d_2=y_{B_2}-y_A$',fontsize=12)
fig.text(.59,.49,r'$\mathrm{Cov}(\eta_{d_1},\eta_{d_2})=\mathrm{Var}(\eta_A)$',fontsize=10)
fig.text(.59,.31,'For independent assay errors, both\ndifferences contain the same parent error.\nShared comparisons are not independent.',linespacing=1.5)
fig.text(.5,.08,r'$\mathrm{Var}(\hat{\Delta}-\Delta)=\sigma_A^2+\sigma_B^2-2\rho\sigma_A\sigma_B$',ha='center',fontsize=12)
fig.text(.5,.015,'Illustrative error model; variance reduction does not remove bias or establish a reliable direction.',ha='center',fontsize=7)
save(fig,3)
import subprocess
import sys
subprocess.run([sys.executable, str(Path(__file__).with_name('draw_figure5.py'))], check=True)
