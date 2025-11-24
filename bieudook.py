import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === CẤU HÌNH ===
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    sns.set_style("whitegrid")

sns.set_context("paper", font_scale=1.3)
plt.rcParams['figure.figsize'] = (16, 12) 
plt.rcParams['lines.linewidth'] = 2.5

def safe_read_csv(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy file {filename}")
        return None

# LOAD DỮ LIỆU
df_rsrp = safe_read_csv('scenario1_final_rsrp.csv')
df_thpt = safe_read_csv('scenario1_final_throughput.csv')
df_mec = safe_read_csv('scenario1_final_mec_offload.csv')
df_ho = safe_read_csv('scenario1_final_handover_quality.csv')

# === TẠO BỐ CỤC MỚI (3 HÌNH) ===
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 2)

# --- HÌNH 1: RSRP (TOÀN BỘ HÀNG TRÊN) ---
ax1 = fig.add_subplot(gs[0, :]) 
if df_rsrp is not None and not df_rsrp.empty:
    target_ue = 2
    ue_data = df_rsrp[df_rsrp['IMSI'] == target_ue]
    if not ue_data.empty:
        pivot_data = ue_data.pivot_table(index='Time', columns='CellId', values='RSRP')
        pivot_data.plot(ax=ax1, marker='.', markersize=3, alpha=0.8)
        
        if df_ho is not None and not df_ho.empty:
            ho_events = df_ho[df_ho['IMSI'] == target_ue]
            for _, row in ho_events.iterrows():
                ax1.axvline(x=row['Time'], color='red', linestyle='--', linewidth=1.5, alpha=0.8)
                
                # Chữ HO nằm trong hình, dịch trái 2s
                ax1.text(row['Time']-2, 0.95, 'HO Event', 
                         transform=ax1.get_xaxis_transform(),
                         color='red', fontweight='bold', rotation=90,
                         ha='center', va='top', fontsize=10)

        ax1.set_title(f'Signal Strength (RSRP) & Handover Points (UE {target_ue})', fontweight='bold', fontsize=14)
        ax1.set_ylabel('RSRP (dBm)')
        ax1.legend(title='Cell ID', loc='lower right')

# --- HÌNH 2: THROUGHPUT (HÀNG DƯỚI TRÁI) ---
ax2 = fig.add_subplot(gs[1, 0])
if df_thpt is not None and not df_thpt.empty:
    target_ue = 2
    thpt_data = df_thpt[df_thpt['UE_ID'] == target_ue]
    if not thpt_data.empty:
        ax2.plot(thpt_data['Time'].values, thpt_data['Throughput_Mbps'].values, color='#2ca02c', label='Throughput')
        if df_ho is not None and not df_ho.empty:
            ho_events = df_ho[df_ho['IMSI'] == target_ue]
            for _, row in ho_events.iterrows():
                ax2.axvspan(row['Time']-2, row['Time']+2, color='red', alpha=0.15, label='HO Impact')
        
        ax2.set_title('Throughput Stability', fontweight='bold')
        ax2.set_ylabel('Mbps')
        ax2.set_xlabel('Time (s)')
        handles, labels = ax2.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax2.legend(by_label.values(), by_label.keys())

# --- HÌNH 3: MEC LATENCY (HÀNG DƯỚI PHẢI) - [ĐÃ XÓA CHẤM ĐỎ] ---
ax3 = fig.add_subplot(gs[1, 1])
if df_mec is not None and not df_mec.empty:
    target_ue = 2
    mec_data = df_mec[df_mec['UE_ID'] == target_ue].copy()
    if not mec_data.empty:
        mec_data['Latency_ms'] = mec_data['Latency'] * 1000 
        
        # Chỉ vẽ đường xanh, không vẽ chấm đỏ nữa
        ax3.plot(mec_data['Time'].values, mec_data['Latency_ms'].values, 
                 marker='o', markersize=5, color='#1f77b4', label='Latency')
        
        # --- ĐOẠN CODE VẼ CHẤM ĐỎ ĐÃ BỊ XÓA ---
        
        ax3.set_title('MEC Service Latency', fontweight='bold')
        ax3.set_ylabel('Latency (ms)')
        ax3.set_xlabel('Time (s)')
        ax3.legend()

plt.savefig('UAV_MEC_Report_3Charts_Clean.png', dpi=300)
print("✅ Đã vẽ xong: UAV_MEC_Report_3Charts_Clean.png (Không có chấm đỏ)")
