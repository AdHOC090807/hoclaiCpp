import numpy as np, soundfile as sf, matplotlib.pyplot as plt

x, fs = sf.read("noisy.wav")
if x.ndim > 1: x = x.mean(axis=1)      # về mono
M = 5                                    # thử M = 3, 5, 11, 21 rồi chọn

def ma_direct(x, M):
    N = len(x); y = np.zeros(N)
    for n in range(N):
        s = 0.0
        for k in range(M):
            if n - k >= 0:               # biên: x(n<0) = 0
                s += x[n - k]
        y[n] = s / M
    return y

y = ma_direct(x, M)
y /= max(1, np.max(np.abs(y)))           # tránh clip
sf.write(f"filtered_M{M}.wav", y, fs)

t = np.arange(len(x)) / fs
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 5))
ax[0].plot(t, x);  ax[0].set_title("Trước lọc")
ax[1].plot(t, y);  ax[1].set_title(f"Sau lọc (M={M})")
ax[1].set_xlabel("Thời gian (s)")
plt.tight_layout(); plt.savefig(f"waveform_M{M}.png", dpi=200)