# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# %%
case1 = pd.DataFrame({
    'Case': [1]*5*3,
    'MG': ['MG1', 'MG1', 'MG1', 'MG2', 'MG2', 'MG2', 'MG3', 'MG3', 'MG3', 'MG4', 'MG4', 'MG4', 'MG5', 'MG5', 'MG5'],
    'phase': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
    'D-OPF': [60.28, 19.69, 58.25, 60.29, 19.69, 58.26, 60.29, 19.69, 58.26, 1.56, 1.56, 1.56, 1.56, 1.56, 1.56],
    'ACA': [28.39, 28.39, 28.39, 31.23, 31.23, 31.23, 34.03, 34.03, 34.03, 36.80, 36.80, 36.80, 39.55, 39.55, 39.55],
    'CA': [29.18, 29.18, 29.18, 32.09, 32.09, 32.09, 34.98, 34.98, 34.98, 37.83, 37.83, 37.83, 40.66, 40.66, 40.66],
})
case2 = pd.DataFrame({
    'Case': [2]*5*3,
    'MG': ['MG1', 'MG1', 'MG1', 'MG2', 'MG2', 'MG2', 'MG3', 'MG3', 'MG3', 'MG4', 'MG4', 'MG4', 'MG5', 'MG5', 'MG5'],
    'phase': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
    'D-OPF': [62.25, 28.64, 60.48, 62.25, 28.64, 60.48, 62.25, 28.64, 60.48, 12.70, 6.61, 12.46, 12.70, 6.61, 12.46],
    'ACA': [33.40, 33.40, 33.40, 36.74, 36.74, 36.74, 40.04, 40.04, 40.04, 43.30, 43.30, 43.30, 46.53, 46.53, 46.53],
    'CA': [31.92, 31.92, 31.92, 35.11, 35.11, 35.11, 38.26, 38.26, 38.26, 41.38, 41.38, 41.38, 44.47, 44.47, 44.47],
})
case3 = pd.DataFrame({
    'Case': [3] * 5 * 3,
    'MG': ['MG1', 'MG1', 'MG1', 'MG2', 'MG2', 'MG2', 'MG3', 'MG3', 'MG3', 'MG4', 'MG4', 'MG4', 'MG5', 'MG5', 'MG5'],
    'phase': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
    'D-OPF': [65.24, 33.02, 63.51, 65.25, 33.02, 63.51, 65.25, 33.02, 63.51, 17.04, 10.42, 16.77, 17.04, 10.42, 16.77],
    'ACA': [36.74, 36.74, 36.74, 40.41, 40.41, 40.41, 44.04, 44.04, 44.04, 47.63, 47.63, 47.63, 51.18, 51.18, 51.18],
    'CA': [34.36, 34.36, 34.36, 37.79, 37.79, 37.79, 41.19, 41.19, 41.19, 44.55, 44.55, 44.55, 47.87, 47.87, 47.87],
})
case4 = pd.DataFrame({
    'Case': [4]*5*3,
    'MG': ['MG1', 'MG1', 'MG1', 'MG2', 'MG2', 'MG2', 'MG3', 'MG3', 'MG3', 'MG4', 'MG4', 'MG4', 'MG5', 'MG5', 'MG5'],
    'phase': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
    'D-OPF': [69.90, 37.51, 68.14, 69.91, 37.51, 68.14, 69.91, 37.51, 68.14, 17.65, 11.78, 17.39, 17.65, 11.78, 17.39],
    'ACA': [39.52, 39.52, 39.52, 43.47, 43.47, 43.47, 47.37, 47.37, 47.37, 51.23, 51.23, 51.23, 55.06, 55.06, 55.06],
    'CA': [36.91, 36.91, 36.91, 40.61, 40.61, 40.61, 44.25, 44.25, 44.25, 47.86, 47.86, 47.86, 51.43, 51.43, 51.43],
})
case5 = pd.DataFrame({
    'Case': [5]*5*3,
    'MG': ['MG1', 'MG1', 'MG1', 'MG2', 'MG2', 'MG2', 'MG3', 'MG3', 'MG3', 'MG4', 'MG4', 'MG4', 'MG5', 'MG5', 'MG5'],
    'phase': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
    'D-OPF': [79.67, 47.42, 77.88, 79.68, 47.42, 77.89, 79.68, 47.42, 77.89, 18.95, 14.28, 18.71, 18.95, 14.28, 18.71],
    'ACA': [45.92, 45.92, 45.92, 50.52, 50.52, 50.52, 55.05, 55.05, 55.05, 59.53, 59.53, 59.53, 63.98, 63.98, 63.98],
    'CA': [42.69, 42.69, 42.69, 46.97, 46.97, 46.97, 51.18, 51.18, 51.18, 55.35, 55.35, 55.35, 59.49, 59.49, 59.49],
})
df = pd.concat([case1, case2, case3, case4, case5])
# %%
df = pd.melt(df, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
case1_melt = pd.melt(case1, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
case2_melt = pd.melt(case2, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
case3_melt = pd.melt(case3, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
case4_melt = pd.melt(case4, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
case5_melt = pd.melt(case5, id_vars=['Case', 'MG', 'phase'], value_vars=['D-OPF', 'ACA', 'CA'], var_name='Algorithm', value_name='Q Injection (kvar)')
# %%
# for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
fig = px.bar(
    df, x='MG', y='Q Injection (kvar)', color='Algorithm', barmode='group',
    # pattern_shape='phase', pattern_shape_sequence=['.', 'x', '+'],
    facet_col='Case',
    # facet_row='phase',
    template='seaborn'
)
fig.show()
fig.update_layout(
    font_family="Times New Roman",
    font_size=24,
)
fig.write_image('dispatch.png',
                width=1600,
                height=700,
                )
