# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

> Tá Sabendo?

## 2. Integrantes do grupo

- Nome 1: Raiany Morais Ribeiro
- Nome 2: Moises de Souza do Carmo

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de perguntas e respostas (Quiz)

## 4. Descrição geral do jogo

O jogo será um quiz de perguntas e respostas sobre conhecimentos gerais, História e Geografia.

Cada jogador começará a partida com 3 vidas. Para cada pergunta, o jogador terá 15 segundos para escolher uma alternativa. Caso o tempo acabe antes da resposta, o jogador perderá 1 vida. A cada novo intervalo de 15 segundos sem responder, perderá outra vida consecutivamente.

Se o jogador errar a questão, também perderá 1 vida, o que influenciará diretamente no resultado final da partida.

Ao acertar uma pergunta, o jogador ganhará pontos. Esses pontos poderão ser usados para comprar dicas ou recuperar vidas durante o jogo. Caso o jogador perca todas as suas vidas, também perderá todos os pontos acumulados durante a partida.

As perguntas terão níveis de dificuldade diferentes, com pontuações específicas:
- Perguntas fáceis: 1 ponto
- Perguntas médias: 2 pontos
- Perguntas difíceis: 3 pontos

Os pontos poderão ser acumulados ao longo do jogo até o momento em que o jogador decidir apertar “sair” e encerrar a partida.

## 5. Objetivo do jogador

Objetivo:

> Testar seus conhecimentos respondendo corretamente ao maior número possível de perguntas antes de perder todas as vidas.

## 6. Regras principais

Regras do grupo:

- Cada pergunta possui quatro alternativas de resposta.
- O jogador terá um tempo limitado (15 segundos) para responder cada pergunta.
- Caso o jogador acerte, ganhará pontos baseados na dificuldade da questão.
- Caso o jogador erre ou o tempo acabe, perderá uma vida (e vidas continuam caindo a cada ciclo de 15s sem resposta).
- Se o jogador perder todas as vidas, perderá também todos os pontos acumulados na partida.
- O jogo continuará com perguntas consecutivas até que o jogador aperte “sair” ou perca todas as vidas.

## 7. Condição de vitória

Condição de vitória:

> O jogador vence ao decidir encerrar a partida voluntariamente clicando em “sair” sem ter perdido todas as suas vidas, conseguindo assim salvar e manter os pontos acumulados.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> O jogador é derrotado caso perca todas as suas 3 vidas (seja por errar perguntas ou por estouro do cronômetro). Como consequência, a partida é encerrada e todos os pontos acumulados são zerados.

## 9. Elementos previstos no jogo

## Jogador ou elemento principal

Descrição:

> Interface do jogador que exibe o progresso atual, quantidade de vidas restantes, pontuação acumulada e o painel de compra de vantagens (dicas/vidas).

## Obstáculos, inimigos ou desafios

Descrição:

> O tempo limite de 15 segundos por pergunta e o nível crescente de dificuldade das questões (fáceis, médias e difíceis) que testam o conhecimento e agilidade do usuário.

## Itens, alvos ou objetos de interação

Descrição:

> Sistema de perguntas com 4 alternativas clicáveis, além dos botões interativos para "Comprar Dica", "Recuperar Vida" e o botão "Sair".

## Pontuação, vidas, tempo ou progresso

Descrição:

> O jogador inicia com 3 vidas e 0 pontos. Cada acerto concede de 1 a 3 pontos. Há um temporizador regressivo de 15 segundos por questão exibido na tela.

## 10. Controles previstos

Controles do grupo:

- Clique do Mouse: Selecionar alternativas de resposta
- Clique do Mouse: Confirmar respostas e interagir com menus
- Clique do Mouse: Comprar dicas ou recuperar vidas usando os pontos acumulados
- Clique do Mouse / Teclado: Iniciar o jogo ou acionar o botão de Sair

## 11. Organização inicial do código

Organização planejada:

- `main.py`: Inicia o jogo, gerencia as telas (Menu, Jogo, Fim de Jogo) e controla o loop principal do Pygame.
- `src/config.py`: Armazena constantes como cores, fontes, dimensões da janela e caminhos dos arquivos.
- `src/perguntas.py`: Gerencia a estrutura de dados (listas e dicionários) contendo os enunciados, alternativas, respostas corretas e dificuldades.
- `src/mecanicas.py`: Controla as funções de pontuação, lógica do temporizador, sistema de vidas e validação de respostas.
- `src/arquivos.py`: Cuida da leitura e escrita do arquivo de salvamento do histórico de pontos acumulados.

## 12. Recursos externos previstos

Recursos previstos:

- Imagens e ícones de interface obtidos de bancos gratuitos (para botões, ícones de vidas/coração e fundo).
- Fontes tipográficas personalizadas (TTF) para melhorar a legibilidade e estética das perguntas na tela.
- Arquivo de texto ou JSON externo contendo o banco de dados de perguntas organizadas por dificuldade.

## 13. Principais dificuldades esperadas

Dificuldades previstas:

- Dificuldade 1: Implementação e sincronização precisa do temporizador (cronômetro) no loop do Pygame.
- Dificuldade 2: Criação da lógica de troca de pontos por benefícios (comprar dicas/vidas) dinamicamente durante a partida.
- Dificuldade 3: Manipulação, leitura e escrita correta de arquivos externos para salvar os pontos acumulados.
- Dificuldade 4: Renderização e organização de blocos de texto longos (perguntas e alternativas) na interface gráfica do Pygame.

## 14. Escopo mínimo para a entrega final

Escopo mínimo:

> Um jogo de quiz com sistema funcional de perguntas de múltipla escolha, controle de tempo (cronômetro regressivo), gerenciamento de vidas e pontuação na tela, telas básicas de vitória/derrota, opção visível de sair e o salvamento persistente dos pontos acumulados em arquivo.

## 15. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

- Melhoria 1: Adição de efeitos sonoros (som de acerto, erro, tempo acabando e música de fundo).
- Melhoria 2: Criação de uma tela de ranking/Leaderboard exibindo as maiores pontuações já salvas.
- Melhoria 3: Implementação de animações visuais na tela (como piscar verde ao acertar ou vermelho ao errar).
