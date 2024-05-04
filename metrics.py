import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import time

dopf_voltages = {
    'Case 1': [1.0076659201024456, 0.9952088070951687, 0.9884654611509147, 0.9898275854600317, 0.993992223351458, 0.9890483017991063],
    'Case 2': [1.009153813783544, 0.998018601258673, 0.9920645500347114, 0.9934837362580538, 0.9970164398534944, 0.9926198903515355],
    'Case 3': [1.0089040757895194, 0.9985548056061544, 0.9930670234310931, 0.9945330691232308, 0.9976613562033695, 0.9936003933495965],
    'Case 4': [1.0077478856596884, 0.9980625946552547, 0.9929571740764264, 0.994486524282575, 0.997220544554115, 0.9934611650546092],
    'Case 5': [1.004163178904184, 0.9958808981841684, 0.9915832326841314, 0.9932538556436364, 0.9951461430791126, 0.992027340781365],
}
dopf_voltages_df = pd.DataFrame(dopf_voltages)
dopf_voltages_df['Algorithm'] = ['D-OPF']*6
dopf_voltages_df['area'] = ['Substation', 'MG1', 'MG2', 'MG3', 'MG4', 'MG5']
dopf_voltages_df = pd.melt(dopf_voltages_df, id_vars=['Algorithm', 'area'], value_vars=['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5'], var_name='Case', value_name='Positive Sequence Voltage (pu)')
voltages = pd.concat([dopf_voltages_df])
print(voltages)
def parse_phasors(str_values: np.ndarray):
    values = str_values.flatten()
    n = values.shape[0]
    for i in range(n):
        values[i] = parse_phasor(values[i])
    return values


def parse_phasor(str_value: str):
    if str_value[-1] != 'd':
        raise ValueError("Value is not a phasor with angle in degrees.")
    last_minus = str_value.rfind('-')
    last_plus = str_value.rfind('+')
    start_angle = max(last_plus, last_minus)
    magnitude = float(str_value[:start_angle])
    angle = float(str_value[start_angle:-1])
    complex_value = magnitude*np.exp(np.radians(angle)*1j)
    return complex_value


def symmetrical_components(v_3ph):
    v_3ph_ = np.array([np.array(v_3ph).flatten()]).T
    a = np.exp(120*np.pi/180*1j)
    c = 1/3*np.array(
        [
            [1, 1, 1],
            [1, a, a**2],
            [1, a**2, a],
        ]
    )
    v_seq = c @ v_3ph_
    return v_seq.flatten()

def symmetrical_components_list(v_3ph_array):
    a = np.exp(120*np.pi/180*1j)
    c = 1/3*np.array(
        [
            [1, 1, 1],
            [1, a, a**2],
            [1, a**2, a],
        ]
    )
    seq = c @ v_3ph_array
    return seq.T

def process_v(volt_dump, v_ln_base):
    if 'voltA_mag' in volt_dump.keys():  # polar format
        volt_dump.loc[:, ['voltA_mag', 'voltB_mag', 'voltC_mag']] /= v_ln_base
        volt_dump.loc[:, ['a', 'b', 'c']] = np.multiply(
            volt_dump.loc[:, ['voltA_mag', 'voltB_mag', 'voltC_mag']].values,
            np.exp(volt_dump.loc[:, ['voltA_angle', 'voltB_angle', 'voltC_angle']].values*1j))
    if 'voltA_real' in volt_dump.keys():  # rectangular format
        volt_dump.loc[:, ['voltA_real', 'voltB_real', 'voltC_real']] /= v_ln_base
        volt_dump.loc[:, ['voltA_imag', 'voltB_imag', 'voltC_imag']] /= v_ln_base
        volt_dump.loc[:, ['a', 'b', 'c']] = \
            (volt_dump.loc[:, ['voltA_real', 'voltB_real', 'voltC_real']].values +
             volt_dump.loc[:, ['voltA_imag', 'voltB_imag', 'voltC_imag']].values*1j)
        volt_dump.loc[:, ['voltA_mag', 'voltB_mag', 'voltC_mag']] = np.abs(volt_dump.loc[:, ['a', 'b', 'c']].values)
    return volt_dump


def process_i(curr_dump, i_base):
    if 'currA_mag' in curr_dump.keys():  # polar format
        curr_dump.loc[:, ['currA_mag', 'currB_mag', 'currC_mag']] /= i_base
        curr_dump.loc[:, ['a', 'b', 'c']] = np.multiply(
            curr_dump.loc[:, ['currA_mag', 'currB_mag', 'currC_mag']].values,
            np.exp(curr_dump.loc[:, ['currA_angle', 'currB_angle', 'curr_angle']].values*1j))
    if 'currA_real' in curr_dump.keys():  # rectangular format
        curr_dump.loc[:, ['currA_real', 'currB_real', 'currC_real']] /= i_base
        curr_dump.loc[:, ['currA_imag', 'currB_imag', 'currC_imag']] /= i_base
        curr_dump.loc[:, ['a', 'b', 'c']] = \
            curr_dump.loc[:, ['currA_real', 'currB_real', 'currC_real']].values + \
            curr_dump.loc[:, ['currA_imag', 'currB_imag', 'currC_imag']].values*1j
        curr_dump.loc[:, ['voltA_mag', 'voltB_mag', 'voltC_mag']] = np.abs(curr_dump.loc[:, ['a', 'b', 'c']].values)
    return curr_dump


