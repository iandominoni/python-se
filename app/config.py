"""
Módulo de configuração de cores e constantes - DESIGN PROFISSIONAL MODERNO.
"""

# Paleta de cores profissional para área da saúde - WCAG 2.1 AA compliant
# Baseada em estudos de psicologia das cores em ambientes médicos
PRIMARY_COLOR = "#F8F9FA"  # Fundo principal - Cinza muito claro (neutro, calmo)
SECONDARY_COLOR = "#0D7377"  # Azul-teal médico (confiança, profissionalismo)
ACCENT_COLOR = "#14BDBE"  # Teal claro (tecnologia, modernidade)
SUCCESS_COLOR = "#059669"  # Verde médico (saúde, positivo)
WARNING_COLOR = "#D97706"  # Laranja médico (atenção, cuidado)
DANGER_COLOR = "#DC2626"  # Vermelho médico (urgência, alerta)
LIGHT_BG = "#FFFFFF"  # Fundo dos cards - Branco puro (clareza)
WHITE = "#FFFFFF"  # Branco puro
CARD_BG = "#FFFFFF"  # Fundo dos cards
DARK_TEXT = "#1F2937"  # Texto principal (contraste 7:1)
SECONDARY_TEXT = "#6B7280"  # Texto secundário (contraste 4.5:1)
BORDER_COLOR = "#E5E7EB"  # Bordas suaves
HOVER_BG = "#F3F4F6"  # Background hover sutil

# Cores para níveis de risco - Padrão médico internacional
LEVEL_COLORS = {
    "Baixo": "#059669",  # Verde médico - Estável
    "Médio": "#D97706",  # Laranja médico - Observação
    "Alto": "#DC2626",  # Vermelho médico - Atenção
    "Crítico": "#991B1B",  # Vermelho escuro - Crítico
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

# Cores dos eixos temáticos - Diferenciação visual clara
EIXO_COLORS = {
    "Comportamento Alimentar": "#0D7377",  # Teal médio
    "Imagem Corporal": "#14BDBE",  # Teal claro
    "Emoção e Autocontrole": "#0891B2",  # Cyan médico
    "Controle de Peso": "#0284C7",  # Azul médico
    "Percepção e Cognição": "#0369A1",  # Azul profundo
}

# Tamanhos de fonte para projeção
FONT_SIZES = {
    "title": 40,  # Títulos principais - Montserrat Bold
    "subtitle": 20,  # Subtítulos - Poppins Regular
    "header": 26,  # Headers de seção - Poppins Bold
    "body": 16,  # Texto principal - Poppins Regular
    "label": 14,  # Labels e descrições - Poppins Regular
    "small": 12,  # Texto secundário - Poppins Regular
    "button": 15,  # Texto de botões - Poppins Bold
}

# Fontes principais - Montserrat e Poppins
FONT_FAMILY_TITLE = "Montserrat"  # Para títulos (Bold)
FONT_FAMILY_BODY = "Poppins"  # Para texto geral (Regular/Bold)

# Configurações de estilo
BORDER_RADIUS = 2  # Raio de borda para elementos (Tkinter usa bd/relief)
