# %%
import time

import plotly.io as pio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

color_set = pio.templates['seaborn'].layout.colorway
# color = color_set[offsetgroup % len(color_set)]
q_df = pd.DataFrame({
    'Case': [1, 2, 3, 4, 5],
    'Ideal': [450, 360, 300, 250, 135],
    'D-OPF': [473, 378, 322, 275, 177],
    'ACA':   [389, 298, 237, 187, 73],
    'CA':    [374, 324, 281, 235, 132],
})
df = q_df.melt(id_vars=['Case'], value_vars=['Ideal', 'D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q')
# fig = px.bar(
#     q_df, x='Case', y='Q',
#     color='Algorithm',
#     barmode='group',
#     title='Total Q Injection (kVAr)',
#     template='seaborn',)
#
# fig.show(renderer='browser')

fig = go.Figure()
patterns = ['.', '/', '\\']
for i, algorithm in enumerate(['D-OPF', 'ACA', 'CA']):
    offsetgroup = i
    color_set = pio.templates['seaborn'].layout.colorway
    color = color_set[offsetgroup % len(color_set)]
    fig.add_trace(
        go.Bar(
            name=algorithm,
            x=df.Case,
            y=df[df['Algorithm'] == algorithm]['Q'],
            marker=go.bar.Marker(color=color, line=dict(width=4, color='black')),
            marker_pattern_shape=patterns[i],
            # offsetgroup=offsetgroup,
            # legendgroup=offsetgroup,
            showlegend=True,
            # text='a',
        ),
    )
fig.add_trace(
    go.Scatter(
        name='Ideal',
        x=df.Case,
        y=df[df['Algorithm'] == 'Ideal']['Q'],
        mode='markers',
        marker_symbol="diamond",
        marker_size=10,
        marker_color="black"
    )
)
fig.update_layout(
    font_family="Times New Roman",
    font_size=24,
    template='seaborn',
    margin=dict(l=10, r=10, t=10, b=10),
)
fig.update_xaxes(title_text='Case')
fig.update_yaxes(title_text='Substation Q Load (kVAr)')
fig.show(renderer='browser')

fig_dummy = go.Figure()
fig_dummy.write_image('dummy.pdf', format="pdf")
time.sleep(1)
fig.write_image('q_support.pdf',
                width=600,
                height=600,
                )
fig.write_image('q_support.png',
                width=600,
                height=500,
                )