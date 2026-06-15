from mpi4py import MPI
import math

def calcular_somatorio(inicio, fim):
    """Calcula a soma dos números de inicio até fim"""
    # ALTERADO: Mudado para laço for para gerar tempo computacional real
    soma = 0
    for i in range(inicio, fim + 1):
        soma += i
    return soma

def configurar_pedacos(numero_total, num_escravos, fator=2):
    """Configura os pedaços para distribuição"""
    pedacos = num_escravos * fator
    parte = numero_total // pedacos
    
    vetinic = []
    vetfim = []
    
    for i in range(pedacos):
        inicio = i * parte + 1
        fim = (i + 1) * parte
        
        if i == pedacos - 1 and fim != numero_total:
            fim = numero_total
        
        vetinic.append(inicio)
        vetfim.append(fim)
    
    return vetinic, vetfim

def mestre():
    comm = MPI.COMM_WORLD
    N = comm.Get_size()
    num_escravos = N - 1
    
    # Configuração
    valor = int(input("Digite o valor N para somar de 1 até N: "))
    fator = int(input("Digite o fator de balanceamento (ex: 2, 3, 4): "))
    
    # ALTERADO: Início da medição de tempo
    tempo_inicio = MPI.Wtime()
    
    # Cria os pedaços
    vetinic, vetfim = configurar_pedacos(valor, num_escravos, fator)
    pedacos = len(vetinic)
    
    print(f"\nMestre: {pedacos} pedaços para {num_escravos} escravos")
    print("="*60)
    
    # Distribuição inicial
    foi = 0
    for i in range(1, N):
        if foi < pedacos:
            comm.send((vetinic[foi], vetfim[foi]), dest=i, tag=1)
            print(f"Mestre -> Escravo {i}: pedaço {foi} [{vetinic[foi]}..{vetfim[foi]}]")
            foi += 1
    
    # Coleta e redistribuição
    somapar = 0
    pedacos_ativos = min(foi, pedacos)
    
    while foi < pedacos or pedacos_ativos > 0:
        # Recebe resultado
        status = MPI.Status()
        resultado = comm.recv(source=MPI.ANY_SOURCE, tag=2, status=status)
        id_escravo = status.Get_source()
        
        if isinstance(resultado, tuple):
            soma_esc, num_pedacos = resultado
        else:
            soma_esc, num_pedacos = resultado, 1
        
        somapar += soma_esc
        pedacos_ativos -= num_pedacos
        
        print(f"Mestre <- Escravo {id_escravo}: soma={soma_esc}")
        
        # Envia próximo pedaço se houver
        if foi < pedacos:
            comm.send((vetinic[foi], vetfim[foi]), dest=id_escravo, tag=1)
            print(f"Mestre -> Escravo {id_escravo}: pedaço {foi} [{vetinic[foi]}..{vetfim[foi]}]")
            foi += 1
            pedacos_ativos += 1
    
    # Sinaliza término
    for i in range(1, N):
        comm.send(-1, dest=i, tag=1)
    
    # Sinaliza término
    for i in range(1, N):
        comm.send(-1, dest=i, tag=1)
        
    # ALTERADO: Fim da medição de tempo e exibição do resultado
    tempo_fim = MPI.Wtime()
    tempo_total = tempo_fim - tempo_inicio
    
    print("\n" + "="*60)
    print(f"RESULTADO FINAL: Somatório de 1 até {valor} = {somapar}")
    print(f"Tempo de execução em segundos: {tempo_total:.6f}")
    print("="*60)

def escravo():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    count = 0
    
    while True:
        # Recebe dados do mestre
        dados = comm.recv(source=0, tag=1)
        
        if dados == -1:
            print(f"Escravo {rank}: Terminando após {count} cálculos")
            break
        
        inicio, fim = dados
        print(f"Escravo {rank}: Calculando [{inicio}..{fim}]")
        
        # Calcula somatório
        soma_parcial = calcular_somatorio(inicio, fim)
        count += 1
        
        # Envia resultado
        comm.send(soma_parcial, dest=0, tag=2)
        print(f"Escravo {rank}: Enviou soma={soma_parcial}")

def main():
    rank = MPI.COMM_WORLD.Get_rank()
    
    if rank == 0:
        print("\n" + "="*60)
        print("PROGRAMA DE SOMATÓRIO COM BALANCEAMENTO DE CARGA")
        print("="*60 + "\n")
        mestre()
    else:
        escravo()

if __name__ == "__main__":
    main()