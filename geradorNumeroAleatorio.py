
from typing import List
from enum import Enum
from typing import List



class TipoEvento(Enum):
    CHEGADA = 'chegada'
    SAIDA = 'saida'
    VAZIO = 'vazio'

class RegistroEventos:

    def __init__(self, 
                 tipo_evento: TipoEvento, 
                 fila : int, 
                 tempo : float, 
                 estados : list[float]):
        
        self.tipo_evento =   tipo_evento 
        self.fila = fila
        self.tempo = tempo
        self.sorteio = None
        self.estados = estados


class SorteioEvento:
        

        def __init__(self, tipo_evento: TipoEvento, tempo_inicial: float,  random_number: float | None):
             self.tipo_evento = tipo_evento
             self.tempo = tempo_inicial

             if random_number != None:
                if self.tipo_evento == TipoEvento.CHEGADA:
                    self.sorteio = 2 + ( ( 5 - 2 ) * random_number)
                elif self.tipo_evento == TipoEvento.SAIDA:
                        self.sorteio = 3 + ( ( 5 - 3 ) * random_number)
                self.tempo += self.sorteio
             else:
                  self.sorteio = None




X_inicil = 707
a = 927
c = 467
M = 1000
count = 100000
numero_servidores = 1

prev = X_inicil
tamanho_fila = 5
eventos_perdidos = 0

def next_random(count, prev, a, c, M):

    count -= 1

    prev = ( ( a * prev ) + c) % M
    return prev / M, count



######### Tabelas de registro de eventos!
registro_eventos : List[RegistroEventos] = []

######### Tabela de registro de Sorteio!
sorteio_eventos : List[SorteioEvento] = []


def get_proximo_sorteio() -> SorteioEvento | None:
    if not sorteio_eventos or len(sorteio_eventos) == 0:
        return None
    
    return min(sorteio_eventos, key=lambda evento: evento.tempo)



def registra_chegada(objeto_sorteio : SorteioEvento, prev, count, eventos_perdidos, numero_servidores):

    ultimo_evento = registro_eventos[-1]

    nova_lista_estados = ultimo_evento.estados.copy()

    tempo_ultimo_evento = ultimo_evento.tempo
    tempo_novo_evento = objeto_sorteio.tempo

    nova_lista_estados[ultimo_evento.fila] = (tempo_novo_evento - tempo_ultimo_evento) + nova_lista_estados[ultimo_evento.fila]

    if ultimo_evento.fila >= tamanho_fila:
        novo_tamanho_fila = ultimo_evento.fila
        eventos_perdidos = eventos_perdidos + 1

    else:
        novo_tamanho_fila = ultimo_evento.fila + 1

    novo_tempo = objeto_sorteio.tempo


    novo_evento = RegistroEventos(
        tipo_evento=TipoEvento.CHEGADA, 
        fila=novo_tamanho_fila, 
        tempo=novo_tempo, 
        estados=nova_lista_estados
        )

    registro_eventos.append(novo_evento)

    sorteio_eventos.remove(objeto_sorteio)

    # se fila é menor ou igual a 1, não agenda uma saida.
    if novo_evento.fila <= numero_servidores:


        next_random_number, count= next_random(count, prev, a, c, M)
        evento_saida = SorteioEvento(tipo_evento=TipoEvento.SAIDA, tempo_inicial=registro_eventos[-1].tempo , random_number=next_random_number)
        sorteio_eventos.append(evento_saida)
        print("next_random_number 1 : " + str(next_random_number))
        prev = next_random_number
        if count <= 0:
            return -1, count, prev, eventos_perdidos
    
    return 0, count, prev, eventos_perdidos




