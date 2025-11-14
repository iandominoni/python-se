from config import SCORE_RANGES, MESSAGES


def get_risk_level(score):
    """Retorna o nível de risco baseado na pontuação."""
    for range_config in SCORE_RANGES:
        if range_config["min"] <= score <= range_config["max"]:
            return range_config["level"]
    return "Crítico"


def get_color_by_level(level):
    """Retorna a cor correspondente ao nível de risco."""
    for range_config in SCORE_RANGES:
        if range_config["level"] == level:
            return range_config["color"]
    return "#3498DB"


def get_message_by_level(level):
    """Retorna a mensagem correspondente ao nível de risco."""
    return MESSAGES.get(level, "")


def format_response_path(responses):
    """Formata o caminho de respostas para exibição."""
    if not responses:
        return "Nenhuma resposta registrada"

    current_eixo = None
    formatted = []

    for resp in responses:
        if resp["eixo_nome"] != current_eixo:
            current_eixo = resp["eixo_nome"]
            formatted.append(f"\n{current_eixo}:")

        response_symbol = "✓ SIM" if resp["resposta"] == "sim" else "✗ NÃO"
        formatted.append(
            f"  Q{resp['question_id']:02d}: {response_symbol} (+{resp['pontos']} pts)"
        )

    return "\n".join(formatted)


def get_response_summary(responses):
    """Gera um sumário das respostas por eixo."""
    summary = {}

    for resp in responses:
        eixo = resp["eixo_nome"]
        if eixo not in summary:
            summary[eixo] = {"sim": 0, "nao": 0, "pontos": 0}

        summary[eixo][resp["resposta"]] += 1
        summary[eixo]["pontos"] += resp["pontos"]

    return summary
