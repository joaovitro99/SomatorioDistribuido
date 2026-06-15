from mpi4py import MPI
import math

def calcular_somatorio(inicio, fim):
    """Calcula a soma dos números de inicio até fim"""
    soma = 0
    for i in range(inicio, fim + 1):
        soma += i
    return soma

def main():
    # Inicializa MPI
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    N = comm.Get_size()
    
    somatorio = 0
    soma = 0
    
    # ALTERADO: Início da contagem de tempo
    tempo_inicio = MPI.Wtime()

    if id == 0:
        # Processo mestre lê o número
        numero = int(input("Digite o número: "))
        
        # Envia o número para todos os outros processos
        for i in range(1, N):
            comm.send(numero, dest=i)
    else:
        # Processos escravos recebem o número
        numero = comm.recv(source=0)
    
    # Calcula parcela, início e fim para cada processo
    parcela = numero // N  # Divisão inteira
    inicio = (parcela * id) + 1
    fim = parcela * (id + 1)
    
    if id == N - 1:
        fim = numero
    
    # Cada processo calcula seu somatório parcial
    somatorio = calcular_somatorio(inicio, fim)
    
    # Fase de redução (soma paralela)
    metade = N
    
    while id < metade and metade > 1:
        metade = metade // 2
        soma = somatorio
        
        if id >= metade:
            # Envia para o processo par
            comm.send(soma, dest=(id - metade))
        else:
            # Recebe de processo ímpar
            soma_recebida = comm.recv(source=(id + metade))
            somatorio = somatorio + soma_recebida
    
    # Processo 0 exibe o resultado final
    if id == 0:
        # ALTERADO: Fim da contagem de tempo e exibição formatada
        tempo_fim = MPI.Wtime()
        tempo_total = tempo_fim - tempo_inicio
        print(f"Somatório total: {somatorio}")
        print(f"Tempo de execução em segundos: {tempo_total:.6f}")

if __name__ == "__main__":
    main()