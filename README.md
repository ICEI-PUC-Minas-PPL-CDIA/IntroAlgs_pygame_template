# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

## 1. Nome provisório do jogo

> Antares

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1:Beatriz Carvalho
- Nome 2:Iale Leles
- Nome 3:Igor Carvalho
- Nome 4:Isadora Alvarenga

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

- nave desviando de meteoros;
- corrida simples com obstáculos;
- jogo de clique rápido;

## 4. Descrição geral do jogo

Descrição:

> Antares é um jogo de combate espacial inspirado em Space Invaders e ambientado no universo Star Wars, desenvolvido em Python com a biblioteca Pygame. O jogador assume o controle de uma nave de combate em meio a uma resistência contra uma frota inimiga, enfrentando ondas de inimigos, desviando de obstáculos, sobrevivendo a Quick Time Events em momentos críticos e enfrentando combates contra chefes. Entre as fases, o jogador precisa reparar sistemas danificados da nave por meio de um minijogo de circuitos lógicos, no qual deve combinar portas AND, OR e NOT para restabelecer a energia dos componentes, integrando uma camada educacional de lógica booleana ao gameplay.

## 5. Objetivo do jogador

Objetivo:

Pilotar a nave através de fases progressivamente mais difíceis, eliminando inimigos, sobrevivendo aos obstáculos do espaço e mantendo a nave operacional ao reparar seus sistemas com base em raciocínio lógico, até derrotar a frota inimiga e seu comandante na batalha final.

## 6. Regras principais

Liste as principais regras do jogo.

Regras do grupo:

- Regra 1: O jogador começa com 100% de vida.
- Regra 2: Cada colisão é progressiva, onde os asteróides pequenos tiram 5% de vida, os médios 10% e os grandes 15% de vida.
- Regra 3: Cada tiro reduz uma porcentagem da vida conforme o seu tipo. 
- Regra 4: Se o jogador cair no buraco negro ele morre instantâneamente.
- Regra 5: A fase termina após o jogador exterminar todas as naves presentes naquelas determinada fase.
- Regra 6: Quando a nave do jogador ficar com a vida baixa o jogador terá a opção de resgatar no espaço uma ferramente de reparo para a nave, aumentando a vida em 20%, não tendo o direito de reparar no fim da fase. 
- Regra 7: Se o jogador não conseguir reparar a nave, em qualquer situação, após 3 chances, ele perderá 3% de vida.
- Regra 8: Se o jogador inutilizar a nave, ele volta para o início da fase atual.
- Regra 9: Se o jogador cair no buraco negro, ele volta para a fase inicial.
- Regra 10: O jogo acaba após o jogador eliminar o boss: A estrela da morte.

## 7. Condição de vitória

Condição de vitória:

> O jogador passa de fase se matar todas as naves presentes naquelas determinada fase.
> O jogador vence o jogo após eliminar a estrela da morte, na última fase.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> Quando a barra de vida da nave se esgotar.
> Cair no buraco negro.

## 9. Elementos previstos no jogo

Descrição:

> Jogador, controlado pelas setas do teclado.
> Naves inimigas.
> Antares(bot de suporte), aparece em situações de vulnerabilidade.
> Buraco negro, reseta o jogo.
> Estrela da morte, boss final, inimigo mais difícil, tem munições fatais.
> Asteróides, obstáculos simples.

## Obstáculos, inimigos ou desafios

Descrição:

> buraco negro, reseta o jogo e atraí o jogador quando passa da zona segura.
> Estrela da morte, boss final, inimigo mais difícil, tem munições fatais e aprace apenas na última fase.
> Asteróides, obstáculos simples, aparecem em momentos e posições aleatórias no espaço, seguem sempre uma direção única.

## Itens, alvos ou objetos de interação

Descrição:

> Naves inimigas, são alvos.
> Ferramentas de reparo aparecem no espaço quando a vida útil da nave se encontra em 35% ou menos. 

## Pontuação, vidas, tempo ou progresso

Descrição:

> O jogador começa com a nave em 100%, e só tem a oportunidade de conserta-la com ferramentas de reparo coletadas e utilizadas com exito ou no fim de cada fase, onde não foram feito o uso dessas ferramentas. 

## 10. Controles previstos

Controles do grupo:

- Tecla/comando: Seta para cima: mover para cima
- Tecla/comando: Seta para baixo: mover para baixo
- Tecla/comando: Seta para esquerda: mover para esquerda
- Tecla/comando: Seta para direita: mover para direita
- Tecla/comando: W: mover para cima
- Tecla/comando: S: mover para baixo
- Tecla/comando: A: mover para esquerda
- Tecla/comando: D: mover para direita
- Tecla/comando: Espaço: Atirar
- Tecla/comando: ESC: Menu de opções
- Tecla/comando: Mouse: Realizar o reparo da nave

## 11. Organização inicial do código

Organização planejada:

> `main.py`: inicia o jogo;
> `src/jogo.py`: contém o loop principal;
> `src/config.py`: guarda configurações como tamanho da tela e cores;
> `src/funcoes.py`: contém funções auxiliares;
> `src/dados.py`: contém funções de leitura e escrita de arquivos.

## 12. Recursos externos previstos

Recursos previstos:

> Imagens obtidas de meios gratuitos;
> Sons gratuitos;
> Documentação pygame;

## 13. Principais dificuldades esperadas

Dificuldades previstas:

- Dificuldade 1: Obtenção das mídias;
- Dificuldade 2: Controle de tempo;
- Dificuldade 3: Projetar mecânicas específicas, como a do buraco negro;
- Dificuldade 4: Testes;

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> A versão mínima do jogo terá um personagem controlado pelo teclado, obstáculos aparecendo na tela, amostra de vida útil da nave, tela de fim de jogo.

## 15. Possíveis melhorias, caso haja tempo

- tela inicial;
- sons;
- fases;
- aumento de dificuldade;
- ranking;
- animações;
- novos tipos de obstáculos;
- menu de pausa;
- fases;
- buraco negro;
- boss na fase final;

Melhorias possíveis:

- Melhoria 1: Novas naves;
- Melhoria 2: Salvar o progresso;
- Melhoria 3: Mais opções no menu de pausa.
