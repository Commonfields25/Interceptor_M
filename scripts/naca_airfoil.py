import numpy as np

def get_naca_4digit(m, p, t, c, n=100):
    """
    Returns a NACA 4-digit airfoil profile.
    m: max camber (e.g. 0.02)
    p: position of max camber (e.g. 0.4)
    t: max thickness (e.g. 0.12)
    c: chord length
    """
    x = np.linspace(0, c, n)

    # Thickness distribution
    yt = 5 * t * c * (0.2969 * np.sqrt(x/c) - 0.1260 * (x/c) - 0.3516 * (x/c)**2 + 0.2843 * (x/c)**3 - 0.1015 * (x/c)**4)

    # Camber line
    yc = np.zeros_like(x)
    if m > 0:
        yc[x <= p*c] = m * (x[x <= p*c] / p**2) * (2*p - (x[x <= p*c]/c))
        yc[x > p*c] = m * ((c - x[x > p*c]) / (1-p)**2) * (1 + (x[x > p*c]/c) - 2*p)

    # For symmetric airfoils (m=0), theta is 0
    upper = np.column_stack((x, yc + yt))
    lower = np.column_stack((x, yc - yt))

    return upper, lower

if __name__ == "__main__":
    u, l = get_naca_4digit(0, 0, 0.12, 100)
    print(f"Generated NACA 0012 with {len(u)} points.")