def registra_saida(objeto_sorteio: SorteioEvento, prev, count, numero_servidores):
    
    # Remove da list de sorteio
    sorteio_eventos.remove(objeto_sorteio)

    ultimo_evento = registro_eventos[-1]

    tempo_evento_saida = objeto_sorteio.tempo
    tempo_ultimo_evento = ultimo_evento.tempo

    #Copia o objeto de lista
    nova_lista_estados = ultimo_evento.estados.copy()


    nova_lista_estados[ultimo_evento.fila] = (tempo_evento_saida - tempo_ultimo_evento) + ultimo_evento.estados[ultimo_evento.fila]

    novo_tamanho_fila = ultimo_evento.fila - 1

    novo_evento_saida = RegistroEventos(
        tipo_evento=TipoEvento.SAIDA, 
        fila=novo_tamanho_fila, 
        tempo=tempo_evento_saida, 
        estados=nova_lista_estados
        )
    
    registro_eventos.append(novo_evento_saida)

    if novo_evento_saida.fila >= numero_servidores:
        # Agenda uma saida
        
        next_random_number, count= next_random(count, prev, a, c, M)
        novo_sorteio_saida = SorteioEvento(tipo_evento=TipoEvento.SAIDA, tempo_inicial=registro_eventos[-1].tempo , random_number=next_random_number)
        sorteio_eventos.append(novo_sorteio_saida)
        print("next_random_number 2: " + str(next_random_number))
        prev = next_random_number



        if count <= 0:
            return -1, count, prev
    return 0 , count, prev


######### Adicionando primeiro evento vazio
registro_eventos.append(RegistroEventos(
    tipo_evento=TipoEvento.VAZIO, 
    fila=0, 
    tempo=0, 
    estados=[0,0,0,0,0,0,0]
    )
)

###### Primeiro Sorteio
primeiro_sorteio = SorteioEvento(tipo_evento=TipoEvento.CHEGADA, tempo_inicial=2 , random_number=None)
sorteio_eventos.append(primeiro_sorteio)


#### Loop de execução
while count > 0:

    proximo_sorteio = get_proximo_sorteio()

    if proximo_sorteio.tipo_evento == TipoEvento.CHEGADA:
        
        result, count, prev, eventos_perdidos = registra_chegada(proximo_sorteio, prev, count, eventos_perdidos, numero_servidores) # sorteia e talvez ja agenda uma saida.
        # print("updated 1: " + str(prev))

        if result == -1:
                break
    if proximo_sorteio.tipo_evento == TipoEvento.SAIDA:
        result, count, prev = registra_saida(proximo_sorteio, prev, count, numero_servidores)
        print("updated 2: " + str(prev))
        if result == -1:
                break
    #agenda uma chegada
    next_random_number, count= next_random(count, prev, a, c, M)
    novo_objeto_sorteio_chegada = SorteioEvento(tipo_evento=TipoEvento.CHEGADA, tempo_inicial=registro_eventos[-1].tempo , random_number=next_random_number)
    sorteio_eventos.append(novo_objeto_sorteio_chegada)
    # print("next_random_number 3: " + str(next_random_number))
    prev = next_random_number
    # print("updated 3 : " + str(prev))
    if count <= 0:
        break


print()
print("Tempos de execução: ")
ultimo_estado = registro_eventos[-1]
print("Fila com 0: " + str(ultimo_estado.estados[0]) + " - Probabilidade: " + str(ultimo_estado.estados[0]*100/ ultimo_estado.tempo))
print("Fila com 1: " + str(ultimo_estado.estados[1]) + " - Probabilidade: " + str(ultimo_estado.estados[1]*100/ ultimo_estado.tempo))
print("Fila com 2: " + str(ultimo_estado.estados[2]) + " - Probabilidade: " + str(ultimo_estado.estados[2]*100/ ultimo_estado.tempo))
print("Fila com 3: " + str(ultimo_estado.estados[3]) + " - Probabilidade: " + str(ultimo_estado.estados[3]*100/ ultimo_estado.tempo))
print("Fila com 4: " + str(ultimo_estado.estados[4]) + " - Probabilidade: " + str(ultimo_estado.estados[4]*100/ ultimo_estado.tempo))
print("Fila com 5: " + str(ultimo_estado.estados[5]) + " - Probabilidade: " + str(ultimo_estado.estados[5]*100/ ultimo_estado.tempo))
print("Tempo total de execução: " + str(ultimo_estado.tempo) + " - Porcentagem: " + str(ultimo_estado.tempo*100/ ultimo_estado.tempo))
print()
print("Eventos perdidos: " + str(eventos_perdidos))

print()
print()





    







