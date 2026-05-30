# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> AstroRun

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: Kennedy Pereira Mendes
- Nome 2: Maria Eduarda Barreto da Silva

## 3. Tipo de jogo

Indique o tipo de jogo que será desenvolvido.

Tipo escolhido pelo grupo:

> Nave desviando de meteoros.

## 4. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará.

Procure responder:

- O que aparece na tela?
- O que o jogador controla?
- O que o jogador precisa fazer?
- Quais desafios aparecem durante a partida?

Descrição:

> O jogo consiste em uma nave espacial que se desloca em um cenário horizontal. Durante a partida, meteoritos surgem continuamente do lado direito da tela e se movem em direção ao lado esquerdo, criando obstáculos que o jogador deve evitar. A nave pode ser controlada pelo jogador para realizar os desvios necessários, tornando a jogabilidade dinâmica e progressivamente desafiadora.
## 5. Objetivo do jogador

Explique qual é o objetivo principal do jogador.


Objetivo:

> O objetivo do jogador é permanecer em jogo pelo maior tempo possível sem colidir com os meteoritos. A pontuação é calculada com base no tempo de sobrevivência, de modo que quanto mais tempo a nave permanecer intacta, maior será a pontuação obtida. Quando ocorre uma colisão, a partida é encerrada e a pontuação final é comparada ao recorde armazenado. Caso a nova pontuação seja superior à anterior, ela passa a ser registrada como o novo recorde, incentivando o jogador a superar sua própria marca em partidas futuras.

## 6. Regras principais

Liste as principais regras do jogo.

Regras do grupo:

- Regra 1: O jogador controla uma nave espacial utilizando teclado
- Regra 2: A nave pode se mover apenas para cima ou para baixo
- Regra 3: Meteoros aparecem do lado direito e se movem para o lado esquerdo
- Regra 4: Quanto maior o tempo de sobrevivência, maior a pontuação
- Regra 5: O jogo registra automaticamente o maior recorde alcançado pelo jogador
- Regra 6: O jogo termina quando a nave colide com um meteoro

## 7. Condição de vitória

Explique como o jogador vence ou conclui o jogo.

Condição de vitória:

> Toda vez que o jogador alcançar o próprio recorde.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> A nave colidir com algum meteoro.

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Descrição:

> Uma nave controlada pelas setas do teclado.

## Obstáculos, inimigos ou desafios

Descrição:

> Meteoros saindo do lado direito da tela e indo em diração ao esquerdo.

## Itens, alvos ou objetos de interação

Descrição:

> Tempo de sobrevivência que será convertido em pontuação.

## Pontuação, vidas, tempo ou progresso

Descrição:

> A cada segundo que o jogador se mantém vivo, ele ganhará 1 ponto no somatório da pontuação na partida.

## 10. Controles previstos

Informe os comandos que serão utilizados pelo jogador.

Exemplo:

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- Espaço: realizar ação
- ESC: sair do jogo

Controles do grupo:

- Seta para cima: mover a nave para cima
- Seta para baixo: mover a nave para baixo
- Enter: iniciar ou reiniciar o jogo
- ESC: sair do jogo

## 11. Organização inicial do código

Explique como o grupo pretende organizar o código.

Organização planejada:

> - main.py: inicia o jogo e executa o loop principal;
- src/player.py: contém a classe e as funções relacionadas à nave do jogador;
- src/meteor.py: contém a criação e movimentação dos meteoros;
- src/game.py: controla as regras do jogo, pontuação e colisões;
- src/config.py: armazena configurações como tamanho da tela, cores e velocidades;
- src/record.py: realiza a leitura e gravação do recorde em arquivo;
- assets/: contém imagens, sons e demais recursos utilizados..


## 12. Recursos externos previstos

Informe se o grupo pretende utilizar imagens, sons, fontes, tutoriais ou códigos externos.

Recursos previstos:

> - imagens gratuitas para a nave e os meteoros;
- fonte gratuita para exibição da pontuação e do recorde;
- tutoriais de Pygame utilizados apenas como referência para implementação;
- possíveis efeitos sonoros gratuitos para colisões e menu..

## 13. Principais dificuldades esperadas

Liste as dificuldades que o grupo acredita que poderá enfrentar.

Dificuldades previstas:

- Dificuldade 1: implementação de detecção de colisão entre a nave e os meteoros;
- Dificuldade 2: armazenamento e atualização do recorde do jogador;

## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

Esta seção é importante para evitar que o grupo escolha uma ideia grande demais.

Escopo mínimo:

> A versão mínima do jogo terá uma nave controlada pelo teclado, movimentação vertical, meteoros atravessando a tela, sistema de pontuação baseado no tempo de sobrevivência, registro do maior recorde e tela de fim de jogo quando ocorrer uma colisão.

## 15. Possíveis melhorias, caso haja tempo

Liste funcionalidades extras que o grupo poderá implementar se conseguir concluir o escopo mínimo.



Melhorias possíveis:

- Melhoria 1: Tela inicial e menu de reinício
- Melhoria 2: Efeitos sonoros e música de fundo
- Melhoria 3: Diferentes tipos de meteoros com velocidade variadas
- Malhoria 4: aumento progressivo da dificuldade
