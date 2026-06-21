import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

FIGSIZE = (16, 9)
DPI = 120  # 240 For 4K, 80 for 720p

T = 200
SUB_SAMPLING = 20

###############################################################################

""" Parameters & Differential equation """

sigma = 10
rho = 28
beta = 8 / 3


def derivs(state, t):

    x, y, z = state[0], state[1], state[2]
    res = np.zeros_like(state)

    res[0] = sigma * (y - x)
    res[1] = x * (rho - z) - y
    res[2] = x * y - beta * z

    return res


###############################################################################

# Time range
dt = 0.01
t = np.arange(0.0, T, dt)

# initial state
state = [-5, 5, 5]

# integration
res = integrate.odeint(derivs, state, t)
x, y, z = res[:, 0], res[:, 1], res[:, 2]

###############################################################################

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.view_init(elev=None, azim=None)
# ax.set_axis_bgcolor('black')
# ax.w_xaxis.set_pane_color((0,0,0,0))
# ax.w_yaxis.set_pane_color((0,0,0,0))
# ax.w_zaxis.set_pane_color((0,0,0,0))
# plt.plot(x,y,z, '-', lw=1)

###################################################################################

i_anim_start = 300
i_anim_end = 1000
azim_start = -45.0
azim_end = 135.0

fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
ax = fig.add_subplot(111, projection="3d")

fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.xaxis.set_pane_color((0, 0, 0, 0))
ax.yaxis.set_pane_color((0, 0, 0, 0))
ax.zaxis.set_pane_color((0, 0, 0, 0))
(line,) = ax.plot(np.array([0]), np.array([0]), np.array([0]), "-", lw=1)
ax.set_xlim3d([-30, 30])
ax.set_ylim3d([-30, 30])
ax.set_zlim3d([-10, 50])
(ball,) = ax.plot([], [], [], "o", color="dodgerblue")
ax.view_init(azim=azim_start)


NB_FRAMES = int(np.floor(len(x) / SUB_SAMPLING))


def init():
    line.set_data([], [])
    line.set_3d_properties([])

    ball.set_data([], [])
    ball.set_3d_properties([])
    return line, ball


def animate(i):
    print("Computing frame", i)
    j = i * SUB_SAMPLING
    line.set_data(x[:j], y[:j])
    line.set_3d_properties(z[:j])
    ball.set_data([x[j]], [y[j]])
    ball.set_3d_properties([z[j]])
    if i_anim_start < i < i_anim_end:
        alpha = (i - i_anim_start) / (i_anim_end - i_anim_start)
        ax.view_init(azim=azim_start + (azim_end - azim_start) * alpha)
    return line, ball


ani = animation.FuncAnimation(
    fig,
    animate,
    np.arange(0, NB_FRAMES),
    init_func=init,
    interval=40,
    blit=True,
)

# Uncomment to save the video
# writer = animation.FFMpegWriter(fps=30, bitrate=5000)
# ani.save("11-lorenz 3D.mp4", writer=writer, dpi=DPI)

plt.show()
