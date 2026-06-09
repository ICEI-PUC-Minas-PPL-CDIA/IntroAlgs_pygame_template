# SpaceNinja

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

O jogo consiste em controlar uma nave espacial que deve sobreviver o maior tempo possível desviando de meteoros que surgem aleatoriamente na tela.

## Integrantes do Grupo

* Henrique Santos de Souza
* Guilherme Henrique
* Bruno Coutinho

## Estrutura do Projeto

```text
Meteor-Escape/
├── main.py
├── requirements.txt
├── README.md
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── data/
│   └── ranking.json
├── docs/
│   ├── proposta.md
│   └── relatorio.md
├── src/
│   ├── game.py
│   ├── player.py
│   ├── meteor.py
│   └── config.py
└── tests/
```

## Descrição do Jogo

O jogador controla uma nave espacial em um cenário espacial. Meteoros surgem aleatoriamente na parte superior da tela e se movem em direção à parte inferior.

O objetivo é sobreviver o maior tempo possível desviando dos meteoros. Conforme a partida avança, a dificuldade aumenta devido ao surgimento mais frequente de obstáculos.

## Objetivo do Jogador

Sobreviver o maior tempo possível e obter a maior pontuação possível evitando colisões com os meteoros.

## Regras do Jogo

* O jogador controla uma nave espacial.
* A nave pode se mover livremente dentro dos limites da tela.
* Meteoros surgem continuamente em posições aleatórias.
* Cada colisão com um meteoro remove uma vida.
* O jogador inicia a partida com 3 vidas.
* A pontuação aumenta conforme o tempo de sobrevivência.
* O jogo termina quando todas as vidas forem perdidas.

## Controles

* ↑ : mover para cima
* ↓ : mover para baixo
* ← : mover para a esquerda
* → : mover para a direita
* ESC : sair do jogo

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```
Caso tenha um erro ao instalar as dependências, 
verifique se o python está instalado,
se sim execute esse comando no terminal

```bash
pip install pygame-ce pytest
```

### 3. Executar o jogo

```bash
python main.py
```

## Como Executar os Testes

```bash
python -m pytest
```

## Checklist Mínimo para Entrega

* [x] Nave controlada pelo teclado.
* [x] Movimentação em quatro direções.
* [x] Sistema de geração de meteoros.
* [x] Sistema de colisão.
* [x] Sistema de vidas.
* [x] Sistema de pontuação.
* [x] Tela de fim de jogo.
* [x] Execução através de `python main.py`.
* [x] Testes funcionando com `pytest`.
* [x] explicação na tela inicial
* [x] leveis a cada aumento na dificuldade

## Possíveis Melhorias

* [x] Tela inicial.
* [x] Sistema de ranking.
* [] Power-ups de escudo.
* [] Power-ups de velocidade.
* [] Diferentes tipos de meteoros.
* [] Sons e efeitos visuais.
* [] Fazer os nossos proprios sprites
* [] meteoros de todas as direções
* [] trajetorias diferentes(curvilineas e em diagonal)
* [] Diferentes dificuldades(facil, médio, dificil, impossivel)
* [x] Menu de pausa.
* [x] Aumento progressivo da dificuldade.

## Observações

* Manter o código organizado em módulos pequenos e com responsabilidades bem definidas.
* Utilizar GitHub para controle de versão.
* Documentar alterações importantes durante o desenvolvimento.
* Priorizar a conclusão do escopo mínimo antes de implementar funcionalidades extras.
