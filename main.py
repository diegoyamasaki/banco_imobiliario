import json
from random import randrange
from typing import List

from jogador import Jogador
from tipo_jogador import TipoJogador


class BancoImobiliario:

    def __init__(self, lista_jogadores: List[Jogador], max_rodadas: int =1000, lista_propriedades: list = None):
        self._rodada = 0
        self._lista_jogadores = lista_jogadores
        self._max_rodadas = max_rodadas
        self.propriedades = lista_propriedades

    @staticmethod
    def rolar_dado():
        return randrange(1, 7)

    def iniciar(self):
        while self._rodada < self._max_rodadas and self.validar_se_tem_jogadores():
            self._rodada += 1
            self.executar_rodada()
            # print(f"fim da rodada {self._rodada}")

        print(f'fim do jogo n.rodadas={self._rodada}')

    def resultado(self):
        print('resultado do jogo')
        jogadores_com_saldo = [x for x in self._lista_jogadores if x.saldo > 0]
        print(f'numero de jogadores com saldo {len(jogadores_com_saldo)}')
        if len(jogadores_com_saldo) == 1:
            jogador = jogadores_com_saldo[0]
        else:
            jogadores_ordem = sorted(jogadores_com_saldo, key=lambda x: x.ordem)
            jogador = jogadores_ordem[0]
        print(f'jogador vencedor é o {jogador.nome} com saldo de {jogador.saldo}')

    def executar_rodada(self):
        for jogador in self._lista_jogadores:
            if not self.validar_se_tem_jogadores():
                print('acabou o jogo !')
                break
            if jogador.saldo < 0:
                print('jogador fora da partida')
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

    def validar_se_tem_jogadores(self):
        jogadores_com_saldo = [x for x in self._lista_jogadores if x.saldo > 0]
        if len(jogadores_com_saldo) > 1:
            return True
        else:
            return False

    @staticmethod
    def pagar_aluguel(jogador, propriedade):
        jogador.pagar_valor(propriedade['custo_aluguel'])

    @staticmethod
    def comprar_propriedade(jogador, propriedade):
        if jogador.avaliar_compra(propriedade):
            propriedade['proprietario'] = jogador.nome
            jogador.pagar_valor(propriedade['custo_venda'])


if __name__ == "__main__":
    lista_jogadores = list()

    with open('propriedades.json') as f:
        propriedades = json.load(f)
        lista_jogadores.append(
            Jogador(nome='jogador1', ordem=1, tipo_jogador=TipoJogador.IMPULSIVO, max_posicoes=len(propriedades)))
        lista_jogadores.append(
            Jogador(nome='jogador2', ordem=2, tipo_jogador=TipoJogador.EXIGENTE, max_posicoes=len(propriedades)))
        lista_jogadores.append(
            Jogador(nome='jogador3', ordem=3, tipo_jogador=TipoJogador.CAUTELOSO, max_posicoes=len(propriedades)))
        lista_jogadores.append(
            Jogador(nome='jogador4', ordem=4, tipo_jogador=TipoJogador.ALEATORIO, max_posicoes=len(propriedades)))
        banco = BancoImobiliario(lista_jogadores=lista_jogadores, max_rodadas=1000, lista_propriedades=propriedades)
        banco.iniciar()
        banco.resultado()


