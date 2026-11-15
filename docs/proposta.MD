# Proposta Inicial do Jogo

## 1. Nome provisório do jogo

**Nome:**

> **DeepCheck** — *"Na dúvida, verifica."*

## 2. Integrantes do grupo

- Nome 1: Patrick
- Nome 2: (preencher)
- Nome 3: (preencher)
- Nome 4: (preencher)

## 3. Tema escolhido

**Tema:**

> Confiabilidade de sistemas inteligentes e conteúdos reais e artificiais: reconhecer informações falsas, manipuladas ou geradas por IA, proteger dados pessoais e conferir respostas de assistentes virtuais antes de confiar nelas.

**Como esse tema se relaciona com o jogo?**

> O dilema do jogo é o próprio uso responsável da IA. Cada conteúdo que chega traz pistas (fonte, data, pedido de dados pessoais, resposta sem referência), e o jogador decide entre aprovar, bloquear ou gastar uma ficha para verificar. Decidir errado reduz a credibilidade; conferir tudo custa tempo e fichas. A análise crítica muda diretamente a pontuação, a credibilidade e o resultado da partida.

## 4. Tipo de jogo

**Tipo escolhido:**

> Decisão e classificação em tempo real, com itens descendo pela tela (mistura de perguntas e respostas com desvio e coleta de itens).

## 5. Descrição geral do jogo

**Descrição:**

> O jogador é um agente da Central de Verificação. Um feed de conteúdos (notícias, posts, mensagens pedindo dados e respostas de assistentes de IA) desce pela tela em 3 faixas. O jogador move o agente entre as faixas e, quando um item chega à zona de decisão, escolhe **aprovar**, **bloquear** ou **verificar**. Verificar gasta uma ficha e revela uma pista escondida do item, mas o feed continua descendo. Os itens ficam mais rápidos e as pistas mais sutis ao longo da partida.

## 6. Objetivo do jogador

**Objetivo:**

> Classificar corretamente os conteúdos, mantendo a credibilidade acima de zero e fazendo a maior pontuação possível até completar todas as rodadas.

## 7. Regras principais

- Regra 1: O jogador começa com 100% de credibilidade e 3 fichas de verificação.
- Regra 2: Aprovar um conteúdo confiável ou bloquear um falso/abusivo gera pontos; errar a decisão reduz a credibilidade.
- Regra 3: Verificar gasta 1 ficha e revela a pista escondida do item; sem fichas, não é possível verificar.
- Regra 4: Acertos seguidos formam um combo que aumenta os pontos, e acertar sem verificar dá bônus.
- Regra 5: Itens que chegam ao fim da faixa sem decisão contam como erro. As fichas são recarregadas aos poucos.

## 8. Condição de vitória

**Condição de vitória:**

> Completar todas as rodadas de conteúdos com a credibilidade acima de 0%. A pontuação final é comparada com o recorde salvo.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

> A credibilidade chega a 0%. Nesse caso a partida termina e o recorde é atualizado se a pontuação for maior que o anterior.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** agente da Central de Verificação, que se move entre 3 faixas.
- **Obstáculos ou desafios:** conteúdos descendo pela tela (confiáveis, falsos, gerados por IA ou abusivos), cada um com pistas legíveis.
- **Itens ou objetos de interação (se houver):** fichas de verificação e a pista escondida de cada conteúdo.
- **Pontuação, vidas, tempo ou progresso:** barra de credibilidade (funciona como as vidas), pontuação, combo, fichas restantes e rodada atual.

## 11. Controles previstos

**Controles:**

> - Setas esquerda/direita: mudar de faixa
> - A: aprovar o conteúdo
> - B: bloquear o conteúdo
> - Espaço: verificar (gasta uma ficha)
> - ESC: sair do jogo

## 12. Principais dificuldades esperadas

- Dificuldade 1: Escrever conteúdos e pistas realistas e balanceados, para que o jogo seja justo e ensine algo.
- Dificuldade 2: Controlar a velocidade dos itens, o tempo e a recarga das fichas para equilibrar a dificuldade.
- Dificuldade 3: Manter a lógica em funções separadas do desenho para facilitar os testes, e organizar o trabalho do grupo no GitHub.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> Janela com o jogo, agente que se move entre 3 faixas, itens descendo carregados de um arquivo JSON (cerca de 20 a 30 conteúdos), decisões de aprovar, bloquear e verificar funcionando, credibilidade, pontuação, tela de vitória e de derrota e recorde salvo em arquivo. A lógica (avaliar decisão, calcular pontos, atualizar combo e credibilidade) fica em funções testadas com pytest.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Três fases temáticas (Fake News, Privacidade e Respostas de IA) com dificuldade crescente.
- Melhoria 2: Ranking com os 5 melhores resultados salvo em `data/ranking.txt`.
- Melhoria 3: Sons, animações simples e menu inicial.

## Declaração de originalidade

Declaramos que a ideia, as regras e o código deste projeto são de autoria do grupo. O template da disciplina foi usado como base e todo recurso externo (imagens, sons, fontes ou código) será identificado no `README.md`, com origem e licença quando possível.
