import os
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# 1. CÁC HÀM TÍNH TOÁN SHORT-TIME ENERGY (STE)
# ==========================================

def compute_ste_db(signal, sr, frame_len_ms=100, frame_shift_ms=10):
    """
    Chia khung và tính Short-time Energy (STE) theo thang đo dB.
    - frame_len_ms: 100 ms (theo đề bài)
    - frame_shift_ms: 10 ms (theo đề bài)
    """
    frame_len = int(sr * frame_len_ms / 1000)
    frame_shift = int(sr * frame_shift_ms / 1000)
    
    # Số lượng frame
    num_frames = 1 + int((len(signal) - frame_len) / frame_shift)
    ste = []
    time_axis = []
    
    for i in range(num_frames):
        start = i * frame_shift
        end = start + frame_len
        frame = signal[start:end]
        
        # Năng lượng của frame: E = sum(x^2)
        energy = np.sum(frame ** 2)
        
        # Tránh log(0) bằng hằng số eps nhỏ
        energy_db = 10 * np.log10(energy + 1e-12)
        
        ste.append(energy_db)
        # Thời điểm tâm hoặc bắt đầu của frame (tính bằng giây)
        time_axis.append(start / sr)
        
    return np.array(ste), np.array(time_axis)


# ==========================================
# 2. CÁC THUẬT TOÁN TỰ ĐỘNG TÌM NGƯỠNG VÀ N1, N2
# ==========================================

def find_speech_boundaries(ste, time_axis, threshold, min_duration=0.1):
    """
    Tìm thời điểm bắt đầu (N1) và kết thúc (N2) dựa vào ngưỡng threshold.
    """
    is_speech = ste > threshold
    speech_indices = np.where(is_speech)[0]
    
    if len(speech_indices) == 0:
        return 0.0, 0.0
    
    n1 = time_axis[speech_indices[0]]
    n2 = time_axis[speech_indices[-1]]
    return n1, n2

def vad_baseline(ste, time_axis, sr, init_noise_sec=1.0):
    """
    Thuật toán Baseline theo đề:
    Lấy giá trị STE lớn nhất trong 1s đầu tiên làm ngưỡng.
    """
    noise_frames = int(init_noise_sec / (time_axis[1] - time_axis[0]))
    noise_frames = min(noise_frames, len(ste))
    
    # Ngưỡng là max năng lượng trong 1s đầu
    theta = np.max(ste[:noise_frames])
    n1, n2 = find_speech_boundaries(ste, time_axis, theta)
    return theta, n1, n2

def vad_proposed_adaptive(ste, time_axis, sr, init_noise_sec=1.0, alpha=3.0):
    """
    Thuật toán đề xuất 1: Thích nghi thống kê (Mean + alpha * Std)
    Tính trung bình và độ lệch chuẩn của 1s nhiễu đầu tiên để tạo ngưỡng chịu nhiễu tốt hơn.
    """
    noise_frames = int(init_noise_sec / (time_axis[1] - time_axis[0]))
    noise_frames = min(noise_frames, len(ste))
    
    mu_noise = np.mean(ste[:noise_frames])
    std_noise = np.std(ste[:noise_frames])
    
    # Ngưỡng thích nghi
    theta = mu_noise + alpha * std_noise
    n1, n2 = find_speech_boundaries(ste, time_axis, theta)
    return theta, n1, n2

def vad_proposed_minmax(ste, time_axis, weight=0.35):
    """
    Thuật toán đề xuất 2: Phân tách Min-Max theo phân phối năng lượng
    Ngưỡng nằm ở khoảng giữa Min và Max của cả đoạn tín hiệu.
    """
    min_e = np.min(ste)
    max_e = np.max(ste)
    theta = min_e + weight * (max_e - min_e)
    n1, n2 = find_speech_boundaries(ste, time_axis, theta)
    return theta, n1, n2


# ==========================================
# 3. HÀM VẼ ĐỒ THỊ TÍN HIỆU VÀ NĂNG LƯỢNG STE
# ==========================================

def plot_vad_result(signal, sr, ste, time_axis, theta, n1, n2, title, save_path=None):
    time_signal = np.linspace(0, len(signal) / sr, len(signal))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    # Đồ thị 1: Tín hiệu âm thanh theo thời gian
    ax1.plot(time_signal, signal, color='blue', alpha=0.6, label='Tín hiệu gốc')
    ax1.axvline(n1, color='green', linestyle='--', linewidth=1.5, label=f'N1 (Bắt đầu): {n1:.2f}s')
    ax1.axvline(n2, color='red', linestyle='--', linewidth=1.5, label=f'N2 (Kết thúc): {n2:.2f}s')
    ax1.set_title(f'Tín hiệu âm thanh - {title}')
    ax1.set_ylabel('Biên độ')
    ax1.legend(loc='upper right')
    ax1.grid(True)
    
    # Đồ thị 2: Năng lượng thời gian ngắn (STE theo dB)
    ax2.plot(time_axis, ste, color='purple', label='STE (dB)')
    ax2.axhline(theta, color='orange', linestyle='-', linewidth=1.5, label=f'Ngưỡng (theta): {theta:.2f} dB')
    ax2.axvline(n1, color='green', linestyle='--', linewidth=1.5)
    ax2.axvline(n2, color='red', linestyle='--', linewidth=1.5)
    ax2.set_title('Short-time Energy (dB)')
    ax2.set_xlabel('Thời gian (giây)')
    ax2.set_ylabel('Năng lượng (dB)')
    ax2.legend(loc='upper right')
    ax2.grid(True)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


