import matplotlib.pyplot as plt
import math

MSOL = 1.989e30
MTIERRA = 5.972e24
CTE_GRAVITACIONAL = 6.674e-11

def main():
    #r0x = int(input("Ingresa la componente x de la posicion inicial: "))
    #r0y = int(input("Ingresa la componente y de la posicion inicial: "))
    pos_inicial = (1.496e11, 0)

    #v0x = int(input("Ingresa la componente x de la velocidad inicial: "))
    #v0y = int(input("Ingresa la componente y de la velocidad inicial: "))
    vel_inicial = (0, 29780)

    paso_t = 3600


    

    posicion = []
    velocidad = []

    posicion.append(pos_inicial)
    velocidad.append(vel_inicial)

    for i in range(1,10000):
        rix = posicion[i - 1][0] + paso_t*velocidad[i - 1][0]
        riy = posicion[i - 1][1] + paso_t*velocidad[i - 1][1]
        posicion.append((rix, riy))

        modulo_r_ant = math.sqrt(posicion[i - 1][0]**2 + posicion[i - 1][1]**2)
        vix = velocidad[i - 1][0] + -CTE_GRAVITACIONAL*MSOL*posicion[i - 1][0]*paso_t/modulo_r_ant**3
        viy = velocidad[i - 1][1] + -CTE_GRAVITACIONAL*MSOL*posicion[i - 1][1]*paso_t/modulo_r_ant**3
        velocidad.append((vix, viy))
        # se necesita la distancia entre la tierra y el sol, pero como el sol es nuestro (0,0) en 
        # nuestro sistema, la distancia es simplemente el modulo del vector posicion de la tierra

    x, y = zip(*posicion)  # separa en dos tuplas: (1,3,5,7) y (2,4,1,6)
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Trayectoria")
    plt.show()

if __name__ == "__main__":
    main()