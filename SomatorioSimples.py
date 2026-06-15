from mpi4py import MPI
import datetime

def somatorio(inicio, fim):
   s=0
   for i in range(inicio, fim+1):
     s=s+i
   
   return s   


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
  print("Digite o número para calcular o somatório:")
  num=int(input())
  
  wt = MPI.Wtime()
  start_time = datetime.datetime.now()
  
  for i in range(1,size):
    comm.send(num, dest=i,tag=1)
    
  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=somatorio(inicio,fim)

  #info = MPI.Status()
  for i in range(1,size):
     info = MPI.Status() 
     s=comm.recv(source=i,tag=2,status=info)
     print("rank do escravo do qual recebeu=",info.Get_source())
     soma=soma+s
  wt = MPI.Wtime() - wt
  
  end_time = datetime.datetime.now()

  time_diff = (end_time - start_time)
  execution_time = time_diff.total_seconds() 

  print("Resultado final do somatório=",soma)
  print("Tempo de execução em segundos de relógio: ",wt)
  print("Tempo de execução02 em segundos de relógio: ",execution_time)
  
  
else:
  num = comm.recv(source=0,tag=1)
  print ("Escravo de rank %d: %d" % (rank, num))
  
  parte=int(num/size)
  inicio=parte*rank+1
  fim=parte*(rank+1)
  if(rank == size-1):
    fim=num

  soma=somatorio(inicio,fim)
  comm.send(soma, dest=0,tag=2)
  
   
  
