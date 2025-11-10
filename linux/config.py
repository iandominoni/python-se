"""
Módulo de configuração de cores e constantes.
"""

# Cores modernas
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#3498DB"
SUCCESS_COLOR = "#27AE60"
WARNING_COLOR = "#F39C12"
DANGER_COLOR = "#E74C3C"
LIGHT_BG = "#ECF0F1"
WHITE = "#FFFFFF"

# Ranges de pontuação
SCORE_RANGES = [
    {"min": 0, "max": 32, "level": "Baixo", "color": SUCCESS_COLOR},
    {"min": 33, "max": 42, "level": "Médio", "color": WARNING_COLOR},
    {"min": 43, "max": 52, "level": "Alto", "color": DANGER_COLOR},
    {"min": 53, "max": 999, "level": "Crítico", "color": "#8B0000"},
]

MESSAGES = {
    "Baixo": "Sem indícios clínicos significativos.",
    "Médio": "Relação emocional desajustada com alimentação/imagem.",
    "Alto": "Padrões disfuncionais em desenvolvimento.",
    "Crítico": "Possível transtorno alimentar ativo.",
}
