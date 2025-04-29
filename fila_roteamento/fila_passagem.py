


from RandomGenerator import RandomGenerator
from Fila import Evento,  Fila
from TabelaSorteio import ObjetoSorteio, TabelaSorteio
from TipoEvento import TipoEvento
from math import inf

from utils import agenda_saida_ou_passagem, normaliza_tempo_total_execucao




X_inicil = 707
a = 927
c = 467
M = 1000
count = 100000
tempo_primeiro_cliente= 2.0

################## Inicializando

random_generator = RandomGenerator(numero_inicial=X_inicil, a=a, c=c, M=M, limit=count)





################### Inicializa Filas
fila_1 = Fila( 
    identificador_fila= "1",
    lista_eventos=[],
    tamanho_fila= inf,
    numero_servidores= 1,
    range_chegada=(2 , 4),
    range_atendimento=( 1, 2)
    )
fila_1.lista_eventos.append(Evento(tipo_evento=TipoEvento.VAZIO, fila=0, tempo=0, estados= [0] ))


fila_2 = Fila(
    identificador_fila= "2",
    lista_eventos=[],
    tamanho_fila= 5,
    numero_servidores= 3,
    range_chegada=(0 , 0),
    range_atendimento=( 2, 4)
)
fila_2.lista_eventos.append(Evento(tipo_evento=TipoEvento.VAZIO, fila=0, tempo=0, estados= [0] * (fila_2.tamanho_fila + 1) ))


fila_3 = Fila(
    identificador_fila= "3",
    lista_eventos=[],
    tamanho_fila= 2,
    numero_servidores= 2,
    range_chegada=(0 , 0),
    range_atendimento=( 3, 6)
)
fila_3.lista_eventos.append(Evento(tipo_evento=TipoEvento.VAZIO, fila=0, tempo=0, estados= [0] * (fila_3.tamanho_fila + 1) ))

fila_4 = Fila( 
    identificador_fila= "4",
    lista_eventos=[],
    tamanho_fila= 10,
    numero_servidores= 2,
    range_chegada=(0 , 0),
    range_atendimento=( 2, 4)
    )
fila_4.lista_eventos.append(Evento(tipo_evento=TipoEvento.VAZIO, fila=0, tempo=0, estados= [0] * (fila_4.tamanho_fila + 1) ))
#################### Adiciona subfilas

fila_1.adiciona_subfilas(
    [
        {
            "ObjetoFila": fila_2,
            "Lower_bound_prob": 0,
            "Upper_bound_prob": 0.7
        },
        {
            "ObjetoFila": fila_3,
            "Lower_bound_prob": 0.7,
            "Upper_bound_prob": 1
        }
    ]
)


fila_2.adiciona_subfilas(
    [
        {
            "ObjetoFila": fila_4,
            "Lower_bound_prob": 0.1,
            "Upper_bound_prob": 0.9
        },
        {
            "ObjetoFila": fila_3,
            "Lower_bound_prob": 0.9,
            "Upper_bound_prob": 1
        }
    ]
)


fila_3.adiciona_subfilas(
    [
        {
            "ObjetoFila": fila_3,
            "Lower_bound_prob": 0,
            "Upper_bound_prob": 0.1
        },
        {
            "ObjetoFila": fila_4,
            "Lower_bound_prob": 0.1,
            "Upper_bound_prob": 1
        }
    ]
)

fila_4.adiciona_subfilas(
    [
        {
            "ObjetoFila": fila_2,
            "Lower_bound_prob": 0,
            "Upper_bound_prob": 0.2
        }
    ]
)
########################




######### Tabela de registro de Sorteio!
# sorteio_eventos : List[SorteioEvento] = []
tabela_sorteio = TabelaSorteio( [] , random_generator)

tabela_sorteio.adiciona_evento(
    tipo_evento=TipoEvento.CHEGADA,
    tempo=tempo_primeiro_cliente,
    fila=fila_1,
    fila_destino=None
    )


