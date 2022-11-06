import json
from random import randrange
from tipo_jogador import TipoJogador


class Jogador:
    def __init__(self, nome: str, ordem: int, tipo_jogador: TipoJogador, saldo: int = 300, max_posicoes: int = 20):
        self._saldo = saldo
        self.nome = nome
        self.tipo_jogador = tipo_jogador
        self._posicao_tabuleiro = 0
        self._max_posicoes = max_posicoes
        self.ordem = ordem

    @property
    def saldo(self) -> int:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: int):
        self._saldo += valor

    def pagar_valor(self, valor: int):
        self._saldo -= valor

    @property
    def posicao_tabuleiro(self) -> int:
        return self._posicao_tabuleiro

    @posicao_tabuleiro.setter
    def posicao_tabuleiro(self, posicao: int) -> None:
        if (self._posicao_tabuleiro + posicao) > self._max_posicoes:
            temp_posicao = self._posicao_tabuleiro + posicao
            temp_posicao -= self._max_posicoes
            self._saldo = 100
            self._posicao_tabuleiro = temp_posicao
        else:
            self._posicao_tabuleiro += posicao

    def avaliar_compra(self, propriedade: json) -> bool:
        match self.tipo_jogador:
            case TipoJogador.EXIGENTE:
                if propriedade['custo_aluguel'] > 50:
                    return True
                return False
            case TipoJogador.ALEATORIO:
                numero = randrange(1, 2)
                if numero == 1:
                    return True
                elif numero == 2:
                    return False
            case TipoJogador.CAUTELOSO:
                if (self.saldo - propriedade['custo_venda']) >= 80:
                    return True
                return False
            case TipoJogador.IMPULSIVO:
                return True
        return True

