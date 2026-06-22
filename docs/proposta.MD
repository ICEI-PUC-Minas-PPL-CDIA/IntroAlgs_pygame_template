# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> “Cobralia: Snake Ascension” ou “Scaleborn Tales of Ophidia”.

## 2. Integrantes do grupo

- Nome 1: Daniel Aguiar Pacheco
- Nome 2: Gustavo Henrique de Lima
- Nome 3: Victor Gabriel Ananias
- Nome 4: Julia Carvalho

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Arcade / Ação 2D (Uma reimaginação moderna do clássico "Snake Game").

## 4. Descrição geral do jogo

Descrição:

> O jogo é uma reimaginação moderna do "Snake Game" baseada em progressão por história e fases. O jogador controla uma cobra que se movimenta para coletar maçãs e avançar de níveis. A partida introduz obstáculos como paredes móveis, uma mecânica nova de "dash" (arrancada), um sistema dinâmico de itens temporários (power-ups e power-downs) e inimigos com inteligência artificial. O grande desafio culmina em uma batalha contra um Chefão final que o jogador deverá derrotar.

## 5. Objetivo do jogador

Objetivo:

> Controlar a cobra para coletar uma quantidade gradativa de maçãs em cada nível para desbloquear o avanço às próximas fases, até conseguir chegar ao confronto final e derrotar o Chefão.

## 6. Regras principais


Regras do grupo:

- A cobra deve obrigatoriamente comer maçãs para crescer e progredir pelas fases.
- O uso da habilidade de "Dash" (arrancada rápida) exige recursos, consumindo parte da pontuação ou um pedaço da cauda da cobra.
- Coletar itens especiais aplica efeitos temporários, podendo gerar aumento/redução de velocidade, inversão de controles, corte na cauda ou um modo fantasma.
- O jogador deve evitar sofrer colisões com o próprio corpo (exceto durante o modo fantasma), com as paredes do cenário e com os inimigos predadores.

## 7. Condição de vitória

Condição de vitória:

> O jogador vence ao alcançar a última fase e derrotar o Chefão da IA Intermediária, o que exige atingir os seus pontos fracos 3 vezes exatas.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> A partida termina se a barra de vida (caso implementada) chegar a zero ou se a cobra colidir de forma letal, como bater em paredes fixas ou móveis, no próprio corpo, ou ser pega pelo inimigo Predador.

## 9. Elementos previstos no jogo

>Personagem: Cobra (design a definir).
>Coletáveis: Maçãs (objetivo), Pimenta, Gelo, Cogumelo Venenoso, Tesoura e item de Fantasma.
>Inimigos: Predador (IA simples de perseguição) e Chefão Final (IA intermediária com padrões de ataque e pontos fracos).
>Cenário: Paredes fixas e paredes móveis.
>Interface (UI): Contador de maçãs, indicador de fase atual, temporizador de efeitos dos power-ups.

### Jogador ou elemento principal

Descrição:

> Uma Cobra, que cresce dinamicamente e que (na versão avançada do projeto) possuirá movimentação livre em 360 graus utilizando matemática vetorial.

### Obstáculos, inimigos ou desafios

Descrição:

> O cenário contará com paredes fixas e paredes móveis que exigem timing para serem ultrapassadas. Os inimigos incluem um Predador com IA para perseguição inteligente desviando de obstáculos, e um Chefão Final.

### Itens, alvos ou objetos de interação

Descrição:

> O coletável principal e alvo do jogo são as Maçãs. Também estarão disponíveis itens especiais: Pimenta (Aumento de velocidade), Gelo (Redução de velocidade), Cogumelo Venenoso (Inversão de controles), Tesoura (Corta a cauda) e Fantasma (Permite atravessar obstáculos).

### Pontuação, vidas, tempo ou progresso

Descrição:

> A interface terá um contador de maçãs para gerenciar o progresso das metas gradativas de cada fase, um indicador da fase atual e um temporizador para os efeitos dos power-ups. Também há previsão de um medidor de pontuação/cauda consumido pelo uso de dash e vida do chefe.

## 10. Controles previstos

Controles do grupo:

- Setas do Teclado ou W, A, S, D: Movimentação direcional da cobra.
- Barra de Espaço: Ativar a habilidade de Dash (arrancada rápida).

## 11. Organização inicial do código

Organização planejada:

> O código usará `main.py` como ponto de entrada e `config.py` para constantes globais, com as dependências no `requirements.txt`. O jogo será dividido nos seguintes diretórios: `assets/` para recursos visuais e sonoros; `core/` para gerenciar o loop principal, o estado de jogo e os níveis; `entities/` para os códigos interativos do jogador, itens, obstáculos e sistema do Chefão; `systems/` para lógicas independentes (colisão, pathfinding e matemática); e `ui/` para gerenciar a interface HUD e os menus do jogo.

## 12. Recursos externos previstos


Recursos previstos:

> O grupo utilizará arquivos de imagem (.png) para a criação dos sprites (cabeça/corpo da cobra, itens, inimigos e paredes). Também serão utilizados arquivos para efeitos sonoros e fontes de texto para compor a interface de usuário, bem como arquivos de texto ou `.json` para carregar a configuração estrutural das diferentes fases do jogo. A biblioteca de terceiros `pygame` será usada como dependência.

## 13. Principais dificuldades esperadas


Dificuldades previstas:

- Dificuldade 1: Desenvolver toda a lógica e os padrões de ataque matemáticos da Inteligência Artificial do Chefão Final.
- Dificuldade 2: Gerenciar o tempo e o conflito da sobreposição de múltiplos efeitos temporários simultâneos (power-ups e power-downs) durante o loop principal do jogo.
- Dificuldade 3: Criar layouts de níveis que sejam equilibrados (desafiadores e justos) incorporando a mecânica de paredes móveis.

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> A entrega final mínima requer a cobra com movimentação funcional e sistema de crescimento ao comer maçãs, com um sistema básico de colisão contra as paredes e o próprio corpo. O jogo deverá possuir paredes móveis, transição funcional de pelo menos 3 fases possuindo metas gradativas de maçãs, e a implementação de no mínimo 2 power-ups (por exemplo: Pimenta e Tesoura).

## 15. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

- Melhoria 1: Implementação da Movimentação Livre (Estilo Slither.io) em 360 graus utilizando matemática vetorial, abolindo a movimentação apenas por grades rígidas.
- Melhoria 2: Implementação do Predador Avançado, uma inteligência artificial baseada no Algoritmo A* para desviar de obstáculos ativamente.
- Melhoria 3: Criação da Fase Final com o Chefão de IA Intermediária atirando projéteis geométricos na mecânica de "Bullet Hell".
- Melhoria 4: Implementação de todos os itens extras não englobados no escopo mínimo, como o Gelo, o Cogumelo Venenoso e o modo Fantasma.