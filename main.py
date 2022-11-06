import json
from random import randrange
from typing import List
from itertools import groupby

from jogador import Jogador
from tipo_jogador import TipoJogador


class BancoImobiliario:

    def __init__(self,
                 partida: int = 0,
                 lista_jogadores: List[Jogador] = None,
                 max_rodadas: int = 1000,
                 lista_propriedades: List[json] = None):
        self._partida = partida
        self._rodada = 0
        self._lista_jogadores = lista_jogadores
        self._max_rodadas = max_rodadas
        self.propriedades = lista_propriedades
        self.time_out = False

    @staticmethod
    def rolar_dado() -> int:
        return randrange(1, 7)

    def iniciar(self) -> None:
        while self._rodada < self._max_rodadas and self.validar_se_tem_jogadores():
            self._rodada += 1
            self.executar_rodada()
        if self._rodada > self._max_rodadas:
            self.time_out = True

    def resultado(self) -> json:
        jogadores_com_saldo = [x for x in self._lista_jogadores if x.saldo > 0]
        if len(jogadores_com_saldo) == 1:
            jogador = jogadores_com_saldo[0]
        else:
            jogadores_ordem = sorted(jogadores_com_saldo, key=lambda x: x.ordem)
            jogador = jogadores_ordem[0]
        return {
            'rodadas_realizadas': self._rodada,
            'jogador_ganhador': jogador.nome,
            'tipo_jogador': jogador.tipo_jogador.name
        }

    def executar_rodada(self) -> None:
        for jogador in self._lista_jogadores:
            if not self.validar_se_tem_jogadores():
                break
            if jogador.saldo < 0:
                continue
            posicao = self.rolar_dado()
            jogador.posicao_tabuleiro = posicao
            propriedade = self.propriedades[f"{posicao}"]
            if not propriedade['proprietario']:
                self.comprar_propriedade(jogador, propriedade)
            else:
                proprietario = [x for x in self._lista_jogadores if x.nome == propriedade['proprietario']][0]
                if proprietario.saldo < 0:
                    self.comprar_propriedade(jogador, propriedade)
                else:
                    self.pagar_aluguel(jogador, propriedade)

    def validar_se_tem_jogadores(self) -> bool:
        jogadores_com_saldo = [x for x in self._lista_jogadores if x.saldo > 0]
        if len(jogadores_com_saldo) > 1:
            return True
        else:
            return False

    @staticmethod
    def pagar_aluguel(jogador: Jogador, propriedade: json) -> None:
        jogador.pagar_valor(propriedade['custo_aluguel'])

    @staticmethod
    def comprar_propriedade(jogador: Jogador, propriedade: json) -> None:
        if jogador.avaliar_compra(propriedade):
            propriedade['proprietario'] = jogador.nome
            jogador.pagar_valor(propriedade['custo_venda'])


def resultado_tipo_vencedor(list_resultados: list) -> None:
    sort_data = sorted(list_resultados, key=lambda content: content['tipo_jogador'])
    groups = groupby(sort_data, lambda content: content['tipo_jogador'])
    tipo_jogador = None
    total_jogadores = 0
    for key, value in groups:
        total = len(list(value))
        if total > total_jogadores:
            tipo_jogador = key
            total_jogadores = total
    print(f'o tipo de jogador que mais vence é o {tipo_jogador} com {total_jogadores} vitorias')


def partidas_com_max_partidas_realizadas(list_resultados: list, max_partidas: int) -> None:
    total_partidas = [x for x in list_resultados if x['rodadas_realizadas'] == max_partidas]
    print(f'total de partidas com 1000 rodadas realizados {len(total_partidas)}')


def porcentagem_vitorias_tipo_jogador(list_resultados: list) -> None:
    sort_data = sorted(list_resultados, key=lambda content: content['tipo_jogador'])
    groups = groupby(sort_data, lambda content: content['tipo_jogador'])
    for key, value in groups:
        total = len(list(value))
        porcentagem = (total / len(list_resultados)) * 100
        print(f'o tipo {key} tem uma porcetagem de vitorias {round(porcentagem, 2)} %')


def calcular_media_de_partidas(list_resultados: list, total_partidas_realizadas: int) -> None:
    total_partidas = 0
    for resultado in list_resultados:
        total_partidas += resultado['rodadas_realizadas']
    media = total_partidas / total_partidas_realizadas
    print(f'media de partidas é de {round(media, 0)}')


if __name__ == "__main__":
    total_partidas = 300
    max_rodadas = 1000
    with open('propriedades.json') as f:
        propriedades = json.load(f)
        list_resultados = list()
        for x in range(total_partidas):
            lista_jogadores = list()
            lista_jogadores.append(
                Jogador(nome='jogador1', ordem=1, tipo_jogador=TipoJogador.IMPULSIVO, max_posicoes=len(propriedades)))
            lista_jogadores.append(
                Jogador(nome='jogador2', ordem=2, tipo_jogador=TipoJogador.EXIGENTE, max_posicoes=len(propriedades)))
            lista_jogadores.append(
                Jogador(nome='jogador3', ordem=3, tipo_jogador=TipoJogador.CAUTELOSO, max_posicoes=len(propriedades)))
            lista_jogadores.append(
                Jogador(nome='jogador4', ordem=4, tipo_jogador=TipoJogador.ALEATORIO, max_posicoes=len(propriedades)))
            banco = BancoImobiliario(
                partida=x,
                lista_jogadores=lista_jogadores, max_rodadas=max_rodadas, lista_propriedades=propriedades)
            banco.iniciar()
            resultado = banco.resultado()
            list_resultados.append(resultado)
        resultado_tipo_vencedor(list_resultados)
        partidas_com_max_partidas_realizadas(list_resultados, max_rodadas)
        porcentagem_vitorias_tipo_jogador(list_resultados)
        calcular_media_de_partidas(list_resultados, total_partidas)
