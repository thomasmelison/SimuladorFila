


from Fila import Fila, FilaInfo
from RandomGenerator import RandomGenerator
from TipoEvento import TipoEvento


class ObjetoSorteio:

        def __init__(self, 
                     tipo_evento: TipoEvento,
                     tempo: float,
                     fila: Fila,
                     fila_destino: Fila | None = None
                     ):
            self.tipo_evento = tipo_evento
            self.tempo = tempo
            self.fila = fila
            self.fila_destino = fila_destino


             

class TabelaSorteio:


    def __init__(self, 
                 lista_sorteio_eventos: ObjetoSorteio, 
                 random_generator: RandomGenerator 
                 ):
        self.lista_sorteio_eventos : list[ObjetoSorteio] = lista_sorteio_eventos
        self.random_generator: RandomGenerator = random_generator


    
    def get_proximo_sorteio(self) -> ObjetoSorteio | None:

        if not self.lista_sorteio_eventos or len(self.lista_sorteio_eventos) == 0:
            return None
        last_sorteio = min(self.lista_sorteio_eventos, key=lambda evento: evento.tempo)

        self.lista_sorteio_eventos.remove(last_sorteio)

        return last_sorteio
    
    def encontrar_fila_info(self, lista: list[FilaInfo], fila_procurada: Fila) -> FilaInfo:
        if fila_procurada == None:
            return True
        for fila_info in lista:
            if fila_info['ObjetoFila'] == fila_procurada:
                return True
        return False
    
    def adiciona_evento(self, 
                        tipo_evento: TipoEvento,
                        tempo: float,
                        fila: Fila,
                        fila_destino: Fila = None
                        ):
        novo_sorteio = ObjetoSorteio(
             tipo_evento=tipo_evento,
             tempo=tempo,
             fila=fila, 
             fila_destino=fila_destino
        )

        if not self.encontrar_fila_info( lista=fila.sub_filas, fila_procurada=fila_destino):
            if fila_destino == None: 
                raise Exception("Erro inesperado ocorreu ao procurar uma fila. Valor enviado é nulo")
            raise ValueError(f"Objeto de fila_destino (fila {fila_destino.identificador_fila} ) não é uma subfila da fila {fila.identificador_fila}.")
        
        self.lista_sorteio_eventos.append(novo_sorteio)
    
    def sorteia_evento(self, 
                        tipo_evento: TipoEvento , 
                        fila: Fila, 
                        fila_destino: Fila = None
                       ):
        
        random_number = self.random_generator.generate_next_random()
        
        if tipo_evento == TipoEvento.CHEGADA:
            sorteio = fila.range_chegada[0] + ( ( fila.range_chegada[1] - fila.range_chegada[0] ) * random_number)

        elif tipo_evento == TipoEvento.PASSAGEM or tipo_evento == TipoEvento.SAIDA:
            sorteio = fila.range_atendimento[0] + ( ( fila.range_atendimento[1] - fila.range_atendimento[0] ) * random_number)
        
        else:
            raise Exception("Tipo de evento desconhecido!")
           
        
        self.adiciona_evento(
            tipo_evento=tipo_evento,
            tempo= fila.get_tempo_ultimo_evento() + sorteio,
            fila= fila,
            fila_destino= fila_destino
         ) 
         
         