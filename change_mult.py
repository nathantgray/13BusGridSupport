from glmpy import Gridlabd
import pandas as pd


def change_gen_mult(glm: Gridlabd, mult=1):
    inverters = glm.model.get('inverter', {})
    for inverter_name in inverters.keys():
        s_rated = glm.model['inverter'][inverter_name]['rated_power']
        p_rated = float(s_rated)/1.2
        p_out = p_rated * mult
        glm.model['inverter'][inverter_name]['P_Out'] = p_out
    return glm


def change_load_mult(glm: Gridlabd, power_data: pd.DataFrame, mult=1):
    for load_name in glm.model.get('load', {}):
        node_id = load_name.split('_')[1]
        complex_part = load_name.split('_')[2]
        is_p = complex_part == 'p'
        is_q = complex_part == 'q'
        s_base = power_data.s_base[power_data.id == int(node_id)].values[0]
        p_a = power_data.Pa[power_data.id == int(node_id)].values[0]*s_base*mult
        q_a = power_data.Qa[power_data.id == int(node_id)].values[0]*s_base*mult
        p_b = power_data.Pb[power_data.id == int(node_id)].values[0]*s_base*mult
        q_b = power_data.Qb[power_data.id == int(node_id)].values[0]*s_base*mult
        p_c = power_data.Pc[power_data.id == int(node_id)].values[0]*s_base*mult
        q_c = power_data.Qc[power_data.id == int(node_id)].values[0]*s_base*mult
        if is_p:
            glm.model['load'][load_name]['base_power_A'] = p_a
            glm.model['load'][load_name]['base_power_B'] = p_b
            glm.model['load'][load_name]['base_power_C'] = p_c
        if is_q:
            glm.model['load'][load_name]['base_power_A'] = q_a
            glm.model['load'][load_name]['base_power_B'] = q_b
            glm.model['load'][load_name]['base_power_C'] = q_c
    return glm


if __name__ == '__main__':
    power_data1 = pd.read_csv('powerdata.csv', sep=',', header=0, index_col=False)
    glm1 = Gridlabd('demonstration.glm')
    glm1 = change_gen_mult(glm1, mult=0.5)
    glm1 = change_load_mult(glm1, power_data1, mult=0.5)
    glm1.write('demonstration_50_50.glm')
