import json
import os

CAMINHO_RANKING = "data/ranking.json"
CAMINHO_RANKING_COOP = "data/ranking_coop.json"


def carregar_ranking():
    """Carrega o ranking do JSON; retorna dict vazio se não existir."""
    if not os.path.exists(CAMINHO_RANKING):
        return {}
    with open(CAMINHO_RANKING, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def salvar_ranking(ranking):
    """Salva o dict de ranking no JSON."""
    with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)


def obter_recorde_jogador(nome):
    """Retorna o maior score do jogador; 0 se não existir."""
    return carregar_ranking().get(nome, 0)


def atualizar_ranking(nome, pontuacao):
    """Atualiza o score do jogador se a nova pontuação for maior."""
    ranking = carregar_ranking()
    if pontuacao > ranking.get(nome, 0):
        ranking[nome] = pontuacao
        salvar_ranking(ranking)


def top10():
    """Retorna lista dos 10 melhores [(nome, pontuacao)] em ordem decrescente."""
    ranking = carregar_ranking()
    ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    return ordenado[:10]


def melhor_pontuacao_global():
    """Retorna a maior pontuação entre todos os jogadores."""
    ranking = carregar_ranking()
    if not ranking:
        return 0
    return max(ranking.values())


def carregar_ranking_coop():
    """Carrega o ranking coop do JSON; retorna dict vazio se não existir."""
    if not os.path.exists(CAMINHO_RANKING_COOP):
        return {}
    with open(CAMINHO_RANKING_COOP, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def atualizar_ranking_coop(nome_dupla, pontuacao):
    """Atualiza o score da dupla se a nova pontuação for maior."""
    ranking = carregar_ranking_coop()
    if pontuacao > ranking.get(nome_dupla, 0):
        ranking[nome_dupla] = pontuacao
        with open(CAMINHO_RANKING_COOP, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)


def top10_coop():
    """Retorna lista dos 10 melhores do ranking coop [(dupla, pontuacao)]."""
    ranking = carregar_ranking_coop()
    ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    return ordenado[:10]
