import matplotlib.pyplot as plt
from matplotlib.patches import Circle   # arriba, con los imports
import math

MSOL = 1.989e30
MTIERRA = 5.972e24
R_SOL = 6.96e8
CTE_GRAVITACIONAL = 6.674e-11
CANT_SEGUNDOS_POR_PASO = 3600
CANT_PASOS = 10000
def imprimir_tabla(posicion, velocidad, paso_t, cada=100):
    print(f"{'t (s)':>12} {'t (días)':>10} {'x (m)':>14} {'y (m)':>14} {'vx (m/s)':>14} {'vy (m/s)':>14}")
    print("-" * 84)
    n = len(velocidad)  # puede ser una menos que posicion si hubo choque
    for i in range(n):
        if i % cada == 0 or i == n - 1:
            t = i * paso_t
            x, y = posicion[i]
            vx, vy = velocidad[i]
            print(f"{t:12.0f} {t/86400:10.2f} {x:14.4e} {y:14.4e} {vx:14.4e} {vy:14.4e}")

def main():
    print("Posicion recomendada: (149600000000, 0)")
    r0x = int(input("Ingresa la componente x de la posicion inicial: "))
    r0y = int(input("Ingresa la componente y de la posicion inicial: "))
    pos_inicial = (r0x, r0y)

    print("Velocidad recomendada: (0, 29780)")
    v0x = int(input("Ingresa la componente x de la velocidad inicial: "))
    v0y = int(input("Ingresa la componente y de la velocidad inicial: "))
    vel_inicial = (v0x, v0y)
    choco = False
    paso_t = CANT_SEGUNDOS_POR_PASO
    posicion = []
    velocidad = []

    posicion.append(pos_inicial)
    velocidad.append(vel_inicial)

    for i in range(1,CANT_PASOS):

        modulo_r_ant = math.sqrt(posicion[i - 1][0]**2 + posicion[i - 1][1]**2)
        vix = velocidad[i - 1][0] + -CTE_GRAVITACIONAL*MSOL*posicion[i - 1][0]*paso_t/modulo_r_ant**3
        viy = velocidad[i - 1][1] + -CTE_GRAVITACIONAL*MSOL*posicion[i - 1][1]*paso_t/modulo_r_ant**3
        velocidad.append((vix, viy))

        rix = posicion[i - 1][0] + paso_t*vix
        riy = posicion[i - 1][1] + paso_t*viy
        posicion.append((rix, riy))

        if math.sqrt(rix**2 + riy**2) < R_SOL:
            choco = True
            dias_choque = i*paso_t/86400
            print(f"Choque en el paso {i} (~{dias_choque:.1f} días)")
            break
    
        # se necesita la distancia entre la tierra y el sol, pero como el sol es nuestro (0,0) en 
        # nuestro sistema, la distancia es simplemente el modulo del vector posicion de la tierra

    imprimir_tabla(posicion, velocidad, paso_t, cada=100)

    # Coordenadas en millones de kilómetros
    x = [p[0] / 1e9 for p in posicion]
    y = [p[1] / 1e9 for p in posicion]

    # Estilo visual
    fig, ax = plt.subplots(figsize=(10, 10))

    fig.patch.set_facecolor("#080D1A")
    ax.set_facecolor("#080D1A")

    # Trayectoria completa
    ax.plot(
        x, y,
        color="#38BDF8",
        linewidth=2,
        label="Trayectoria",
        zorder=2
    )

    # Posición inicial
    ax.scatter(
        x[0], y[0],
        color="#FFFFFF",
        edgecolors="#38BDF8",
        linewidths=2,
        s=90,
        label="Posición inicial",
        zorder=5
    )

    # Posición final
    ax.scatter(
        x[-1], y[-1],
        color="#FB7185" if choco else "#A78BFA",
        s=65,
        label="Posición final",
        zorder=5
    )

    # Sol brillante
    ax.scatter(
        0, 0,
        color="#FDB813",
        edgecolors="#FFF1A8",
        linewidths=2,
        s=300,
        label="Sol",
        zorder=6
    )

    # Anotación si ocurre un choque
    if choco:
        ax.annotate(
            f"¡Choque con el Sol!\nDía {dias_choque:.2f}",
            xy=(x[-1], y[-1]),
            xytext=(0.05, 0.92),
            textcoords="axes fraction",
            color="#FB7185",
            fontsize=11,
            fontweight="bold",
            arrowprops=dict(
                arrowstyle="->",
                color="#FB7185",
                linewidth=1.5
            )
        )

    # Título y etiquetas
    ax.set_title(
        "ÓRBITA TERRESTRE",
        color="white",
        fontsize=20,
        fontweight="bold",
        pad=22
    )

    ax.set_xlabel(
        "Posición X (millones de km)",
        color="#CBD5E1",
        fontsize=12
    )

    ax.set_ylabel(
        "Posición Y (millones de km)",
        color="#CBD5E1",
        fontsize=12
    )

    # Misma escala en los dos ejes
    ax.set_aspect("equal", adjustable="datalim")

    # Márgenes automáticos para no cortar la trayectoria
    ax.margins(0.15)

    # Cuadrícula sutil
    ax.grid(
        True,
        color="#64748B",
        linestyle="--",
        linewidth=0.7,
        alpha=0.25
    )

    # Colores de los ejes y números
    ax.tick_params(colors="#CBD5E1", labelsize=10)

    for borde in ax.spines.values():
        borde.set_color("#334155")

    # Leyenda
    leyenda = ax.legend(
        loc="upper right",
        facecolor="#111827",
        edgecolor="#334155",
        fontsize=10,
        framealpha=0.95
    )

    for texto in leyenda.get_texts():
        texto.set_color("white")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()