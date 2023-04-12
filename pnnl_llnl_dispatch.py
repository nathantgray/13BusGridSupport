# %%
import numpy as np

s_rated = np.array([
    [180000.0, 180000.0, 180000.0],  # Inverter 20
    [195000.0, 195000.0, 195000.0],  # Inverter 23
    [210000.0, 210000.0, 210000.0],  # Inverter 26
    [225000.0, 225000.0, 225000.0],  # Inverter 29
    [240000.0, 240000.0, 240000.0],  # Inverter 30
])
p_out = np.array([
    [75000, 75000, 75000],  # Inverter 20
    [75000, 75000, 75000],  # Inverter 23
    [75000, 75000, 75000],  # Inverter 26
    [75000, 75000, 75000],  # Inverter 29
    [75000, 75000, 75000],  # Inverter 30
])

q_reserve = (s_rated ** 2 - p_out ** 2) ** 0.5
q_support = [510000, 600000, 660000, 710000, 825000]
total_reserve = np.sum(q_reserve)
print(total_reserve)
pnnl_dispatch = []
pnnl_fairness = []
for i in range(len(q_support)):
    fair_fraction = q_support[i] / total_reserve
    print(fair_fraction)
    pnnl_dispatch.append(fair_fraction * q_reserve)
    pnnl_fairness.append(np.mean(np.sum(pnnl_dispatch[i]/q_reserve, axis=1)) ** 2 / np.mean(np.sum(pnnl_dispatch[i]/q_reserve, axis=1) ** 2))
# pnnl_fairness = np.mean(np.sum(fair_fractions, axis=1)) ** 2 / np.mean(np.sum(fair_fractions, axis=1) ** 2)
# %%
for i_case in range(len(q_support)):
    table_str = ""
    for i_row in range(pnnl_dispatch[i_case].shape[0]):
        for item in pnnl_dispatch[i_case][i_row, :]:
            # print(item/1e3)
            table_str = table_str + "{:0.2f}".format(item/1e3) + " & "
            # table_str = table_str + "\{{0.4f}\}".format(item)
    print(table_str)

# %%

llnl_table_strs = [
    "{29.18} & {29.18} & {29.18} & {32.09} & {32.09} & {32.09} & {34.98} & {34.98} & {34.98} & {37.83} & {37.83} & {37.83} & {40.66} & {40.66} & {40.66}",
    "{31.92} & {31.92} & {31.92} & {35.11} & {35.11} & {35.11} & {38.26} & {38.26} & {38.26} & {41.38} & {41.38} & {41.38} & {44.47} & {44.47} & {44.47}",
    "{34.36} & {34.36} & {34.36} & {37.79} & {37.79} & {37.79} & {41.19} & {41.19} & {41.19} & {44.55} & {44.55} & {44.55} & {47.87} & {47.87} & {47.87}",
    "{36.91} & {36.91} & {36.91} & {40.61} & {40.61} & {40.61} & {44.25} & {44.25} & {44.25} & {47.86} & {47.86} & {47.86} & {51.43} & {51.43} & {51.43}",
    "{42.69} & {42.69} & {42.69} & {46.97} & {46.97} & {46.97} & {51.18} & {51.18} & {51.18} & {55.35} & {55.35} & {55.35} & {59.49} & {59.49} & {59.49}",
]

llnl_dispatches = []

for i in range(5):
    table_str = llnl_table_strs[i]
    table_str = table_str.replace("{", "").replace("}", "").replace("}", "").replace(" ", "").split("&")
    a = np.zeros((5, 3))
    for j, q in enumerate(table_str):
        row = j//3
        col = j%3
        a[row, col] = float(q)*1e3
    llnl_dispatches.append(a)


llnl_dispatch_1 = 1e3*np.array([
    [29.18, 29.18, 29.18],
    [32.09, 32.09, 32.09],
    [34.98, 34.98, 34.98],
    [37.83, 37.83, 37.83],
    [40.66, 40.66, 40.66],
])

llnl_fairness = []
for i in range(len(q_support)):
    fair_fraction = q_support[i] / total_reserve
    print(fair_fraction)
    llnl_fairness.append(np.mean(np.sum(llnl_dispatches[i]/q_reserve, axis=1)) ** 2 / np.mean(np.sum(llnl_dispatches[i]/q_reserve, axis=1) ** 2))
