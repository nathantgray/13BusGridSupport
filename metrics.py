import pandas as pd
import numpy as np
from pathlib import Path


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
        v_support = pd.read_csv(Path(f"case{i}/support/output/output_voltage.csv"), header=1, index_col=0)
        v_support = process_v(v_support, v_base)
        v_no_support = pd.read_csv(Path(f"case{i}/no_support/output/output_voltage.csv"), header=1, index_col=0)
        v_no_support = process_v(v_no_support, v_base)
        i_support = pd.read_csv(Path(f"case{i}/support/output/output_current.csv"), header=1, index_col=0)
        i_support = process_i(i_support, i_base)
        i_no_support = pd.read_csv(Path(f"case{i}/no_support/output/output_current.csv"), header=1, index_col=0)
        i_no_support = process_i(i_no_support, i_base)

        v_df.loc[f'case{i}_no_support', ['a', 'b', 'c']] = \
            v_no_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real
        v_df.loc[f'case{i}', ['a', 'b', 'c']] = v_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real
        v_df.loc[f'case{i}_increase', ['a', 'b', 'c']] = \
            v_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real - \
            v_no_support.loc['node_1', ['voltA_mag', 'voltB_mag', 'voltC_mag']].values.real

        load = v_support.loc['node_1', ['a', 'b', 'c']] * np.conj(i_support.loc['oh_line_1_2', ['a', 'b', 'c']])
        load_no_support = \
            v_no_support.loc['node_1', ['a', 'b', 'c']] * np.conj(i_no_support.loc['oh_line_1_2', ['a', 'b', 'c']])
        q = load.values.imag
        p = load.values.real
        q_no_support = load_no_support.values.imag
        p_no_support = load_no_support.values.real

        s_df.loc[f'case{i}_no_support', 'p'] = p_no_support.sum()
        s_df.loc[f'case{i}', 'p'] = p.sum()
        s_df.loc[f'case{i}_delta', 'p'] = p.sum() - p_no_support.sum()
        s_df.loc[f'case{i}_no_support', 'q'] = q_no_support.sum()
        s_df.loc[f'case{i}', 'q'] = q.sum()
        s_df.loc[f'case{i}_delta', 'q'] = q.sum() - q_no_support.sum()




    print(v_df)
    print(s_df)

    pass
