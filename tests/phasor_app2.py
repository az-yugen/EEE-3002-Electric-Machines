import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Phasor Diagram with Matplotlib in Streamlit")

# Sliders
L = st.slider("Green Vector Magnitude (L)", 0.1, 10.0, 5.0, step=0.1)
H_mag = st.slider("H Magnitude", 0.1, 5.0, 1.0, step=0.1)
H_angle_deg = st.slider("H Angle (degrees)", -180, 180, 0, step=1)

# Calculate phasor H
H_angle_rad = np.deg2rad(H_angle_deg)
H = H_mag * np.exp(1j * H_angle_rad)

# Vectors
vec1 = np.array([L, 0])                         # Green
vec2 = np.array([2 * H.real, 2 * H.imag])       # Red = 2H
vec3 = np.array([-5 * H.imag, 5 * H.real])      # Orange = 5jH
vec4 = vec1 + vec2 + vec3                       # Blue = Resultant

# Origins
origin1 = np.array([0, 0])
origin2 = origin1 + vec1
origin3 = origin2 + vec2

# Plotting
fig, ax = plt.subplots()
ax.set_title("Phasor Diagram (Complex Plane)")

def draw_vector(ax, start, vec, color, label):
    ax.arrow(start[0], start[1], vec[0], vec[1],
             head_width=0.2, head_length=0.3, fc=color, ec=color, length_includes_head=True)
    end = start + vec
    ax.text(end[0], end[1], label, fontsize=10, color=color)

# Draw all vectors
draw_vector(ax, origin1, vec1, 'green', 'Green (L)')
draw_vector(ax, origin2, vec2, 'red', 'Red (2H)')
draw_vector(ax, origin3, vec3, 'orange', 'Orange (5jH)')
draw_vector(ax, origin1, vec4, 'blue', 'Resultant')

# Dynamic axis limits
all_points = np.array([
    origin1, origin2, origin3, origin1 + vec4,
    origin1 + vec1, origin2 + vec2, origin3 + vec3
])
x_min, x_max = np.min(all_points[:, 0]) - 2, np.max(all_points[:, 0]) + 2
y_min, y_max = np.min(all_points[:, 1]) - 2, np.max(all_points[:, 1]) + 2
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.grid(True)

# Resultant info
mag_res = np.linalg.norm(vec4)
angle_res = np.rad2deg(np.arctan2(vec4[1], vec4[0]))
st.markdown(f"### 🔵 Resultant Vector")
st.markdown(f"- Magnitude: **{mag_res:.2f}**")
st.markdown(f"- Angle: **{angle_res:.1f}°**")

# Show plot
st.pyplot(fig)