# ==========================================
# 4. CHƯƠNG TRÌNH CHÍNH & TÍNH TOÁN MSE BẢNG KẾT QUẢ
# ==========================================

def main():
    AUDIO_DIR = "wav_chuan_hoa"
    GT_CSV_PATH = "ground_truth.csv"
    OUTPUT_PLOT_DIR = "vad_plots"
    os.makedirs(OUTPUT_PLOT_DIR, exist_ok=True)
    
    # Đọc dữ liệu Ground Truth
    gt_df = pd.read_csv(GT_CSV_PATH)
    
    records = []
    
    for _, row in gt_df.iterrows():
        fname = row['filename']
        env = row['environment']
        theta_gt = row['theta_manual']
        n1_gt = row['n1_manual']
        n2_gt = row['n2_manual']
        
        filepath = os.path.join(AUDIO_DIR, fname)
        if not os.path.exists(filepath):
            continue
            
        signal, sr = sf.read(filepath)
        
        # Đảm bảo tín hiệu là 1 kênh Mono
        if len(signal.shape) > 1:
            signal = signal[:, 0]
            
        ste, time_axis = compute_ste_db(signal, sr, frame_len_ms=100, frame_shift_ms=10)
        
        # 1. Chạy Baseline
        th_base, n1_base, n2_base = vad_baseline(ste, time_axis, sr)
        records.append({
            'filename': fname, 'env': env, 'method': 'Baseline (Max 1s noise)',
            'theta_pred': th_base, 'n1_pred': n1_base, 'n2_pred': n2_base,
            'theta_gt': theta_gt, 'n1_gt': n1_gt, 'n2_gt': n2_gt
        })
        
        # 2. Chạy Đề xuất 1 (Adaptive Mean + Std)
        th_prop1, n1_prop1, n2_prop1 = vad_proposed_adaptive(ste, time_axis, sr)
        records.append({
            'filename': fname, 'env': env, 'method': 'Proposed 1 (Mean + 3*Std)',
            'theta_pred': th_prop1, 'n1_pred': n1_prop1, 'n2_pred': n2_prop1,
            'theta_gt': theta_gt, 'n1_gt': n1_gt, 'n2_gt': n2_gt
        })
        
        # 3. Chạy Đề xuất 2 (Min-Max Ratio)
        th_prop2, n1_prop2, n2_prop2 = vad_proposed_minmax(ste, time_axis)
        records.append({
            'filename': fname, 'env': env, 'method': 'Proposed 2 (Min-Max Ratio)',
            'theta_pred': th_prop2, 'n1_pred': n1_prop2, 'n2_pred': n2_prop2,
            'theta_gt': theta_gt, 'n1_gt': n1_gt, 'n2_gt': n2_gt
        })
        
        # Vẽ minh họa cho file đầu tiên của mỗi môi trường
        plot_vad_result(
            signal, sr, ste, time_axis, th_prop1, n1_prop1, n2_prop1,
            title=f"{fname} ({env})",
            save_path=os.path.join(OUTPUT_PLOT_DIR, f"{fname}.png")
        )

    # ==========================================
    # TÍNH TOÁN MSE VÀ TẠO BẢNG TỔNG HỢP
    # ==========================================
    res_df = pd.DataFrame(records)
    
    # Tính sai số bình phương
    res_df['sq_err_theta'] = (res_df['theta_pred'] - res_df['theta_gt']) ** 2
    res_df['sq_err_n1'] = (res_df['n1_pred'] - res_df['n1_gt']) ** 2
    res_df['sq_err_n2'] = (res_df['n2_pred'] - res_df['n2_gt']) ** 2
    
    # Gom nhóm theo phương pháp và tính Mean Squared Error (MSE)
    summary_table = res_df.groupby('method').agg(
        MSE_theta=('sq_err_theta', 'mean'),
        MSE_N1=('sq_err_n1', 'mean'),
        MSE_N2=('sq_err_n2', 'mean')
    ).reset_index()
    
    # Đổi tên cột chuẩn theo đúng yêu cầu đề bài
    summary_table.columns = ['Phương pháp', 'MSE ngưỡng theta', 'MSE N1 (giá trị xuất hiện)', 'MSE N2 (giá trị kết thúc)']
    
    print("\n--- BẢNG KẾT QUẢ SO SÁNH ĐỘ CHÍNH XÁC ---")
    print(summary_table.to_string(index=False))
    
    # Xuất ra file Excel/CSV để nộp báo cáo
    summary_table.to_csv("bang_so_sanh_mse.csv", index=False)
    print("\nĐã lưu bảng so sánh vào 'bang_so_sanh_mse.csv' và đồ thị vào thư mục 'vad_plots/'")

if __name__ == "__main__":
    main()