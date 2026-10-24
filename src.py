import matplotlib.pyplot as plt
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
    r0x = int(input("Ingresa la componente x de la posicion inicial: "))
    r0y = int(input("Ingresa la componente y de la posicion inicial: "))
    pos_inicial = (r0x, r0y)

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

    x, y = zip(*posicion)

    plt.figure(figsize=(7, 7))
    plt.plot(x, y, label="Órbita de la Tierra", color="blue")
    plt.plot(0, 0, 'ro', markersize=8, label="Sol")

    if choco:
        # marca el punto del choque y escribe el mensaje en el gráfico
        plt.annotate(f"¡Choque con el Sol!\n(~{dias_choque:.1f} días)",
                     xy=(x[-1], y[-1]),
                     xytext=(0.05, 0.92), textcoords="axes fraction",
                     fontsize=12, color="red", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color="red"))
        plt.title("Simulación de la Órbita Terrestre")
    else:
        plt.title("Simulación de la Órbita Terrestre")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    main()