#### Loop de execução
while random_generator.get_counter() > 0:

    sorteio_da_rodada : ObjetoSorteio = tabela_sorteio.get_proximo_sorteio()


    if sorteio_da_rodada == None:
        raise Exception("Tabela de sorteio vazia... finalizando execução")


    if sorteio_da_rodada.tipo_evento == TipoEvento.CHEGADA:

        # Checa se tem servidores disponiveis na fila do objeto sorteio
        fila_tem_servidores_disponiveis = sorteio_da_rodada.fila.fila_tem_servidores_disponiveis()
        
        # Se a fila não está cheia, registra a chegada. 
        if not sorteio_da_rodada.fila.check_fila_cheia():
            novo_evento = sorteio_da_rodada.fila.registra_chegada(sorteio_da_rodada.tempo)

        # 
        if fila_tem_servidores_disponiveis:
            agenda_saida_ou_passagem(
                random_generator=random_generator,
                tabela_sorteio=tabela_sorteio,
                fila_origem=sorteio_da_rodada.fila
            )
            
    elif sorteio_da_rodada.tipo_evento == TipoEvento.PASSAGEM:

        
        novo_evento_saida = sorteio_da_rodada.fila.registra_saida(sorteio_da_rodada.tempo, True)

        if sorteio_da_rodada.fila_destino == None:
            raise Exception(f"Erro, evento de passagem não pode ter uma fila destino como nulo.....")
        
        fila_tem_servidores_disponíveis = sorteio_da_rodada.fila_destino.fila_tem_servidores_disponiveis()
       
        sorteio_da_rodada.fila_destino.registra_chegada(sorteio_da_rodada.tempo)
    
        if fila_tem_servidores_disponiveis:
            agenda_saida_ou_passagem(
                random_generator=random_generator,
                tabela_sorteio=tabela_sorteio,
                fila_origem=sorteio_da_rodada.fila_destino
            )
    elif sorteio_da_rodada.tipo_evento == TipoEvento.SAIDA:

        novo_evento_saida = sorteio_da_rodada.fila.registra_saida(sorteio_da_rodada.tempo, False)
        
        if sorteio_da_rodada.fila.fila_tem_servidores_disponiveis() and sorteio_da_rodada.fila.tem_eventos_em_espera() :
            agenda_saida_ou_passagem(
                random_generator=random_generator,
                tabela_sorteio=tabela_sorteio,
                fila_origem=sorteio_da_rodada.fila
            )
        else:
            print(f"Unexpected: fila nao tem servidores disponiveis ou eventos em espera quando um evento saiu da fila {sorteio_da_rodada.fila.identificador_fila} ")


    if random_generator.get_counter() <= 0 :
            print("Finalizou numeros pseudo aleatorios")
            break
    

    tabela_sorteio.sorteia_evento(
        tipo_evento=TipoEvento.CHEGADA, 
        fila=fila_1,
        fila_destino=None
    )

normaliza_tempo_total_execucao([fila_1, fila_2, fila_3])

print()
print()
print("=====================================================================================")
print(f"Tempos de execução da fila {fila_1.identificador_fila}:")
ultimo_estado_fila_1 = fila_1.lista_eventos[-1]
print(f"Fila com {ultimo_estado_fila_1.fila} eventos.")
for index in range(len( ultimo_estado_fila_1.estados ) ):
    if ultimo_estado_fila_1.estados[index] > 0.5: 
        print(f"Fila {fila_1.identificador_fila} com {index}: { str( ultimo_estado_fila_1.estados[index] ) } - Probabilidade: { str( ultimo_estado_fila_1.estados[index] * 100 / ultimo_estado_fila_1.tempo) } " )

print("Tempo total de execução: " + str(ultimo_estado_fila_1.tempo) + " - Porcentagem: " + str( ultimo_estado_fila_1.tempo* 100 / ultimo_estado_fila_1.tempo) )

print("Eventos perdidos: " + str(fila_1.eventos_perdidos))

print("=====================================================================================")

fila_2.printa_fila()

fila_3.printa_fila()

fila_4.printa_fila()
