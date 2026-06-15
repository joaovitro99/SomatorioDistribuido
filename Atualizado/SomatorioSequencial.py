import time

def calcular_sequencial(numero):
    soma = 0
    for i in range(1, numero + 1):
        soma += i
    return soma

if __name__ == "__main__":
    numero = int(input("Digite um número: "))

    print("Iniciando cálculo sequencial...")

    inicio = time.time()
    resultado = calcular_sequencial(numero)
    fim = time.time()

    print(f"\n[SEQUENCIAL] | Resultado: {resultado}")
    print(f"Tempo de Execução: {fim - inicio:.6f} segundos")