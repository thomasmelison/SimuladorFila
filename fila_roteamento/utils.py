


from Fila import Fila
from RandomGenerator import RandomGenerator
from TabelaSorteio import TabelaSorteio
from TipoEvento import TipoEvento


def agenda_saida_ou_passagem(random_generator: RandomGenerator , tabela_sorteio: TabelaSorteio ,fila_origem: Fila ):
    random_number = random_generator.generate_next_random()

    # Verifica qual será o destino da Saida ou da passagem que está sendo sorteada
    fila_destino_saida = None
    for fila_info in fila_origem.sub_filas:
        
        if fila_info.get("Lower_bound_prob") <= random_number and random_number < fila_info.get("Upper_bound_prob"): 
            fila_destino_saida = fila_info.get("ObjetoFila")

    # Se o numero aleatorio nao caiu no intervalo de um dos objetos sorteio, sorteia uma saida.
    if fila_destino_saida == None:
        tabela_sorteio.sorteia_evento(
            tipo_evento=TipoEvento.SAIDA,
            fila=fila_origem,
            fila_destino=fila_destino_saida
        )
    # Se o numeor aleatorio caiu no intervalo de uma das subfilas, agenda uma passagem para essa fila.
    else:
        tabela_sorteio.sorteia_evento(
            tipo_evento=TipoEvento.PASSAGEM,
            fila=fila_origem,
            fila_destino=fila_destino_saida
        )
    fila_origem.decrementa_servidores_disponiveis()

def normaliza_tempo_total_execucao(lista_filas: list[Fila]):
    tempo_total_execucao = 0 
    for fila in lista_filas:
        ultimo_evento_fila = fila.lista_eventos[-1]
        if ultimo_evento_fila.tempo > tempo_total_execucao:
            tempo_total_execucao = ultimo_evento_fila.tempo

    for fila in lista_filas:
        ultimo_evento_fila = fila.lista_eventos[-1]
        print(f"Fila: { fila.identificador_fila}")
        print(f"Tamanho ultimo_evento_fila.estados: { len(ultimo_evento_fila.estados) }")
        print(f" ultimo_evento_fila.fila : { ultimo_evento_fila.fila}")
        tempo_nao_contabilizado = tempo_total_execucao - ultimo_evento_fila.tempo
        ultimo_evento_fila.estados[ ultimo_evento_fila.fila ] = tempo_nao_contabilizado + ultimo_evento_fila.estados[ ultimo_evento_fila.fila ]
        ultimo_evento_fila.tempo = tempo_total_execucao
    
    print(f"Tempo global de execução: { tempo_total_execucao }")