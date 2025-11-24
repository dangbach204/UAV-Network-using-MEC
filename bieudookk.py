import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === CẤU HÌNH GIAO DIỆN ===
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    sns.set_style("whitegrid")

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['lines.linewidth'] = 2.0

def safe_read_csv(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy file {filename}")
        return None

# LOAD DỮ LIỆU
df_sinr = safe_read_csv('scenario1_final_sinr.csv')
df_ho = safe_read_csv('scenario1_final_handover_quality.csv')

if df_sinr is not None and not df_sinr.empty:
    target_ue = 2
    ue_sinr = df_sinr[df_sinr['IMSI'] == target_ue]
    
    if not ue_sinr.empty:
        # Lọc bỏ giá trị ảo > 60dB
        ue_sinr_clean = ue_sinr[ue_sinr['SINR'] < 60]
        
        plt.figure()
        
        # Vẽ đường SINR
        plt.plot(ue_sinr_clean['Time'].values, ue_sinr_clean['SINR'].values, 
                 color='purple', alpha=0.8, label='SINR (Signal Quality)')
        
        # Vẽ các vạch Handover (nếu có)
        if df_ho is not None and not df_ho.empty:
            ho_events = df_ho[df_ho['IMSI'] == target_ue]
            for _, row in ho_events.iterrows():
                plt.axvline(x=row['Time'], color='red', linestyle='--', linewidth=1.5)
                # Ghi chú HO (Mình giữ nguyên vị trí 52 như code của bạn)
                plt.text(row['Time'], 52, 'HO Event', color='red', fontweight='bold', 
                         ha='center', va='bottom', fontsize=10)

        # --- ĐÃ XÓA CHÚ THÍCH FAST FADING Ở ĐÂY ---

        plt.title(f'SINR Variation with Nakagami Fading (UE {target_ue})', fontweight='bold', fontsize=14)
        plt.ylabel('SINR (dB)', fontsize=12)
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylim(-10, 60) # Giới hạn trục Y chuẩn
        plt.legend(loc='lower right')
        
        plt.tight_layout()
        plt.savefig('SINR_Only_Report.png', dpi=300)
        print("✅ Đã vẽ xong: SINR_Only_Report.png (Đã xóa chữ Fading)")
    else:
        print("Không có dữ liệu cho UE 2")
