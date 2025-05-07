import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Streamlit UI ---
st.set_page_config(page_title="Phasor Visualizer", layout="centered")

st.title("Phasor Vector Visualization")

# Sliders
L = st.slider("Green Vector Magnitude (L)", 0.1, 10.0, 5.0, step=0.1)
H_mag = st.slider("H Magnitude", 0.1, 5.0, 1.0, step=0.1)
H_angle_deg = st.slider("H Angle (degrees)", -180, 180, 0)

# --- Compute Vectors ---
H_angle_rad = np.deg2rad(H_angle_deg)
H = H_mag * np.exp(1j * H_angle_rad)

vec1 = np.array([L, 0])                         # Green
vec2 = np.array([2 * H.real, 2 * H.imag])       # Red = 2H
vec3 = np.array([-5 * H.imag, 5 * H.real])      # Orange = 5jH
vec4 = vec1 + vec2 + vec3                       # Blue = Resultant

# Origins
origin1 = np.array([0, 0])
origin2 = origin1 + vec1
origin3 = origin2 + vec2
origin4 = np.array([0, 0])

# Plotly Figure
fig = go.Figure()

# Add vectors as arrows
def add_vector(fig, start, vec, color, name):
    end = start + vec
    fig.add_trace(go.Scatter(
        x=[start[0], end[0]],
        y=[start[1], end[1]],
        mode="lines+markers",
        marker=dict(size=4),
        line=dict(color=color, width=4),
        name=name
    ))
    # Add arrowhead
    fig.add_annotation(
        ax=start[0], ay=start[1],
        x=end[0], y=end[1],
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor=color,
        opacity=0.8
    )

add_vector(fig, origin1, vec1, "lime", "Green (L)")
add_vector(fig, origin2, vec2, "red", "Red (2H)")
add_vector(fig, origin3, vec3, "orange", "Orange (5jH)")
add_vector(fig, origin4, vec4, "deepskyblue", "Resultant")

# Compute magnitude and angle of resultant
mag_res = np.linalg.norm(vec4)
angle_res = np.rad2deg(np.arctan2(vec4[1], vec4[0]))

# Add result text
st.markdown(f"### 🔵 Resultant Vector")
st.markdown(f"- Magnitude: **{mag_res:.2f}**")
st.markdown(f"- Angle: **{angle_res:.1f}°**")

# Fit axes dynamically
all_points = np.array([
    origin1, origin2, origin3, origin4,
    origin1 + vec1, origin2 + vec2, origin3 + vec3, origin4 + vec4
])
x_range = [np.min(all_points[:, 0]) - 2, np.max(all_points[:, 0]) + 2]
y_range = [np.min(all_points[:, 1]) - 2, np.max(all_points[:, 1]) + 2]

fig.update_layout(
    title="Phasor Diagram (Complex Plane)",
    xaxis=dict(range=x_range, zeroline=True),
    yaxis=dict(range=y_range, zeroline=True),
    showlegend=True,
    height=600,
)

fig.update_yaxes(scaleanchor="x", scaleratio=1)  # Equal aspect ratio

# Show plot
st.plotly_chart(fig, use_container_width=True)
