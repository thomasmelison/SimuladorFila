from __future__ import annotations
from typing import Dict, TypedDict
from TipoEvento import TipoEvento
from math import inf


class Evento:

    def __init__(
            self, 
            tipo_evento: TipoEvento, 
            fila : int, 
            tempo : float, 
            estados : list[float]
            ):
        
        self.tipo_evento =   tipo_evento 
        self.fila = fila
        self.tempo = tempo
        self.estados = estados


class FilaInfo(TypedDict):
    ObjetoFila: Fila
    Lower_bound_prob: float
    Upper_bound_prob: float

class Fila:
    def __init__(self, 
                 identificador_fila: str,
                 lista_eventos: list[Evento], 
                 tamanho_fila: int, 
                 numero_servidores: int,
                range_chegada: tuple,
                range_atendimento: tuple,
                 ):
        self.identificador_fila = identificador_fila
        self.lista_eventos= lista_eventos
        self.tamanho_fila = tamanho_fila
        self.eventos_perdidos = 0
        self.numero_servidores = numero_servidores
        self.range_chegada = range_chegada
        self.range_atendimento = range_atendimento
        self.sub_filas: list[FilaInfo] = []
        self.servidores_disponiveis = numero_servidores


    
    def adiciona_subfilas(
            self, 
            sub_filas : list[FilaInfo]
        ):

        self.sub_filas = sorted(sub_filas, key=lambda x: x['Lower_bound_prob'])

        for index in range( len(  self.sub_filas ) ):
            upper_bound = self.sub_filas[index].get("Upper_bound_prob")

            if upper_bound > 1.0: 
                raise Exception(f"A subfila {index} tem como upper bound um valor maior que 1.0. Valor real: { upper_bound }")
            if index != 0 and self.sub_filas[index - 1].get("Upper_bound_prob") > self.sub_filas[index].get("Lower_bound_prob"):
                raise Exception(f"A subfila {index} tem como lower bound um valor menor ({self.sub_filas[index].get("Lower_bound_prob")}) que o upper bound da fila {index - 1 }, que é {self.sub_filas[index - 1].get("Upper_bound_prob") } ")

    def decrementa_servidores_disponiveis(self):
        self.servidores_disponiveis = self.servidores_disponiveis - 1

        if self.servidores_disponiveis < 0:
            raise Exception("Servidores disponíveis atingiu um numero negativo... ")
        
    def tem_eventos_em_espera(self) -> bool:
        servidores_ocupados = self.numero_servidores - self.servidores_disponiveis
        return self.lista_eventos[-1].fila > servidores_ocupados

    def get_tempo_ultimo_evento(self) -> float:
        return self.lista_eventos[-1].tempo
    
    def check_fila_cheia(self) -> bool:
        if len(self.lista_eventos) == 0:
            return False
        return self.lista_eventos[-1].fila >= self.tamanho_fila 

    def fila_tem_servidores_disponiveis(self) -> bool:

        if len(self.lista_eventos) == 0:
            return True
        return self.servidores_disponiveis > 0
    
    def handle_fila_infinita(self, novo_tamanho_fila: int):
        if self.tamanho_fila == inf:
            # print(f"Fila {self.identificador_fila} é infinita, iniciando tratamento")
            if novo_tamanho_fila >= len(self.lista_eventos[-1].estados):
                for evento in self.lista_eventos:
      
                    while novo_tamanho_fila >= len(evento.estados):
                        evento.estados.append(0) 
        else:
            return
  
    def registra_chegada(self, tempo_sorteio: float):
        ultimo_evento = self.lista_eventos[-1]

        self.handle_fila_infinita(ultimo_evento.fila + 1)

        nova_lista_estados = ultimo_evento.estados.copy()

        tempo_ultimo_evento = ultimo_evento.tempo
        tempo_novo_evento = tempo_sorteio

        nova_lista_estados[ultimo_evento.fila] = (tempo_novo_evento - tempo_ultimo_evento) + nova_lista_estados[ultimo_evento.fila]

        # Trata da perda de um evento pois a fila esta cheia.
        if ultimo_evento.fila >= self.tamanho_fila:
            novo_tamanho_fila = ultimo_evento.fila
            self.eventos_perdidos = self.eventos_perdidos + 1
        # Caso nao esteja cheio pode continuar
        else:
            novo_tamanho_fila = ultimo_evento.fila + 1

        novo_tempo = tempo_sorteio


        novo_evento = Evento(
            tipo_evento=TipoEvento.CHEGADA, 
            fila=novo_tamanho_fila, 
            tempo=novo_tempo, 
            estados=nova_lista_estados,
            )
        self.lista_eventos.clear()
        self.lista_eventos.append(novo_evento)
        return novo_evento




    def registra_saida(self, tempo_sorteio: float, is_passagem: bool):
    
        ultimo_evento = self.lista_eventos[-1]

        self.handle_fila_infinita(ultimo_evento.fila)

        tempo_evento_saida = tempo_sorteio
        tempo_ultimo_evento = ultimo_evento.tempo
   
        nova_lista_estados = ultimo_evento.estados.copy()

        nova_lista_estados[ultimo_evento.fila] = (tempo_evento_saida - tempo_ultimo_evento) + ultimo_evento.estados[ultimo_evento.fila]

        novo_tamanho_fila = ultimo_evento.fila - 1

        if is_passagem:
            tipo_evento = TipoEvento.PASSAGEM
        else:
            tipo_evento = TipoEvento.SAIDA

        self.servidores_disponiveis = self.servidores_disponiveis + 1
        if self.servidores_disponiveis > self.numero_servidores:
            raise Exception("Numero de servidores disponiveis maior do que o numero de servidores real.")


        novo_evento_saida = Evento(
            tipo_evento=tipo_evento, 
            fila=novo_tamanho_fila, 
            tempo=tempo_evento_saida, 
            estados=nova_lista_estados
            )
        self.lista_eventos.clear()
        self.lista_eventos.append(novo_evento_saida)
        return novo_evento_saida


    def printa_fila(self, ):
        print()
        print()
        print("=====================================================================================")
        print(f"Tempos de execução da fila {self.identificador_fila}:")
        ultimo_estado_fila = self.lista_eventos[-1]

        for index in range(len( ultimo_estado_fila.estados ) ):
            print(f"Fila {self.identificador_fila} com {index}: { str( ultimo_estado_fila.estados[index] ) } - Probabilidade: { str( ultimo_estado_fila.estados[index] * 100 / ultimo_estado_fila.tempo) } " )
        
        print("Tempo total de execução: " + str(ultimo_estado_fila.tempo) + " - Porcentagem: " + str( ultimo_estado_fila.tempo* 100 / ultimo_estado_fila.tempo) )

        print("Eventos perdidos: " + str(self.eventos_perdidos))
        print("=====================================================================================")




