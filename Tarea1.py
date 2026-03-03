import random
import simpy
import statistics

def correr_simulacion(total_procesos, intervalo, RAM_size=100):

    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)

    env = simpy.Environment()

    RAM = simpy.Container(env, init=RAM_size, capacity=RAM_size)
    CPU = simpy.Resource(env, capacity=1)

    tiempos = []

    def source(env, RAM, CPU, total_procesos, intervalo, tiempos):
        for i in range(total_procesos):
            tiempo_llegada = random.expovariate(1.0 / intervalo)
            yield env.timeout(tiempo_llegada)
            env.process(proceso(env, RAM, CPU, tiempos))


    def proceso(env, RAM, CPU, tiempos):

        tiempo_llegada = env.now

        memoria_necesaria = random.randint(1, 10)
        instrucciones = random.randint(10, 50)

        yield RAM.get(memoria_necesaria)

        while instrucciones > 0:

            with CPU.request() as req:
                yield req
                yield env.timeout(1)

                ejecutadas = min(3, instrucciones)
                instrucciones -= ejecutadas

            if instrucciones <= 0:
                break

            decision = random.randint(1, 21)

            if decision == 1:
                yield env.timeout(5)

        yield RAM.put(memoria_necesaria)

        tiempo_total = env.now - tiempo_llegada
        tiempos.append(tiempo_total)

    env.process(source(env, RAM, CPU, total_procesos, intervalo, tiempos))
    env.run()

    promedio = sum(tiempos) / len(tiempos)
    desviacion = statistics.stdev(tiempos)

    return promedio, desviacion

print("Intervalo = 10\n")

for n in [25, 50, 100, 150, 200]:
    promedio, desviacion = correr_simulacion(n, intervalo=10)

    print(f"Procesos: {n}")
    print(f"Tiempo promedio: {promedio:.2f}")
    print(f"Desviación estándar: {desviacion:.2f}")
