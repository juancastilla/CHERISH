from utilities import *
import os

### CONFIGURATION ###

stdir = os.getcwd()   # App dir

apptitle = 'ITLAs Computational Social Science Model of Child Wellbeing and Social Assistance Pathways (CHERISH)'

st.set_page_config(page_title=apptitle, layout="wide", page_icon=":eyeglasses:")

st.sidebar.image(os.path.join(stdir, 'CHERISH.png'))

st.sidebar.markdown('# ITLAs Computational Social Science Model of Child Wellbeing and Social Assistance Pathways (CHERISH)')

st.sidebar.subheader('PSM Explorer')
    
option_1 = st.sidebar.selectbox('What PSM do you want to explore?',('Example', 'Breakout 1', 'Breakout 2', 'Breakout 3', 'Consolidated'), key=1)

if st.sidebar.button('load data'):

    load_factors()
    plot_factors()
    load_relationships()
    G = plot_relationships()
    node_colors = load_centrality(G)
    draw_centralities(G,node_colors)
    
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')
st.sidebar.markdown('#')

st.sidebar.image(os.path.join(stdir, 'collaboration_logos.png'))

