import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis import network as net
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from st_aggrid import AgGrid
from pathlib import Path
import os

# Say, "the default sans-serif font is COMIC SANS"
matplotlib.rcParams['font.sans-serif'] = "DIN Alternate"
# Then, "ALWAYS use sans-serif fonts"
matplotlib.rcParams['font.family'] = "sans-serif"

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def load_factors():
    sheet_id = '1MQt451tCvDwlXjZBV0xO8kGUPDFFmGaZTXQYSJhUM4E'
    sheet_name = 'Factors'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_factors=pd.read_csv(url)
    df_factors = df_factors.loc[:, ~df_factors.columns.str.contains('^Unnamed')]
    with st.expander('Factors Table'):
        st.markdown('### Factors Table')
        AgGrid(df_factors)
    
def plot_factors():
    G=nx.empty_graph()
    
    sheet_id = '1MQt451tCvDwlXjZBV0xO8kGUPDFFmGaZTXQYSJhUM4E'
    sheet_name = 'Factors'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_factors=pd.read_csv(url)
    df_factors = df_factors.loc[:, ~df_factors.columns.str.contains('^Unnamed')]

    for index, row in df_factors.iterrows():
        size=15
        if row['short_name']=='FOCAL_FACTOR': size=40
        group = str(row.loc["node_group"])
        if group == '1':
            color = 'lightblue'
        elif group == '2':
            color = 'lemonchiffon'
        elif group == '3':
            color = 'salmon'
        elif group == '4':
            color = 'lightgreen'
        elif group == '5':
            color = 'orchid'
        else:
            color= ''
        G.add_node(row['node_id'], label=row['long_name'], group=row['node_group'], size=size, color=color)
        
    nt = net.Network(width='1000px', height='1000px', directed=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics'])
    nt.show("G_factors.html")
    HtmlFile = open('G_factors.html','r',encoding='utf-8')
    with st.expander('Factors Plot'):
        st.markdown('### General and Focal Factors')
        components.html(HtmlFile.read(),height=1000)
        
def load_relationships():
    sheet_id = '1MQt451tCvDwlXjZBV0xO8kGUPDFFmGaZTXQYSJhUM4E'
    sheet_name = 'Relationships'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_relationships=pd.read_csv(url)
    df_relationships = df_relationships.loc[:, ~df_relationships.columns.str.contains('^Unnamed')]
    with st.expander('Relationships Table'):
        st.markdown('### Relationships Table')
        AgGrid(df_relationships)

def plot_relationships():
    G=nx.empty_graph(create_using=nx.DiGraph())

    sheet_id = '1MQt451tCvDwlXjZBV0xO8kGUPDFFmGaZTXQYSJhUM4E'
    sheet_name = 'Factors'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_factors=pd.read_csv(url)
    df_factors = df_factors.loc[:, ~df_factors.columns.str.contains('^Unnamed')]
    
    sheet_id = '1MQt451tCvDwlXjZBV0xO8kGUPDFFmGaZTXQYSJhUM4E'
    sheet_name = 'Relationships'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df_relationships=pd.read_csv(url)
    df_relationships = df_relationships.loc[:, ~df_relationships.columns.str.contains('^Unnamed')]

    for index, row in df_factors.iterrows():
        size=15
        if row['short_name']=='FOCAL_FACTOR': size=40
        group = str(row.loc["node_group"])
        if group == '1':
            color = 'lightblue'
        elif group == '2':
            color = 'lemonchiffon'
        elif group == '3':
            color = 'salmon'
        elif group == '4':
            color = 'lightgreen'
        elif group == '5':
            color = 'orchid'
        else:
            color= ''
        G.add_node(row['node_id'], label=row['long_name'], group=row['node_group'], size=size, color=color)

    show_weights = False

    for index, row in df_relationships.iterrows():

        edge_from = row['From_id']
        edge_to = row['To_id']

        if show_weights==True:
            if row['Strength']=='weak': value=1
            if row['Strength']=='medium': value=2
            if row['Strength']=='strong': value=3
            G.add_edge(edge_from, edge_to, value=value)

        G.add_edge(edge_from, edge_to)

    nt = net.Network(width='1000px', height='1000px', directed=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics'])
    nt.inherit_edge_colors(False)
#     nt.set_options("""
#     var options = {
#   "physics": {
#     "forceAtlas2Based": {
#       "springLength": 100
#     },
#     "minVelocity": 0.75,
#     "solver": "forceAtlas2Based"
#   }
# }
    
    
#     """)
    nt.show("G_factors_and_relationships.html")
    HtmlFile = open('G_factors_and_relationships.html','r',encoding='utf-8')
    with st.expander('Relationships Plot'):
        st.markdown('### Conceptual Model / Systems Map')
        components.html(HtmlFile.read(),height=1000)
    return G

        
def load_centrality(G):
    df_nodes = pd.DataFrame.from_dict(dict(G.nodes(data=True)), orient='index')
    node_colors = df_nodes.color.to_list()
    df_nodes.drop(['size', 'color'], axis=1, inplace=True)
    
    in_degree_centrality_df = pd.DataFrame(nx.in_degree_centrality(G).items(), columns=["node", "in_degree_centrality"])
    in_degree_centrality_df.index += 1
    
    out_degree_centrality_df = pd.DataFrame(nx.out_degree_centrality(G).items(), columns=["node", "out_degree_centrality"])
    out_degree_centrality_df.index += 1
    
    closeness_centrality_df = pd.DataFrame(nx.closeness_centrality(G).items(), columns=["node", "closeness_centrality"])
    closeness_centrality_df.index += 1
    
    betweenness_centrality_df = pd.DataFrame(nx.betweenness_centrality(G).items(), columns=["node", "betweenness_centrality"])
    betweenness_centrality_df.index += 1
    
    pagerank_centrality_df = pd.DataFrame(nx.pagerank(G).items(), columns=["node", "pagerank_centrality"])
    pagerank_centrality_df.index += 1
    
    hub_scores, auth_scores = nx.hits(G)
    hub_centrality_df = pd.DataFrame(hub_scores.items(), columns=["node", "hub_centrality"])
    auth_centrality_df = pd.DataFrame(auth_scores.items(), columns=["node", "auth_centrality"])
    hub_centrality_df.index += 1
    auth_centrality_df.index += 1
    
    centrality_summary_df = in_degree_centrality_df\
    .merge(out_degree_centrality_df, on="node")\
    .merge(pagerank_centrality_df, on="node")\
    .merge(closeness_centrality_df, on="node")\
    .merge(betweenness_centrality_df, on="node")\
    .merge(hub_centrality_df, on="node")\
    .merge(auth_centrality_df, on="node")

    centrality_summary_df.index += 1
    centrality_summary_df = df_nodes.join(centrality_summary_df).drop(['node'], axis=1)

    centrality_ranks = centrality_summary_df.rank(ascending=False, numeric_only=True, method="dense").astype(int)
    
    # compute the average ranking using the above ranks
    average_ranks = pd.DataFrame(round(centrality_ranks.mean(axis=1)).astype(int), columns=["average_rank"])
    average_ranks.insert(loc=0, column='node', value=centrality_summary_df["label"])
    
    centrality_summary_df_styled = centrality_summary_df.style.background_gradient(subset=list(centrality_ranks.columns[1:]), cmap='PuBu_r').set_precision(2)
    centrality_summary_df_styled.to_html('centrality_summary_df_styled.html')
    HtmlFile_centrality_summary_df_styled = open('centrality_summary_df_styled.html','r',encoding='utf-8')
    
    centrality_ranks_df_styled = df_nodes.join(centrality_ranks.drop(['group'], axis=1), how='left').style.background_gradient(subset=list(centrality_ranks.columns[1:]),cmap='PuBu')
    centrality_ranks_df_styled.to_html('centrality_ranks_df_styled.html')
    HtmlFile_centrality_ranks_df_styled = open('centrality_ranks_df_styled.html','r',encoding='utf-8')
    
    average_ranks_df_styled = average_ranks.sort_values("average_rank").style.background_gradient(subset=["average_rank"], cmap='PuBu')
    average_ranks_df_styled.to_html('average_ranks_df_styled.html')
    HtmlFile_average_ranks_df_styled = open('average_ranks_df_styled.html','r',encoding='utf-8')

    
    with st.expander('Centrality Tables'):
        
        st.markdown('## Node Importance: Centrality')
        centrality_md = read_markdown_file("centrality_explained.md")
        st.markdown(centrality_md, unsafe_allow_html=True)
        
        st.markdown('### Centrality — Summary')
        #st.dataframe(centrality_summary_df.style.background_gradient(subset=list(centrality_ranks.columns[1:]), cmap='PuBu_r').set_precision(2))
        AgGrid(centrality_summary_df.round(2))
        st.markdown('*white = more important | dark blue = less important*')
        components.html(HtmlFile_centrality_summary_df_styled.read(),height=400)
        
        st.markdown('### Centrality — All Rankings')
        st.markdown('*white = more important | dark blue = less important*')
        #st.dataframe(centrality_ranks.style.background_gradient(cmap='PuBu'))
        components.html(HtmlFile_centrality_ranks_df_styled.read(),height=400)
        
        st.markdown('### Centrality — Average Ranking')
        st.markdown('*white = more important | dark blue = less important*')
        #st.dataframe(average_ranks.sort_values("average_rank").style.background_gradient(subset=["average_rank"], cmap='PuBu'))
        components.html(HtmlFile_average_ranks_df_styled.read(),height=400)

    return node_colors
        
def draw(G, pos, measures, measure_name, ax):
    
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=250, cmap=plt.cm.plasma, 
                                   node_color=list(measures.values()),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=ax)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()
    
    
def draw_centralities(G,node_colors):
    
    pos = nx.kamada_kawai_layout(G)
    
    f = plt.figure(constrained_layout=True, figsize=(25,20))
    gs = f.add_gridspec(4, 4)

    f_ax2 = f.add_subplot(gs[0:2,1:3])
    #f_ax2.set_title('table of factors')
    f_ax2.set_aspect('equal')

    f_ax3 = f.add_subplot(gs[2, 0])
    f_ax3.set_title('in-degree centrality')
    f_ax3.set_aspect('equal')

    f_ax4 = f.add_subplot(gs[2, 1])
    f_ax4.set_title('out-degree centrality')
    f_ax4.set_aspect('equal')

    f_ax5 = f.add_subplot(gs[2, 2])
    f_ax5.set_title('degree centrality')
    f_ax5.set_aspect('equal')

    f_ax6 = f.add_subplot(gs[2, 3])
    f_ax6.set_title('betweenness centrality')
    f_ax6.set_aspect('equal')

    f_ax7 = f.add_subplot(gs[3, 0])
    f_ax7.set_title('in-degree centrality')
    f_ax7.set_aspect('equal')

    f_ax8 = f.add_subplot(gs[3, 1])
    f_ax8.set_title('out-degree centrality')
    f_ax8.set_aspect('equal')

    f_ax9 = f.add_subplot(gs[3, 2])
    f_ax9.set_title('degree centrality')
    f_ax9.set_aspect('equal')

    f_ax10 = f.add_subplot(gs[3, 3])
    f_ax10.set_title('betweenness centrality')
    f_ax10.set_aspect('equal')
    
    nx.draw(G, pos, ax=f_ax2, with_labels=True, font_size=20, width=1, node_size=1000, node_color=node_colors)

    # in-degree centrality
    measure_name = 'In-Degree Centrality'
    measures = nx.in_degree_centrality(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax3, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax3)
    f_ax3.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax3,location='right')

    # out-degree centrality
    measure_name = 'Out-Degree Centrality'
    measures = nx.out_degree_centrality(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax4, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax4)
    f_ax4.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax4,location='right')

    # degree centrality
    measure_name = 'Degree Centrality'
    measures = nx.degree_centrality(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax5, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax5)
    f_ax5.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax5,location='right')

    # betweenness centrality
    measure_name = 'Betweenness Centrality'
    measures = nx.betweenness_centrality(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax6, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax6)
    f_ax6.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax6,location='right')

    # closeness centrality
    measure_name = 'Closeness Centrality'
    measures = nx.closeness_centrality(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax7, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax7)
    f_ax7.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax7,location='right')

    # pagerank centrality
    measure_name = 'Pagerank Centrality'
    measures = nx.pagerank(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax8, node_size=250, cmap=plt.cm.plasma, node_color=list(measures.values()), nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax8)
    f_ax8.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax8,location='right')

    # hub centrality
    measure_name = 'Hub Centrality'
    h,a = nx.hits(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax9, node_size=250, cmap=plt.cm.plasma, node_color=list(h.values()), nodelist=h.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax9)
    f_ax9.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax9,location='right')

    # authority centrality
    measure_name = 'Authority Centrality'
    h,a = nx.hits(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=f_ax10, node_size=250, cmap=plt.cm.plasma, node_color=list(a.values()), nodelist=a.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    #labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos, ax=f_ax10)
    f_ax10.set_title(measure_name, size=16, weight='bold')
    plt.colorbar(nodes,ax=f_ax10,location='right')
    
    with st.expander('Centrality Plots'):
        st.pyplot(f)