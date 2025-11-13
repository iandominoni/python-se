"""
Módulo de configuração de cores e constantes - DESIGN PROFISSIONAL MODERNO.
"""

# Paleta de cores profissional - Tema moderno e sofisticado
PRIMARY_COLOR = "#1E293B"  # Slate 800 - Azul escuro elegante
SECONDARY_COLOR = "#334155"  # Slate 700 - Azul acinzentado
ACCENT_COLOR = "#475569"  # Slate 600 - Accent suave
SUCCESS_COLOR = "#10B981"  # Verde esmeralda moderno
WARNING_COLOR = "#F59E0B"  # Âmbar profissional
DANGER_COLOR = "#EF4444"  # Vermelho coral
LIGHT_BG = "#F1F5F9"  # Slate 100 - Cinza muito claro
WHITE = "#FFFFFF"
DARK_TEXT = "#0F172A"  # Slate 900
PURPLE = "#8B5CF6"  # Roxo moderno
PINK = "#EC4899"  # Rosa contemporâneo
ORANGE = "#F97316"  # Laranja vibrante
GREEN = "#059669"  # Verde profissional
BLUE = "#3B82F6"  # Azul elétrico
TEAL = "#14B8A6"  # Teal moderno
INDIGO = "#6366F1"  # Indigo profissional

# Cores para níveis de risco - Design profissional
LEVEL_COLORS = {
    "Baixo": "#10B981",  # Verde - Seguro
    "Médio": "#F59E0B",  # Âmbar - Atenção
    "Alto": "#F97316",  # Laranja - Alerta
    "Crítico": "#EF4444",  # Vermelho - Crítico
}

# Ícones profissionais (Unicode)
LEVEL_ICONS = {
    "Baixo": "●",  # Círculo preenchido
    "Médio": "▲",  # Triângulo
    "Alto": "■",  # Quadrado
    "Crítico": "♦",  # Losango
}


# Ranges de pontuação
SCORE_RANGES = [
    {"min": 0, "max": 32, "level": "Baixo", "color": LEVEL_COLORS["Baixo"]},
    {"min": 33, "max": 42, "level": "Médio", "color": LEVEL_COLORS["Médio"]},
    {"min": 43, "max": 52, "level": "Alto", "color": LEVEL_COLORS["Alto"]},
    {"min": 53, "max": 999, "level": "Crítico", "color": LEVEL_COLORS["Crítico"]},
]

MESSAGES = {
    "Baixo": "Resultado positivo. Sem indícios clínicos significativos detectados.",
    "Médio": "Atenção necessária. Relação emocional desajustada com alimentação e imagem corporal.",
    "Alto": "Alerta importante. Padrões disfuncionais em desenvolvimento requerem atenção profissional.",
    "Crítico": "Intervenção urgente recomendada. Possível transtorno alimentar ativo detectado.",
}

# Mensagens motivacionais profissionais
MOTIVATIONAL_MESSAGES = [
    "Você está fazendo progresso",
    "Continue com atenção",
    "Cada resposta é importante",
    "Quase finalizando",
    "Excelente foco",
]

# Cores dos eixos temáticos - Professional palette
EIXO_COLORS = {
    "Comportamento Alimentar": "#8B5CF6",  # Roxo
    "Imagem Corporal": "#EC4899",  # Rosa
    "Emoção e Autocontrole": "#F97316",  # Laranja
    "Controle de Peso": "#10B981",  # Verde
    "Percepção e Cognição": "#3B82F6",  # Azul
}

# Tamanhos de fonte para projeção
FONT_SIZES = {
    "title": 28,  # Títulos principais
    "subtitle": 18,  # Subtítulos
    "header": 22,  # Headers de seção
    "body": 16,  # Texto principal
    "label": 14,  # Labels e descrições
    "small": 12,  # Texto secundário
    "button": 15,  # Texto de botões
}
