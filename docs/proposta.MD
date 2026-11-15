# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com **Python e Pygame** dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

# 1. Nome provisório do jogo
Nome: Guerra das Máquinas

# 2. Integrantes do grupo

Nome 1: Luanna Rodrigues Campos

Nome 2: Manuela Terto Boaventura

Nome 3: Kennedy Pereira Mendes Lima

Nome 4: Davi Alves Franco Gomes

# 3. Tema escolhido
Tema: Mundo Pós-Apocalíptico e Rebelião das Máquinas (Inteligência Artificial hostil).

Como esse tema se relaciona com o jogo? O tema define diretamente os obstáculos e a progressão da partida: o jogador enfrenta ondas de robôs autônomos coordenados por uma IA central que tomou o planeta. Para avançar pelo território devastado e sobreviver, é preciso gerenciar disparos e eliminar os sentinelas mecânicos que bloqueiam o caminho até o núcleo de controle.

#4. Tipo de jogo
Tipo escolhido: Jogo de tiro e progressão lateral (Run and Gun / Side-Scroller Shooter 2D).

#5. Descrição geral do jogo
Descrição: Na tela, aparece um cenário urbano em ruínas visto de lado, com deslocamento horizontal da esquerda para a direita. O jogador controla um sobrevivente armado que precisa caminhar para frente enquanto robôs controlados pela IA surgem pelo caminho tentando interceptá-lo. O desafio consiste em desviar das investidas ou disparos inimigos e atirar nos robôs para abrir passagem e acumular pontos.

#6. Objetivo do jogador
Objetivo: Avançar pelo percurso pós-apocalíptico destruindo os robôs inimigos até alcançar o final da fase (ou atingir a pontuação necessária) sem perder todas as vidas.

#7. Regras principais
Regra 1: O jogador inicia a partida com 3 vidas (pontos de integridade).

Regra 2: Cada robô destruído pelos disparos do jogador soma 100 pontos ao placar.

Regra 3: Colidir diretamente com um robô ou ser atingido por um ataque inimigo retira 1 vida do jogador.

Regra 4: O jogador pode se mover para frente e para trás dentro dos limites da tela e disparar projéteis em linha reta.

Regra 5: Robôs possuem resistência definida (ex.: 1 a 2 tiros para serem destruídos) e desaparecem da tela ao serem derrotados.

#8. Condição de vitória
Condição de vitória: O jogador vence a partida ao percorrer toda a extensão do mapa (avançando até o ponto final da fase) e eliminar os robôs que bloqueiam o caminho, mantendo pelo menos 1 vida restante.

#9. Condição de derrota ou encerramento
Condição de derrota ou encerramento: A partida termina em derrota (Game Over) imediatamente quando o contador de vidas do jogador chegar a zero.

#10. Elementos previstos no jogo
Personagem ou elemento principal: Sobrevivente humano equipado com uma arma de energia/projéteis.

Obstáculos ou desafios: Robôs patrulheiros controlados pela IA que avançam em direção ao jogador (e barreiras/destroços no cenário, se aplicável).

Itens ou objetos de interação (se houver): Kits de reparo/vida ou recarga de munição deixados ocasionalmente ao destruir robôs.

Pontuação, vidas, tempo ou progresso: Contador de vidas no canto superior esquerdo, placar de pontos no canto superior direito e barra ou indicador de distância percorrida.

#11. Controles previstos
Controles: Teclas A / D ou Setas Esquerda / Direita para andar para trás e para frente; Barra de Espaço (ou clique esquerdo do mouse) para atirar; tecla W ou Seta para Cima caso seja implementado pulo simples para desviar.

#12. Principais dificuldades esperadas
Dificuldade 1: Programar as colisões entre os tiros, os robôs e o personagem.

Dificuldade 2: Controlar o tempo de surgimento dos robôs e o aumento gradual da dificuldade na partida.

Dificuldade 3: Organizar e juntar o código do grupo usando o GitHub.

#13. Escopo mínimo para a entrega final
Escopo mínimo: Uma tela jogável funcional contendo o personagem que anda para frente/trás e atira, um tipo básico de robô inimigo surgindo pela direita, detecção de colisão (tiro destrói robô; robô tira vida do jogador), contagem funcional de vidas e pontos, além de telas simples de Vitória e Game Over.

#14. Possíveis melhorias, caso haja tempo
Melhoria 1: Adicionar efeitos sonoros de tiros, explosões de robôs e trilha sonora de fundo pós-apocalíptica.

Melhoria 2: Incluir um segundo tipo de robô mais resistente (ou um chefe robótico da IA no final do percurso).

Melhoria 3: Criar um menu inicial com instruções de controles e um sistema de ranking de maior pontuação (High Score).

