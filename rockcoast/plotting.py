# This module contains plotting routines to visualize cliff evolution.

import matplotlib.pyplot as plt

def setup_plots(Z, X):
    """
    Initialize the interactive plot for profile evolution.

    Parameters:
    - Z (numpy.ndarray): vertical profile
    - X (numpy.ndarray): horizontal profile

    Returns:
    - fig, ax, line: figure, axis, and line object for updates
    """
    fig, ax=plt.subplots(figsize=(8, 6))
    line,=ax.plot(X, Z, color='blue')
    ax.set_xlabel('Distance inland (m)')
    ax.set_ylabel('Elevation (m)')
    ax.set_xlim(X.min(), X.max() + 20)
    ax.set_ylim(Z.min(), Z.max())
    ax.grid()
    return fig, ax, line

def update_profile_plot(line, X, Z):
    """
    Update the cliff profile in the interactive plot.

    Parameters:
    - line (matplotlib line object): existing line
    - X (numpy.ndarray): updated horizontal profile
    - Z (numpy.ndarray): unchanged vertical profile
    """
    line.set_xdata(X)
    line.set_ydata(Z)
    plt.pause(0.01)

def finalize_plots(Z, X, InitialX):
    """
    Plot the final retreat distance profile.

    Parameters:
    - Z (numpy.ndarray): vertical profile
    - X (numpy.ndarray): final horizontal profile
    - InitialX (numpy.ndarray): initial horizontal profile
    """
    plt.figure(figsize=(8, 6))
    plt.plot(X-InitialX, Z, color='red')
    plt.xlabel('Retreat distance (m)')
    plt.ylabel('Elevation (m)')
    plt.title('Final Cliff Retreat Profile')
    plt.grid()
    plt.tight_layout()
    plt.show()
