import pandas as pd
import numpy as np
from pathlib import Path


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
    for i in range(1, 6):
        # get_data(f"case{i}/support/output")
        v_support = pd.read_csv(Path(f"case{i}/LLNL_support/output/output_voltage.csv"), header=1, index_col=0)
        v_support = process_v(v_support, v_base)
        v_no_support = pd.read_csv(Path(f"case{i}/no_support/output/output_voltage.csv"), header=1, index_col=0)
        v_no_support = process_v(v_no_support, v_base)
        i_support = pd.read_csv(Path(f"case{i}/LLNL_support/output/output_current.csv"), header=1, index_col=0)
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
        inv_20 = pd.read_csv(Path(f"case{i}/LLNL_support/output/inv_20_meter.csv"), header=8)
        inv_23 = pd.read_csv(Path(f"case{i}/LLNL_support/output/inv_23_meter.csv"), header=8)
        inv_26 = pd.read_csv(Path(f"case{i}/LLNL_support/output/inv_26_meter.csv"), header=8)
        inv_29 = pd.read_csv(Path(f"case{i}/LLNL_support/output/inv_29_meter.csv"), header=8)
        inv_30 = pd.read_csv(Path(f"case{i}/LLNL_support/output/inv_30_meter.csv"), header=8)
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
    print(v_df)
    print(s_df)



    pass
