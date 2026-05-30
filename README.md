AstroRun

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Kennedy Pereira Mendes
- Maria Eduarda Barreto da Silva

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

O jogo consiste em uma nave espacial que se desloca em um cenário horizontal. Durante a partida, meteoritos surgem continuamente do lado direito da tela e se movem em direção ao lado esquerdo, criando obstáculos que o jogador deve evitar. A nave pode ser controlada pelo jogador para realizar os desvios necessários, tornando a jogabilidade dinâmica e progressivamente desafiadora.


## Objetivo do jogador

O objetivo do jogador é permanecer em jogo pelo maior tempo possível sem colidir com os meteoritos. A pontuação é calculada com base no tempo de sobrevivência, de modo que quanto mais tempo a nave permanecer intacta, maior será a pontuação obtida. Quando ocorre uma colisão, a partida é encerrada e a pontuação final é comparada ao recorde armazenado. Caso a nova pontuação seja superior à anterior, ela passa a ser registrada como o novo recorde, incentivando o jogador a superar sua própria marca em partidas futuras.

## Regras do jogo

* O jogador controla uma nave espacial utilizando o teclado.
* A nave pode se mover apenas para cima e para baixo.
* Meteoros aparecem no lado direito da tela e se movem em direção ao lado esquerdo.
* O objetivo do jogo é sobreviver o maior tempo possível desviando dos meteoros.
* Quanto maior o tempo de sobrevivência, maior será a pontuação.
* O jogo registra automaticamente o maior recorde alcançado pelo jogador.
* Conforme o tempo passa, a velocidade e a quantidade de meteoros aumentam.
* O jogo termina quando a nave colide com um meteoro.

## Controles

* Seta para cima: mover a nave para cima
* Seta para baixo: mover a nave para baixo
* ENTER: iniciar ou reiniciar o jogo
* ESC: sair do jogo

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