if __name__ == '__main__':
    s_base = 1e6
    v_base = 2401.7771198288433
    i_base = s_base / v_base
    v_df = pd.DataFrame()
    s_df = pd.DataFrame()
    lab_alg = {
        "PNNL": 'ACA',
        "LLNL": 'CA'
    }
    for lab in ['PNNL', 'LLNL']:
        voltage_cases = {}
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '+lab+' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for i in range(1, 6):
            # get_data(f"case{i}/support/output")
            v_support = pd.read_csv(Path(f"case{i}/{lab}_support/output/output_voltage.csv"), header=1, index_col=0)
            v_support = process_v(v_support, v_base)
            v_no_support = pd.read_csv(Path(f"case{i}/no_support/output/output_voltage.csv"), header=1, index_col=0)
            v_no_support = process_v(v_no_support, v_base)
            i_support = pd.read_csv(Path(f"case{i}/{lab}_support/output/output_current.csv"), header=1, index_col=0)
            i_support = process_i(i_support, i_base)
            i_no_support = pd.read_csv(Path(f"case{i}/no_support/output/output_current.csv"), header=1, index_col=0)
            i_no_support = process_i(i_no_support, i_base)
            v_sym = symmetrical_components(v_no_support.loc['node_1', ['a', 'b', 'c']].values)[1]
            v_df.loc[f'case{i}_no_support', ['a', 'b', 'c']] = \
                v_no_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real
            v_df.loc[f'case{i}_no_support', ['0', '1', '2']] = \
                np.abs(symmetrical_components(v_no_support.loc['node_1', ['a', 'b', 'c']].values))
            v_df.loc[f'case{i}', ['a', 'b', 'c']] = v_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real
            v_df.loc[f'case{i}', ['0', '1', '2']] = \
                np.abs(symmetrical_components(v_support.loc['node_1', ['a', 'b', 'c']].values))
            v_df.loc[f'case{i}_increase', ['a', 'b', 'c']] = \
                v_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real - \
                v_no_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real
            v_df.loc[f'case{i}_increase', ['0', '1', '2']] = \
                np.abs(symmetrical_components(v_support.loc['node_1', ['a', 'b', 'c']].values)) - \
                np.abs(symmetrical_components(v_no_support.loc['node_1', ['a', 'b', 'c']].values))

            load = v_support.loc['node_1', ['a', 'b', 'c']] * np.conj(i_support.loc['oh_line_1_2', ['a', 'b', 'c']])
            load_no_support = \
                v_no_support.loc['node_1', ['a', 'b', 'c']] * np.conj(i_no_support.loc['oh_line_1_2', ['a', 'b', 'c']])
            q = load.values.imag
            p = load.values.real
            q_no_support = load_no_support.values.imag
            p_no_support = load_no_support.values.real
            print(q_no_support.sum())
            s_df.loc[f'case{i}_no_support', 'p'] = p_no_support.sum()
            s_df.loc[f'case{i}', 'p'] = p.sum()
            s_df.loc[f'case{i}_delta', 'p'] = p.sum() - p_no_support.sum()
            s_df.loc[f'case{i}_no_support', 'q'] = q_no_support.sum()
            s_df.loc[f'case{i}', 'q'] = q.sum()
            s_df.loc[f'case{i}_delta', 'q'] = q.sum() - q_no_support.sum()

            # Fairness
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
            inv_df = pd.DataFrame()
            inv_20 = pd.read_csv(Path(f"case{i}/{lab}_support/output/inv_20_meter.csv"), header=8)
            inv_23 = pd.read_csv(Path(f"case{i}/{lab}_support/output/inv_23_meter.csv"), header=8)
            inv_26 = pd.read_csv(Path(f"case{i}/{lab}_support/output/inv_26_meter.csv"), header=8)
            inv_29 = pd.read_csv(Path(f"case{i}/{lab}_support/output/inv_29_meter.csv"), header=8)
            inv_30 = pd.read_csv(Path(f"case{i}/{lab}_support/output/inv_30_meter.csv"), header=8)
            inv_df.loc['inv20', ['a', 'b', 'c']] = parse_phasors(inv_20.iloc[0, 1:].values)
            inv_df.loc['inv23', ['a', 'b', 'c']] = parse_phasors(inv_23.iloc[0, 1:].values)
            inv_df.loc['inv26', ['a', 'b', 'c']] = parse_phasors(inv_26.iloc[0, 1:].values)
            inv_df.loc['inv29', ['a', 'b', 'c']] = parse_phasors(inv_29.iloc[0, 1:].values)
            inv_df.loc['inv30', ['a', 'b', 'c']] = parse_phasors(inv_30.iloc[0, 1:].values)
            loading = np.abs(inv_df.values.imag)/q_reserve
            fairness = np.mean(np.sum(loading, axis=1))**2/np.mean(np.sum(loading, axis=1)**2)
            # see origianl source https://www.cse.wustl.edu/~jain/papers/ftp/fairness.pdf
            # see wikipedia source https://en.wikipedia.org/wiki/Fairness_measure
            print(f"Case {i} Fairness={fairness}")
            voltage_cases[f'Case {i}'] = np.abs(symmetrical_components_list(v_support.loc[['node_1', 'node_15', 'node_16', 'node_17', 'node_27', 'node_28'], ['a', 'b', 'c']].values.T)[:, 1])
        voltage_cases_df = pd.DataFrame(voltage_cases)
        voltage_cases_df['Algorithm'] = [lab_alg[lab]]*6
        voltage_cases_df['area'] = ['Substation', 'MG1', 'MG2', 'MG3', 'MG4', 'MG5']
        voltage_cases_df = pd.melt(voltage_cases_df, id_vars=['Algorithm', 'area'], value_vars=['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5'], var_name='Case', value_name='Positive Sequence Voltage (pu)')
        voltages = pd.concat([voltages, voltage_cases_df])
        print(voltage_cases_df)
        print(v_df)
        print(s_df)

    print(voltages)

