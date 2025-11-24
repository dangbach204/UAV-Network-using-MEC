import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === CẤU HÌNH GIAO DIỆN ===
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    sns.set_style("whitegrid")

# Thiết lập kích thước ảnh lớn để chứa đủ 4 biểu đồ
plt.rcParams['figure.figsize'] = (18, 12)
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['font.size'] = 11

def safe_read_csv(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"⚠️ Lỗi: Không tìm thấy file {filename}")
        return None

# === LOAD DỮ LIỆU ===
df_thpt = safe_read_csv('scenario1_final_throughput.csv')
df_flow = safe_read_csv('scenario1_final_flow_stats.csv')

# Tạo khung hình lưới 2 hàng x 2 cột
fig, axes = plt.subplots(2, 2)
# Tăng khoảng cách giữa các hình để không bị dính chữ
plt.subplots_adjust(hspace=0.3, wspace=0.2)

# ========================================================
# HÌNH 1 (Góc Trái Trên): UE 1 THROUGHPUT (STATIC)
# ========================================================
ax1 = axes[0, 0]
if df_thpt is not None:
    ue1 = df_thpt[df_thpt['UE_ID'] == 1]
    if not ue1.empty:
        ax1.plot(ue1['Time'].values, ue1['Throughput_Mbps'].values, color='#1f77b4', label='Throughput')
        ax1.axhline(y=3.0, color='red', linestyle=':', alpha=0.5, label='Expected (3Mbps)')
        ax1.set_title('(A) UE 1 (Static User): Throughput Stability', fontweight='bold')
        ax1.set_ylabel('Mbps')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylim(0, 5)
        ax1.legend()

# ========================================================
# HÌNH 2 (Góc Phải Trên): UE 3 THROUGHPUT (STATIC)
# ========================================================
ax2 = axes[0, 1]
if df_thpt is not None:
    ue3 = df_thpt[df_thpt['UE_ID'] == 3]
    if not ue3.empty:
        ax2.plot(ue3['Time'].values, ue3['Throughput_Mbps'].values, color='#ff7f0e', label='Throughput')
        ax2.axhline(y=3.0, color='red', linestyle=':', alpha=0.5, label='Expected (3Mbps)')
        ax2.set_title('(B) UE 3 (Static User): Throughput Stability', fontweight='bold')
        ax2.set_ylabel('Mbps')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylim(0, 5)
        ax2.legend()

# ========================================================
# HÌNH 3 (Góc Trái Dưới): SO SÁNH TỔNG HỢP (QUAN TRỌNG)
# ========================================================
ax3 = axes[1, 0]
if df_thpt is not None:
    # Vẽ nền mờ cho UE 1 & 3
    if not ue1.empty:
        ax3.plot(ue1['Time'].values, ue1['Throughput_Mbps'].values, label='UE 1 (Static)', color='#1f77b4', alpha=0.4)
    if not ue3.empty:
        ax3.plot(ue3['Time'].values, ue3['Throughput_Mbps'].values, label='UE 3 (Static)', color='#ff7f0e', alpha=0.4)
    
    # Vẽ nổi bật UE 2 (Di chuyển)
    ue2 = df_thpt[df_thpt['UE_ID'] == 2]
    if not ue2.empty:
        ax3.plot(ue2['Time'].values, ue2['Throughput_Mbps'].values, label='UE 2 (Mobile - Handover)', color='red', linewidth=2.5)

    ax3.set_title('(C) Comparison: Mobile vs. Static Users', fontweight='bold', color='darkred')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Time (s)')
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.7)

# ========================================================
# HÌNH 4 (Góc Phải Dưới): SO SÁNH JITTER (BAR CHART)
# ========================================================
ax4 = axes[1, 1]
if df_flow is not None:
    # Fix tên cột
    col_tx = 'TxPkts' if 'TxPkts' in df_flow.columns else 'TxPackets'
    
    # Lấy dữ liệu (Lọc gói tin rác < 100 gói)
    df_clean = df_flow[df_flow[col_tx].values > 100].copy()
    df_clean = df_clean.sort_values('FlowID')
    
    labels = []
    colors = []
    for fid in df_clean['FlowID']:
        if fid == 7: # UE 2
            labels.append(f"UE 2 (Mobile)\nFlow {fid}")
            colors.append('red')
        else:
            labels.append(f"UE Static\nFlow {fid}")
            colors.append('skyblue')

    # Vẽ Bar Chart
    if not df_clean.empty:
        bars = ax4.bar(labels, df_clean['Jitter(ms)'].values, color=colors, alpha=0.9, edgecolor='black')
        
        ax4.set_title('(D) Jitter Comparison (Lower is Better)', fontweight='bold')
        ax4.set_ylabel('Jitter (ms)')
        ax4.set_ylim(0, df_clean['Jitter(ms)'].max() * 1.25) 
        
        # Hiển thị số liệu
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                     f'{height:.2f}ms', ha='center', va='bottom', fontweight='bold')
    else:
        ax4.text(0.5, 0.5, "No Valid Flow Data", ha='center')

# Lưu file ảnh duy nhất
plt.tight_layout()
plt.savefig('Compare & Delay.png', dpi=300)
print("✅ Đã xuất file ảnh tổng hợp: All_In_One_Report.png")
# plt.show()
