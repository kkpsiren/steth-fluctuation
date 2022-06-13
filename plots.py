import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator
import seaborn as sns
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
import scipy.stats as stats
import pandas as pd


def plot_pair(data, col = 'uniswap'):
    g = sns.jointplot(x='stETH-ETH', y=col, data=data.rename({"MEAN_PRICE":'stETH-ETH'},axis=1),
                      kind="reg", truncate=False,
                      color="m", height=8,ratio=5)

    g_data = data[["MEAN_PRICE",col]].dropna()
    r, p = stats.spearmanr(g_data['MEAN_PRICE'].values, g_data[col].values)
    # if you choose to write your own legend, then you should adjust the properties then
    phantom, = g.ax_joint.plot([], [], linestyle="", alpha=0)
    # here graph is not a ax but a joint grid, so we access the axis through ax_joint method

    g.ax_joint.legend([phantom],[col+' r={:f}, p={:f}'.format(r,p)]);

    return g.fig

def pyplot(cors):
    cors['r'] = cors['r'].astype('float')
    fig,ax =plt.subplots(figsize=(6,12))
    cors.sort_values('r',ascending=False).plot.barh(x='name', y='r',ax=ax)
    return fig

def clustermap_dates(data,names):
    data = data[names+['MEAN_PRICE']].rename({"MEAN_PRICE":'stETH-ETH'},axis=1)
    data1 = data.fillna(data.mean())

    dist = pdist(data1.values, metric='correlation')
    Z = hierarchy.linkage(dist, 'single')

    g = sns.clustermap(data1.T.corr(),#xticklabels=True,yticklabels=True,
        row_linkage=Z,
        col_linkage=Z,)
    den = hierarchy.dendrogram(g.dendrogram_col.linkage, labels=data.index,
                            color_threshold=0.10, distance_sort=True, ax=g.ax_col_dendrogram)
    g.ax_col_dendrogram.axis('on')
    # sns.despine(ax=g.ax_col_dendrogram, left=False, right=True, top=True, bottom=True)
    g.ax_col_dendrogram.yaxis.set_major_locator(MaxNLocator())
    g.ax_col_dendrogram.yaxis.set_major_formatter(ScalarFormatter())
    g.ax_col_dendrogram.grid(axis='y', ls='--', color='grey')
    # g.ax_col_dendrogram.yaxis.tick_right()
    groups = pd.Series(den['leaves_color_list'], index= [data.index[i] for i in den['leaves']])
    return g.fig, groups


def clustermap_groups(data,names):
    data = data[names+['MEAN_PRICE']].rename({"MEAN_PRICE":'stETH-ETH'},axis=1)
    data1 = data.fillna(data.mean())
    dist = pdist(data1.T.values, metric='cosine')
    Z = hierarchy.linkage(dist, 'single')
    
    g = sns.clustermap(data1.corr(),#xticklabels=True,yticklabels=True,
        row_linkage=Z,
        col_linkage=Z,)
    den = hierarchy.dendrogram(g.dendrogram_col.linkage, labels=data1.T.index,
                            color_threshold=0.10, distance_sort=True, ax=g.ax_col_dendrogram)
    g.ax_col_dendrogram.axis('on')
    # sns.despine(ax=g.ax_col_dendrogram, left=False, right=True, top=True, bottom=True)
    g.ax_col_dendrogram.yaxis.set_major_locator(MaxNLocator())
    g.ax_col_dendrogram.yaxis.set_major_formatter(ScalarFormatter())
    g.ax_col_dendrogram.grid(axis='y', ls='--', color='grey')
    # g.ax_col_dendrogram.yaxis.tick_right()
    
    groups = pd.Series(den['leaves_color_list'], index= [data1.T.index[i] for i in den['leaves']])
    return g.fig, groups

def plot_scatter(df,x,y, c=None,text=None):
    mapper = {'stETH':'#bf230f','WETH':'#19848c'}
    fig = make_subplots(rows=1, cols=1)
    string_x = f'<br><b>{x}</b>: '
    string_y = f'<br><b>{y}</b>: '
    if c is not None:
        for option_a in df[c].unique():
            fig.add_trace(
                go.Scatter(x=df[df[c]==option_a][x].tolist(), 
                            y=df[df[c]==option_a][y].tolist(),
                            hovertemplate =
                                string_x + '%{x}<br>'+
                                string_y + '%{y:.3f}<br>',
                                name=option_a,
                                mode='markers',
                                #'%{text}',
                            #text = [f'<br><b>Number of Sales</b>: {i}' for i in a['count'].tolist()],
                            
                            showlegend = True),
                    row=1, col=1
                )
        fig.update_layout(hovermode="x")
        
    else:
        fig.add_trace(
            go.Scatter(x=df[x].tolist(), 
                        y=df[y].tolist(),
                        hovertemplate =
                            string_x + '%{x}<br>'+
                            string_y + '%{y:.3f}<br>',
                            mode='markers',
                            #'%{text}',
                        #text = [f'<br><b>Number of Sales</b>: {i}' for i in a['count'].tolist()],
                        showlegend = False),
                row=1, col=1
            ) 
    fig.update_layout(height=300, width=600, title_text=text)
    return fig