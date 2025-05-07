import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go

# Dash App Initialization
app = dash.Dash(__name__)
server = app.server  # For deployment

# App Layout
app.layout = html.Div([
    html.H2("Phasor Diagram Viewer"),
    
    dcc.Graph(id='phasor-plot'),

    html.Div([
        html.Label("Green Vector Magnitude (L)"),
        dcc.Slider(id='L-slider', min=0.5, max=10, step=0.1, value=5,
                   tooltip={"placement": "bottom", "always_visible": True}),
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("H Magnitude"),
        dcc.Slider(id='H-mag-slider', min=0.1, max=5, step=0.1, value=1,
                   tooltip={"placement": "bottom", "always_visible": True}),
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("H Angle (degrees)"),
        dcc.Slider(id='H-angle-slider', min=-180, max=180, step=1, value=0,
                   tooltip={"placement": "bottom", "always_visible": True}),
    ], style={'margin': '20px'})
])

# Helper: Plot Vectors
def create_phasor_figure(L, H_mag, H_angle_deg):
    H_angle_rad = np.deg2rad(H_angle_deg)
    H = H_mag * np.exp(1j * H_angle_rad)

    vec1 = np.array([L, 0])
    vec2 = np.array([2 * H.real, 2 * H.imag])
    vec3 = np.array([-5 * H.imag, 5 * H.real])
    vec4 = vec1 + vec2 + vec3

    # Origins
    o1 = np.array([0, 0])
    o2 = o1 + vec1
    o3 = o2 + vec2
    o4 = np.array([0, 0])  # Resultant from origin

    starts = [o1, o2, o3, o4]
    vectors = [vec1, vec2, vec3, vec4]
    colors = ['green', 'red', 'orange', 'blue']
    labels = ['Green (L)', 'Red (2H)', 'Orange (5jH)', 'Resultant']

    fig = go.Figure()
    all_points = []

    for start, vec, color, label in zip(starts, vectors, colors, labels):
        end = start + vec
        fig.add_trace(go.Scatter(
            x=[start[0], end[0]],
            y=[start[1], end[1]],
            mode='lines+markers+text',
            marker=dict(size=6),
            line=dict(width=4, color=color),
            text=[None, label],
            textposition="top right",
            name=label
        ))
        all_points.extend([start, end])

    all_points = np.array(all_points)
    x_min, x_max = all_points[:, 0].min() - 2, all_points[:, 0].max() + 2
    y_min, y_max = all_points[:, 1].min() - 2, all_points[:, 1].max() + 2

    mag = np.linalg.norm(vec4)
    angle = np.rad2deg(np.arctan2(vec4[1], vec4[0]))

    fig.update_layout(
        title=f"Resultant: Magnitude = {mag:.2f}, Angle = {angle:.1f}°",
        xaxis=dict(range=[x_min, x_max], zeroline=True),
        yaxis=dict(range=[y_min, y_max], zeroline=True, scaleanchor="x", scaleratio=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=600,
        showlegend=False
    )

    return fig

# Callback to update plot
@app.callback(
    Output('phasor-plot', 'figure'),
    Input('L-slider', 'value'),
    Input('H-mag-slider', 'value'),
    Input('H-angle-slider', 'value')
)
def update_plot(L, H_mag, H_angle):
    return create_phasor_figure(L, H_mag, H_angle)

# Run App
if __name__ == '__main__':
    app.run(debug=True)
