from enum import Enum


class TipoEvento(Enum):
    CHEGADA = 'chegada'
    SAIDA = 'saida'
    PASSAGEM = 'passagem'
    VAZIO = 'vazio'