no_support_voltages = {
    'Case 1': [0.9791760667205147, 0.9597782475187674, 0.9490172236141672, 0.9498354614863559, 0.9581038975967313, 0.949988230171803],
    'Case 2': [0.9693399607228788, 0.9497100338058078, 0.9388164123907903, 0.939647849794722, 0.948014929945814, 0.9398029115044835],
    'Case 3': [0.9585939069833714, 0.93870251117528, 0.9276592358517602, 0.9285056582709, 0.9369839367777686, 0.9286633373481439],
    'Case 4': [0.9447537704199495, 0.924512611238841, 0.9132686804662007, 0.9141353456740094, 0.9227624921435689, 0.9142965853092236],
    'Case 5': [0.8979771781739521, 0.8764265526367158, 0.8644267783465072, 0.8653712820286368, 0.8745568447318511, 0.8655465189382259],
}
no_support_voltages_df = pd.DataFrame(no_support_voltages)
no_support_voltages_df['Algorithm'] = ['No Support']*6
no_support_voltages_df['area'] = ['Substation', 'MG1', 'MG2', 'MG3', 'MG4', 'MG5']
no_support_voltages_df = pd.melt(no_support_voltages_df, id_vars=['Algorithm', 'area'], value_vars=['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5'], var_name='Case', value_name='Positive Sequence Voltage (pu)')

voltages = pd.concat([voltages, no_support_voltages_df])
fig = px.scatter(voltages, x='area', y='Positive Sequence Voltage (pu)',
                    color='Algorithm',
                    symbol='Algorithm',
                    facet_col='Case',
                    # barmode='group',
                    template='seaborn',
                    labels=dict(area=''),
                    symbol_sequence=['circle', 'circle', 'circle', 'x'],
             )
fig.update_layout(
    font_family="Times New Roman",
    font_size=24,
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_traces(marker={'size': 15})
fig_dummy = px.scatter(x=[0], y=[0])
fig_dummy.write_image('dummy.pdf', format="pdf")
time.sleep(1)
fig.write_image('voltage.pdf',
                width=1600,
                height=500,
                )
fig.show()

fig = px.scatter(
    voltages[voltages["area"]=="Substation"],
    x=voltages[voltages["area"]=="Substation"]['Case'].str.strip("Case "),
    y='Positive Sequence Voltage (pu)',
    color='Algorithm',
    symbol='Algorithm',
    template='seaborn',
    symbol_sequence=['circle', 'circle', 'circle', 'x'],
)
fig.add_hline(y=1.01, line_width=2, line_color="black")
fig.update_layout(
    font_family="Times New Roman",
    font_size=24,
    template='seaborn',
    margin=dict(l=10, r=10, t=10, b=10),
    legend_title=None,
)

fig.update_traces(marker=dict(size=16),
                  selector=dict(mode='markers'))
fig.update_xaxes(title_text='Case')
fig.show()

fig.write_image('v_sub.pdf',
                width=500,
                height=500,
                )

fig.write_image('v_sub.png',
                width=600,
                height=500,
                )