import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
if __name__ == '__main__':
    v_base = 4160/sqrt(3)
    va = pd.read_csv("output/grp_rec_vA_mag.csv", header=8, index_col=0)
    vb = pd.read_csv("output/grp_rec_vB_mag.csv", header=8, index_col=0)
    vc = pd.read_csv("output/grp_rec_vC_mag.csv", header=8, index_col=0)
    va.index = (pd.to_datetime(va.index) - pd.to_datetime(va.index[0])).seconds
    vb.index = (pd.to_datetime(vb.index) - pd.to_datetime(vb.index[0])).seconds
    vc.index = (pd.to_datetime(vc.index) - pd.to_datetime(vc.index[0])).seconds
    fig, ax = plt.subplots(1, 1)
    ax.plot(va.node_1/v_base, label="VA")
    ax.plot(vb.node_1/v_base, label="VB")
    ax.plot(vc.node_1/v_base, label="VC")
    ax.legend()
    ax.set_title('Substation Voltage with Grid Support')
    plt.ylabel('Substation Voltage (p.u.)')
    plt.xlabel('Time (s)')
    plt.show()
    pass