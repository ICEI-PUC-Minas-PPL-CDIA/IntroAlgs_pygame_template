# Banco de dados das perguntas

perguntas = [
    {
        "pergunta": "O que armazena uma Matriz de tamanho 3x3?",
        "opcoes": ["3 elementos", "6 elementos", "9 elementos", "0 elementos"],
        "correta": 2
    },
    {
        "pergunta": "O que acontece se tentarmos ler a posição 5 de um vetor de tamanho 3?",
        "opcoes": ["Ele aumenta de tamanho sozinho", "Dá erro de índice fora do limite", "O programa adivinha o valor", "Ele apaga o vetor"],
        "correta": 1
    },
    {
        "pergunta": "Qual comando usamos para repetir um bloco de código enquanto uma condição for verdadeira?",
        "opcoes": ["if", "while", "else", "print"],
        "correta": 1
    },
    {
        "pergunta": "Para que serve o comando 'if' no Python?",
        "opcoes": ["Para repetir o código", "Para criar uma lista", "Para fazer uma pergunta/teste condicional", "Para fechar o jogo"],
        "correta": 2
    },
    {
        "pergunta": "Se o comando 'if' não for atendido, qual comando opcional roda logo em seguida?",
        "opcoes": ["else", "while", "for", "import"],
        "correta": 0
    },
    {
        "pergunta": "Qual das opções abaixo é usada para criar uma lista vazia?",
        "opcoes": ["lista = 0", "lista = []", "lista = 'vazia'", "lista = True"],
        "correta": 1
    },
    {
        "pergunta": "O que acontece se você criar um loop 'while True' sem nenhum comando para pará-lo?",
        "opcoes": ["O computador desliga", "O loop roda apenas uma vez", "Gera um loop infinito e trava o programa", "O Python corrige sozinho"],
        "correta": 2
    },
    {
        "pergunta": "Qual estrutura é ideal para percorrer todos os elementos de uma lista um por um?",
        "opcoes": ["import", "if", "else", "for"],
        "correta": 3
    },
    {
        "pergunta": "O que o comando 'print()' faz no Python?",
        "opcoes": ["Exibe uma mensagem na tela/terminal", "Soma dois números", "Salva o jogo", "Deleta um arquivo"],
        "correta": 0
    },
    {
        "pergunta": "Qual o valor da variável 'x' após rodar: x = 5 + 3?",
        "opcoes": ["5", "3", "53", "8"],
        "correta": 3
    }

]

# Banco de dados de falas de Antares

FALAS_INICIO_FASE = {
    1: "Bom, lá vamos nós. Eu já vi esse tipo de perigo antes — relaxa, eu te guio.",
    2: "Você foi bem na primeira! Essa aqui aperta um pouco mais... mas focamos nela agora, o resto eu conto depois.",
    3: "Penúltima fase. Eu devia te contar uma coisa sobre o que vem a seguir... mas não agora. Foca comigo, tá?",
    4: "Chegou a hora. Eu não te contei antes porque tinha medo que você desistisse — aquilo lá na frente já me consumiu uma vez. Mas dessa vez, eu não vou deixar você enfrentar sozinho.",
}

FALAS_DANO_CRITICO = {
    1: "Ai! Isso doeu até pra mim... vai, acha um item de reparo por aí.",
    2: "Ui, essa eu senti. Tem um reparo rondando por aqui, vê se acha.",
    3: "Isso dói cada vez mais... por favor, acha logo um reparo.",
    4: "Eu sinto cada golpe que você leva agora. Acha o reparo — eu não aguento te ver assim, não dessa vez.",
}

FALAS_DANO = {
    1: "Sua vida tá baixa! Cuidado, ainda temos um caminho longo pela frente.",
    2: "Isso tá ficando perigoso de verdade. Não desiste agora, tá quase lá.",
    3: "Sua luz tá fraquinha... e a minha também. A gente precisa segurar firme.",
    4: "Não! Não agora, não bem na frente dele. Aguenta, por favor — eu já perdi gente pra essa coisa antes.",
}

FALAS_ITEM_REPARO = {
    1: "Relaxa e pensa com calma — a resposta certa raramente é a mais complicada.",
    2: "Se travar, pensa em como você resolveria isso numa situação real, sem enrolação.",
    3: "Confia no que você já aprendeu até aqui. Você sabe mais do que imagina.",
    4: "Essa pode ser a última vez que eu te ajudo assim... então pensa com tudo que você tem. Eu acredito em você.",
}

FALAS_DEATH_STAR = [
    "É ela. Eu reconheceria esse brilho frio em qualquer lugar do universo.",
    "Lá está. Não desvia o olhar, mas também não subestima o que você tá vendo.",
    "Sente esse silêncio? É assim que ela anuncia que chegou.",
    "Essa luz que você vê não é luz de verdade. É vazio se fingindo de estrela.",
] 