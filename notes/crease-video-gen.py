#!/usr/bin/env python3
"""
Crease as projection: trajectories flowing in phase space, projecting onto their invariant.
Audio: frequency modulation converging to a single lock as projection completes.
"""

import numpy as np
from PIL import Image, ImageDraw
import subprocess, os

# ---- Parameters ----
N_FRAMES = 200
W, H = 800, 640
sr = 44100
DURATION = 5.0  # seconds

# Lorenz attractor
sigma = 10.0; rho = 28.0; beta = 8.0 / 3.0

# ---- Generate trajectories ----
def lorenz_deriv(state):
    x, y, z = state
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

def rk4_step(state, dt):
    k1 = lorenz_deriv(state)
    k2 = lorenz_deriv(state + 0.5 * dt * k1)
    k3 = lorenz_deriv(state + 0.5 * dt * k2)
    k4 = lorenz_deriv(state + dt * k3)
    return state + dt / 6.0 * (k1 + 2*k2 + 2*k3 + k4)

# Full attractor for skeleton
attractor = []
state = np.array([0., 0., 1.], dtype=float)
for _ in range(20000):
    state = rk4_step(state, 0.01)
    if _ > 5000:
        attractor.append(state[:2])
attractor = np.array(attractor)

# Multiple trajectories
initial_conditions = [
    [1.0, 1.0, 1.0], [-1.0, -1.0, 1.5], [2.0, -1.0, 0.5],
    [-2.0, 0.5, 2.0], [0.5, 2.0, -0.5], [-0.5, -2.0, -1.0],
]
all_steps = 5000
trajs_2d = []
for ic in initial_conditions:
    state = np.array(ic, dtype=float)
    traj = []
    for _ in range(all_steps):
        state = rk4_step(state, 0.005)
        traj.append(state[:2])
    trajs_2d.append(np.array(traj))

# ---- Colors ----
teal = (0, 184, 184)
amber = (255, 140, 0)
bg = (12, 12, 18)
skeleton = (30, 30, 40)

def lerp_color(t):
    """Teal (t=0) to amber (t=1)"""
    r = int(teal[0] * (1-t) + amber[0] * t)
    g = int(teal[1] * (1-t) + amber[1] * t)
    b = int(teal[2] * (1-t) + amber[2] * t)
    return (r, g, b)

# ---- Coordinate transform ----
def to_pix(x, y):
    """Map from (-25,25) world space to pixel coordinates"""
    px = (x + 25) / 50 * W
    py = (1 - (y + 25) / 50) * H
    return int(px), int(py)

# ---- Generate audio ----
t_audio = np.linspace(0, DURATION, int(sr * DURATION))
freq1 = 220.0 + 5.0 * np.exp(-3 * t_audio)
freq2 = 220.0 - 5.0 * np.exp(-3 * t_audio)
audio = 0.3 * (np.sin(2*np.pi*freq1*t_audio) + np.sin(2*np.pi*freq2*t_audio)) * np.exp(-0.5*t_audio)
audio += 0.15 * np.sin(2*np.pi*55*t_audio) * np.exp(-0.5*t_audio)
audio = audio / np.max(np.abs(audio)) * 0.9

audio_path = './assets/crease-projection.wav'
subprocess.run([
    'sox', '-r', str(sr), '-b', '16', '-e', 'signed-integer',
    '-c', '1', '-t', 'raw', '-r', str(sr), '-b', '16',
    '-', audio_path
], input=(audio * 32767).astype(np.int16).tobytes(), check=True)

# ---- Render frames ----
# Pre-render skeleton to avoid drawing every frame
skeleton_img = Image.new('RGB', (W, H), bg)
draw_s = ImageDraw.Draw(skeleton_img)
if len(attractor) > 1:
    pts = [to_pix(attractor[i,0], attractor[i,1]) for i in range(len(attractor))]
    draw_s.line(pts, fill=skeleton, width=1)

texts = [
    ('initial conditions', 20, 30),
    ('approach', 50, 90),
    ('collapse — trajectories forget their paths', 90, 140),
    ('projection — forgetting the time', 140, 180),
    ('the crease remains', 180, 200),
]

for frame_idx in range(N_FRAMES):
    progress = frame_idx / (N_FRAMES - 1)

    img = skeleton_img.copy()
    draw = ImageDraw.Draw(img)

    # Visible trajectory length
    vis_steps = int(progress * all_steps)

    for i, ic in enumerate(initial_conditions):
        t = i / len(initial_conditions)
        color = lerp_color(t)
        alpha = int(180 * (1 - progress * 0.3))

        traj = trajs_2d[i][:vis_steps]
        if len(traj) > 1:
            pts = [to_pix(traj[j,0], traj[j,1]) for j in range(len(traj))]
            draw.line(pts, fill=color, width=1)

        # Current position dot
        if vis_steps > 0:
            dot_pos = to_pix(traj[-1,0], traj[-1,1])
            r = 4
            draw.ellipse([dot_pos[0]-r, dot_pos[1]-r, dot_pos[0]+r, dot_pos[1]+r],
                        fill=color)

    # Title text
    for text, lo, hi in texts:
        if lo <= frame_idx <= hi:
            alpha = min(1.0, (frame_idx - lo) / 15.0) * min(1.0, (hi - frame_idx) / 15.0)
            if alpha > 0:
                # Simple text rendering
                draw.text((W//2 - 100, 30), text, fill=(200, 200, 200))
                break

    # Time indicator
    t_sim = vis_steps * 0.005
    time_str = f't = {t_sim:.1f}'
    draw.text((10, H - 30), time_str, fill=(100, 100, 120))

    img.save(f'./assets/crease-frame-{frame_idx:04d}.png')

    if (frame_idx + 1) % 50 == 0:
        print(f"  Frame {frame_idx+1}/{N_FRAMES}")

# ---- Encode video ----
video_path = './assets/crease-projection.webm'
subprocess.run([
    'ffmpeg', '-y', '-framerate', '20',
    '-i', './assets/crease-frame-%04d.png',
    '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuv420p', '-crf', '30',
    '-b:v', '0',
    video_path
], check=True)

# ---- Merge audio into video ----
final_path = './assets/crease-projection-final.webm'
subprocess.run([
    'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
    '-c:v', 'copy', '-c:a', 'libopus', '-b:a', '96k', '-strict', '-2',
    '-shortest', final_path
], check=True)

# Clean up frames and intermediate files
for f in range(N_FRAMES):
    os.remove(f'./assets/crease-frame-{f:04d}.png')
os.remove(video_path)

print(f"Video+Audio: {final_path} ({os.path.getsize(final_path)//1024} KB)")
print(f"Audio: {audio_path} ({os.path.getsize(audio_path)//1024} KB)")
print("Done.")
