from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QScrollArea,
    QLineEdit,
    QStackedWidget,
    QProgressBar,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
import sys
import os
from datetime import datetime
from config import *
from data_manager import QuestionManager, HistoryManager, load_questions
from utils import get_risk_level
from pdf_generator import PDFGenerator


class ModernButton(QPushButton):
    """Botão moderno com bordas arredondadas e hover effect."""

    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.base_color = color
        self.display_color = self.soften_color(self.base_color, 12)
        self.hover_color = self.lighten_color(self.display_color, 12)
        self.setMinimumHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_style()

    def apply_style(self):
        """Aplica estilos CSS com boas práticas de acessibilidade."""
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.display_color};
                color: white;
                border: none;
                border-radius: 18px;
                padding: 18px 34px;
                font-size: 17px;
                font-weight: 600;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self.display_color};
                padding-top: 19px;
                padding-bottom: 17px;
            }}
            QPushButton:disabled {{
                background-color: #9CA3AF;
            }}
        """
        )

    @staticmethod
    def lighten_color(color, amount=20):
        """Clareia uma cor em hexadecimal."""
        color = color.lstrip("#")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def soften_color(color, amount=12):
        """Suaviza a cor aproximando-a do branco para menos agressividade."""
        return ModernButton.lighten_color(color, amount)


class StatCard(QFrame):
    """Card de estatística com design médico profissional."""

    def __init__(self, label, value, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {color};
                border-radius: 16px;
                border: none;
                padding: 22px 18px;
            }}
        """
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        # Valor
        value_label = QLabel(str(value))
        value_label.setStyleSheet(
            """
            color: white;
            font-size: 38px;
            font-weight: 700;
            font-family: 'Segoe UI', -apple-system, sans-serif;
            
        """
        )
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        # Label
        text_label = QLabel(label)
        text_label.setStyleSheet(
            """
            color: rgba(255, 255, 255, 0.95);
            font-size: 15px;
            font-weight: 600;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)

        self.setLayout(layout)

        # Sombra sutil
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 22))
        self.setGraphicsEffect(shadow)


class HistoryCard(QFrame):
    """Card de histórico com design moderno."""

    def __init__(self, number, data, on_view_details, parent=None):
        super().__init__(parent)
        self.data = data
        self.on_view_details = on_view_details
        self.number = number

        level = data.get("level", "Baixo")
        level_color = LEVEL_COLORS.get(level, SECONDARY_COLOR)
        # Cores mais suaves e amigáveis
        soft_colors = {
            "Baixo": "#E0F2FE",  # Azul claro
            "Médio": "#FEF3C7",  # Amarelo claro
            "Alto": "#FED7D7",  # Vermelho fraco
            "Crítico": "#FED7D7",  # Vermelho fraco
        }
        card_bg_color = soft_colors.get(level, "#E0F2FE")
        text_color = "#1F2937"  # Texto escuro para melhor contraste
        level_icon = LEVEL_ICONS.get(level, "●")

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {card_bg_color};
                border-radius: 12px;
                border: none;
                padding: 14px 16px;
                margin: 6px 0px;
            }}
            QFrame:hover {{
                background-color: {card_bg_color};
            }}
        """
        )

        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Indicador de nível (ponto colorido)
        indicator = QFrame()
        indicator.setFixedSize(10, 10)
        indicator.setStyleSheet(f"background-color: {level_color}; border-radius: 5px;")
        layout.addWidget(indicator, 0, Qt.AlignmentFlag.AlignVCenter)

        # Informações
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # Nome do paciente
        patient_name = data.get("patient_name", "Paciente sem nome")
        name_label = QLabel(patient_name)
        name_label.setStyleSheet(
            f"""
            color: {text_color};
            font-size: 15px;
            font-weight: 600;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        info_layout.addWidget(name_label)

        # Data e resultado
        info_text = f"Avaliação #{number}  •  {data['data']}  •  {level_icon} {level}  •  {data['score']} pts"
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            f"""
            color: #6B7280;
            font-size: 12px;
            font-weight: 400;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)

        layout.addLayout(info_layout, 1)

        # Botão de detalhes
        details_btn = ModernButton("Ver →", level_color)
        details_btn.setMaximumWidth(90)
        details_btn.setMinimumHeight(36)
        details_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {level_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }}
            QPushButton:hover {{
                background-color: {ModernButton.lighten_color(level_color, 15)};
            }}
            QPushButton:pressed {{
                padding-top: 9px;
                padding-bottom: 7px;
            }}
        """
        )
        details_btn.clicked.connect(lambda: self.on_view_details(number - 1))
        layout.addWidget(
            details_btn, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.setLayout(layout)

        # Sombra para contraste visual
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)


class ExpertSystemApp(QMainWindow):
    """Aplicação principal do sistema de avaliação."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Avaliação de Risco - DSM-5")
        self.setMinimumSize(950, 700)

        # Carregar dados
        questions_data = load_questions()
        if not questions_data:
            sys.exit(1)

        self.question_manager = QuestionManager(questions_data)
        self.history_manager = HistoryManager()

        # Configurar UI
        self.setup_ui()
        self.show_menu()

        # Centralizar janela
        self.center_window()

    def setup_ui(self):
        """Configura a interface principal."""
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self._apply_global_stylesheet()

    def _apply_global_stylesheet(self):
        """Aplica estilo global profissional."""
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {PRIMARY_COLOR};
            }}
            QScrollArea {{
                border: none;
                background-color: {PRIMARY_COLOR};
            }}
            QScrollBar:vertical {{
                background-color: {PRIMARY_COLOR};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #D1D5DB;
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #9CA3AF;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
        )

    def center_window(self):
        """Centraliza a janela na tela."""
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        center = screen.center()
        window.moveCenter(center)
        self.move(window.topLeft())

    def clear_stack(self):
        """Remove todos os widgets do stack."""
        while self.stack.count():
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

    def _create_header_label(self, text, font_size, text_color, object_name):
        """Cria um label para header com propriedades padrão."""
        label = QLabel(text)
        label.setStyleSheet(
            f"""
            color: {text_color};
            font-size: {font_size}px;
            font-weight: 700;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setObjectName(object_name)
        label.setProperty("headerColor", text_color)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        return label

    def create_header(self, title, subtitle=None, bg_color=SECONDARY_COLOR):
        """Cria cabeçalho; fora da home usar azul, na home branco."""
        header = QFrame()
        header.setStyleSheet(
            f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 0px;
                padding: 24px 20px;
                border: none;
            }}
        """
        )
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(6)

        # Título
        if bg_color == WHITE:
            title_frame = QFrame()
            title_frame.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {WHITE};
                    border-radius: 5px;
                    padding: 10px 20px;
                }}
            """
            )
            title_layout = QVBoxLayout()
            title_label = self._create_header_label(
                title, 32, DARK_TEXT, "app_header_title"
            )
            title_layout.addWidget(title_label)
            title_frame.setLayout(title_layout)
            layout.addWidget(title_frame)
        else:
            title_label = self._create_header_label(
                title, 32, WHITE, "app_header_title"
            )
            layout.addWidget(title_label)

        # Subtítulo
        if subtitle:
            subtitle_color = SECONDARY_TEXT if bg_color == WHITE else LIGHT_BG
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet(
                f"""
                color: {subtitle_color};
                font-size: 18px;
                font-weight: 500;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                margin-top: 6px;
            """
            )
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setWordWrap(True)
            subtitle_label.setObjectName("app_header_subtitle")
            subtitle_label.setProperty("headerColor", subtitle_color)
            subtitle_label.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            layout.addWidget(subtitle_label)

        header.setLayout(layout)
        return header

    def adjust_header_fonts(self):
        """Ajusta tamanhos de fonte do header conforme largura da janela."""
        width = self.width()
        # Breakpoints simples
        if width < 520:
            title_size = 22
            subtitle_size = 15
        elif width < 650:
            title_size = 24
            subtitle_size = 16
        elif width < 800:
            title_size = 27
            subtitle_size = 17
        else:
            title_size = 32
            subtitle_size = 18

        # Largura máxima para wrap confortável
        max_w = max(280, width - 48)

        # Atualiza todos os títulos
        for lbl in self.findChildren(QLabel, "app_header_title"):
            color = lbl.property("headerColor") or WHITE
            lbl.setMaximumWidth(max_w)
            lbl.setStyleSheet(
                f"""
                color: {color};
                font-size: {title_size}px;
                font-weight: 700;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            """
            )
        for lbl in self.findChildren(QLabel, "app_header_subtitle"):
            color = lbl.property("headerColor") or LIGHT_BG
            lbl.setMaximumWidth(max_w)
            lbl.setStyleSheet(
                f"""
                color: {color};
                font-size: {subtitle_size}px;
                font-weight: 500;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                margin-top: 6px;
            """
            )

    def resizeEvent(self, event):
        """Override para responsividade do header."""
        super().resizeEvent(event)
        self.adjust_header_fonts()

    def show_menu(self):
        """Exibe o menu principal."""
        self.clear_stack()

        # Widget principal
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header (home em branco)
        header = self.create_header(
            "Sistema de Avaliação de Risco",
            "Transtornos Alimentares - Critérios DSM-5",
            bg_color=WHITE,
        )
        main_layout.addWidget(header)

        # Conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: {PRIMARY_COLOR};")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(20)

        # Cards de estatísticas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        total_assessments = self.history_manager.get_count()

        stats_layout.addWidget(
            StatCard("Avaliações", total_assessments, SECONDARY_COLOR)
        )
        stats_layout.addWidget(
            StatCard("Perguntas", self.question_manager.total_questions, ACCENT_COLOR)
        )
        stats_layout.addWidget(StatCard("Eixos", 5, SECONDARY_COLOR))

        content_layout.addLayout(stats_layout)

        # Descrição
        desc_frame = QFrame()
        desc_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 10px;
                padding: 20px;
            }}
        """
        )

        desc_layout = QVBoxLayout()
        desc_text = QLabel(
            f"Este questionário contém {self.question_manager.total_questions} perguntas estruturadas\n"
            "em 5 eixos temáticos para avaliação de risco.\n\n"
            "Comportamento Alimentar  •  Imagem Corporal  •  Emoção e Autocontrole\n"
            "Controle de Peso  •  Percepção e Cognição"
        )
        desc_text.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 14px;
            font-weight: 400;
            line-height: 1.6;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        desc_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_text.setWordWrap(True)
        desc_layout.addWidget(desc_text)
        desc_frame.setLayout(desc_layout)
        content_layout.addWidget(desc_frame)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        start_btn = ModernButton("Iniciar Nova Avaliação", SECONDARY_COLOR)
        start_btn.clicked.connect(self.start_quiz)
        btn_layout.addWidget(start_btn)

        history_btn = ModernButton("Visualizar Histórico", ACCENT_COLOR)
        history_btn.clicked.connect(self.show_history)
        btn_layout.addWidget(history_btn)

        content_layout.addLayout(btn_layout)
        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)

        self.stack.addWidget(widget)

    def show_history(self):
        """Exibe o histórico de avaliações."""
        self.clear_stack()

        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header("Histórico de Avaliações", bg_color=SECONDARY_COLOR)
        main_layout.addWidget(header)

        # Conteúdo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: {PRIMARY_COLOR}; border: none;")

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        content_widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")

        if self.history_manager.get_count() == 0:
            empty_label = QLabel("Nenhuma avaliação realizada ainda.")
            empty_label.setStyleSheet(
                f"""
                color: {DARK_TEXT};
                font-size: 14px;
                font-family: 'Segoe UI';
            """
            )
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(empty_label)
        else:
            for idx, record in enumerate(self.history_manager.get_all()):
                card = HistoryCard(idx + 1, record, self.show_history_details)
                content_layout.addWidget(card)

        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        main_layout.addWidget(scroll)

        # Botão voltar (não ocupar tela toda)
        controls = QHBoxLayout()
        back_btn = ModernButton("← Voltar", SECONDARY_COLOR)
        back_btn.setMaximumWidth(200)
        back_btn.setMinimumHeight(44)
        back_btn.clicked.connect(self.show_menu)
        controls.addWidget(back_btn, 0, Qt.AlignmentFlag.AlignLeft)
        controls.addStretch(1)
        controls.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(controls)

        widget.setLayout(main_layout)
        self.stack.addWidget(widget)

    def start_quiz(self):
        """Inicia o questionário."""
        self.question_manager.reset()
        self.display_question()

    def display_question(self):
        """Exibe uma pergunta."""
        if self.question_manager.is_finished():
            self.ask_patient_name()
            return

        self.clear_stack()

        question = self.question_manager.get_current_question()
        eixo = self.question_manager.get_current_eixo()
        current_number = self.question_manager.get_current_question_number()
        progress_pct = (current_number / self.question_manager.total_questions) * 100

        eixo_color = EIXO_COLORS.get(eixo["nome"], SECONDARY_COLOR)

        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header(eixo["nome"], bg_color=eixo_color)
        main_layout.addWidget(header)

        # Progress bar
        progress_frame = QFrame()
        progress_frame.setStyleSheet(f"background-color: {LIGHT_BG}; padding: 10px;")
        progress_layout = QVBoxLayout()

        # Barra de progresso responsiva (QProgressBar)
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(int(progress_pct))
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {BORDER_COLOR};
                border: none;
                border-radius: 4px;
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {eixo_color};
                border-radius: 4px;
            }}
        """
        )

        progress_layout.addWidget(progress_bar)

        # Texto de progresso
        progress_text = QLabel(
            f"Pergunta {current_number} de {self.question_manager.total_questions}  •  {int(progress_pct)}% Concluído"
        )
        progress_text.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', -apple-system, sans-serif;
            margin-top: 8px;
        """
        )
        progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(progress_text)

        progress_frame.setLayout(progress_layout)
        main_layout.addWidget(progress_frame)

        # Conteúdo
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Box centralizada para pergunta e respostas
        box = QFrame()
        box.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 16px;
                padding: 40px 50px;
                max-width: 600px;
            }}
        """
        )
        box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        box_layout = QVBoxLayout()
        box_layout.setSpacing(24)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card da pergunta
        question_label = QLabel(question["texto"])
        question_label.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 20px;
            font-weight: 600;
            line-height: 1.5;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setWordWrap(True)
        box_layout.addWidget(question_label)

        # Botões de resposta (verde SIM, vermelho NÃO)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_btn = ModernButton("Sim", "#059669")  # Verde
        yes_btn.setMinimumWidth(140)
        yes_btn.clicked.connect(lambda: self.answer(True))
        btn_layout.addWidget(yes_btn)

        no_btn = ModernButton("Não", "#DC2626")  # Vermelho
        no_btn.setMinimumWidth(140)
        no_btn.clicked.connect(lambda: self.answer(False))
        btn_layout.addWidget(no_btn)

        box_layout.addLayout(btn_layout)
        box.setLayout(box_layout)

        # Adicionar sombra ao box
        shadow = QGraphicsDropShadowEffect(box)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 25))
        box.setGraphicsEffect(shadow)

        # Centralizar a box
        box_container = QHBoxLayout()
        box_container.addStretch()
        box_container.addWidget(box, 0, Qt.AlignmentFlag.AlignCenter)
        box_container.addStretch()

        content_layout.addLayout(box_container)
        content_layout.addStretch()

        # Botão cancelar
        cancel_btn = ModernButton("Cancelar Avaliação", DANGER_COLOR)
        cancel_btn.setMaximumHeight(60)
        cancel_btn.clicked.connect(self.confirm_cancel)
        content_layout.addWidget(cancel_btn)

        content.setLayout(content_layout)
        main_layout.addWidget(content)

        widget.setLayout(main_layout)
        self.stack.addWidget(widget)

    def answer(self, response):
        """Processa uma resposta."""
        response_str = "sim" if response else "nao"
        has_more = self.question_manager.answer_question(response_str)

        if has_more:
            self.display_question()
        else:
            self.ask_patient_name()

    def confirm_cancel(self):
        """Confirma cancelamento."""
        # Implementação simplificada - volta ao menu
        self.show_menu()

    def ask_patient_name(self):
        """Solicita nome do paciente."""
        self.clear_stack()

        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header(
            "Questionário Completo", "Por favor, informe o nome do paciente"
        )
        main_layout.addWidget(header)

        # Conteúdo
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        # Label
        label = QLabel("Nome do Paciente:")
        label.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(label)

        # Campo de entrada
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {LIGHT_BG};
                color: {DARK_TEXT};
                border: 2px solid {BORDER_COLOR};
                border-radius: 8px;
                padding: 16px;
                font-size: 15px;
                font-weight: 500;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }}
            QLineEdit:focus {{
                border: 2px solid {SECONDARY_COLOR};
                background-color: {LIGHT_BG};
                outline: none;
            }}
            QLineEdit::placeholder {{
                color: {SECONDARY_TEXT};
            }}
        """
        )
        self.name_entry.setPlaceholderText("Digite o nome do paciente...")
        self.name_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_entry.returnPressed.connect(self.save_and_show_results)
        content_layout.addWidget(self.name_entry)

        content_layout.addSpacing(20)

        # Botões
        save_btn = ModernButton("Salvar e Continuar", SECONDARY_COLOR)
        save_btn.clicked.connect(self.save_and_show_results)
        content_layout.addWidget(save_btn)

        skip_btn = ModernButton("Continuar Anônimo", ACCENT_COLOR)
        skip_btn.clicked.connect(lambda: self.show_results("Anônimo"))
        content_layout.addWidget(skip_btn)

        content_layout.addStretch()

        content.setLayout(content_layout)
        main_layout.addWidget(content)

        widget.setLayout(main_layout)
        self.stack.addWidget(widget)

        # Focar no campo
        self.name_entry.setFocus()

    def save_and_show_results(self):
        """Salva nome e mostra resultados."""
        name = self.name_entry.text().strip() or "Anônimo"
        self.show_results(name)

    def show_results(self, patient_name):
        """Exibe resultados."""
        self.clear_stack()

        risk_level = get_risk_level(self.question_manager.score)
        color = LEVEL_COLORS.get(risk_level, SUCCESS_COLOR)
        icon = LEVEL_ICONS.get(risk_level, "●")

        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header(
            "Avaliação Concluída", "Resultado da Avaliação de Risco", color
        )
        main_layout.addWidget(header)

        # Scroll content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 20, 50, 20)
        content_layout.setSpacing(20)

        # Card paciente
        patient_card = QFrame()
        patient_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 10px;
                padding: 25px;
            }}
        """
        )

        patient_layout = QVBoxLayout()
        patient_label = QLabel(f"Paciente: {patient_name}")
        patient_label.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 24px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """
        )
        patient_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        patient_layout.addWidget(patient_label)
        patient_card.setLayout(patient_layout)

        content_layout.addWidget(patient_card)

        # Card resultado
        result_card = QFrame()
        result_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 40px;
            }}
        """
        )

        result_layout = QVBoxLayout()

        level_label = QLabel(f"{icon}  NÍVEL DE RISCO: {risk_level.upper()}")
        level_label.setStyleSheet(
            """
            color: white;
            font-size: 32px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """
        )
        level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(level_label)

        score_label = QLabel(f"Pontuação Total: {self.question_manager.score} pontos")
        score_label.setStyleSheet(
            """
            color: white;
            font-size: 20px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """
        )
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(score_label)

        result_card.setLayout(result_layout)
        content_layout.addWidget(result_card)

        # Card aviso
        note_card = QFrame()
        note_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 10px;
                padding: 30px;
            }}
        """
        )

        note_layout = QVBoxLayout()

        note_title = QLabel("AVISO IMPORTANTE")
        note_title.setStyleSheet(
            f"""
            color: {WARNING_COLOR};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """
        )
        note_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note_layout.addWidget(note_title)

        note_text = QLabel(
            "Esta avaliação é uma ferramenta de triagem e os resultados podem apresentar variações.\n\n"
            "A interpretação clínica deve considerar idade, contexto e histórico individual.\n\n"
            "Este instrumento NÃO substitui a avaliação de um profissional de saúde qualificado."
        )
        note_text.setStyleSheet(
            f"""
            color: {DARK_TEXT};
            font-size: 13px;
            font-family: 'Segoe UI';
        """
        )
        note_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note_text.setWordWrap(True)
        note_layout.addWidget(note_text)

        note_card.setLayout(note_layout)
        content_layout.addWidget(note_card)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        again_btn = ModernButton("Nova Avaliação", SECONDARY_COLOR)
        again_btn.clicked.connect(self.show_menu)
        btn_layout.addWidget(again_btn)

        hist_btn = ModernButton("Ver Histórico", ACCENT_COLOR)
        hist_btn.clicked.connect(self.show_history)
        btn_layout.addWidget(hist_btn)

        content_layout.addLayout(btn_layout)
        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        main_layout.addWidget(scroll)

        widget.setLayout(main_layout)
        self.stack.addWidget(widget)

        # Salvar no histórico
        assessment_data = {
            "patient_name": patient_name,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "level": risk_level,
            "score": self.question_manager.score,
            "responses": self.question_manager.responses,
        }
        self.history_manager.add_assessment(assessment_data)

    def export_to_pdf(self, record):
        """Exporta o prontuário do paciente para PDF."""
        try:
            pdf_gen = PDFGenerator()

            # Abrir diálogo para escolher local de salvamento
            default_filename = f"prontuario_{record.get('patient_name', 'paciente').replace(' ', '_')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Prontuário",
                default_filename,
                "PDF Files (*.pdf);;All Files (*)",
            )

            if file_path:
                pdf_gen.generate_prontuario(record, file_path)
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"Prontuário salvo com sucesso!\n\n{file_path}",
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao gerar PDF:\n{str(e)}",
            )

    def show_history_details(self, index):
        """Exibe detalhes da avaliação selecionada."""
        record = self.history_manager.get_assessment(index)
        if not record:
            self.show_history()
            return

        level = record.get("level", "Baixo")
        color = LEVEL_COLORS.get(level, SECONDARY_COLOR)
        icon = LEVEL_ICONS.get(level, "●")

        self.clear_stack()

        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header menor para detalhes
        header = QFrame()
        header.setStyleSheet(
            f"""
            QFrame {{
                background-color: {color};
                padding: 12px 20px;
                border: none;
            }}
        """
        )
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)

        header_title = QLabel("Detalhes da Avaliação")
        header_title.setStyleSheet(
            f"""
            color: white;
            font-size: 16px;
            font-weight: 700;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        header_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_title)

        header_subtitle = QLabel(f"Resultado: {level}")
        header_subtitle.setStyleSheet(
            f"""
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 500;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        header_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_subtitle)
        header.setLayout(header_layout)
        main_layout.addWidget(header)

        # Conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: {PRIMARY_COLOR}; border: none;")

        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        # Cores suaves por nível de risco (azul claro → vermelho fraco)
        soft_level_colors = {
            "Baixo": "#E0F2FE",  # Azul claro
            "Médio": "#FEF3C7",  # Amarelo claro
            "Alto": "#FED7D7",  # Vermelho fraco
            "Crítico": "#FED7D7",  # Vermelho fraco
        }
        soft_bg_color = soft_level_colors.get(level, "#E0F2FE")
        text_color = "#1F2937"  # Texto escuro
        level_color_strong = LEVEL_COLORS.get(level, SECONDARY_COLOR)

        # Card paciente (com cores suaves)
        patient_card = QFrame()
        patient_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {soft_bg_color};
                border-radius: 12px;
                border: none;
                padding: 18px 20px;
            }}
        """
        )
        patient_layout = QVBoxLayout()
        patient_layout.setSpacing(4)

        patient_name_label = QLabel(f"{record.get('patient_name', 'Paciente')}")
        patient_name_label.setStyleSheet(
            f"""
            color: {text_color};
            font-size: 18px;
            font-weight: 700;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        patient_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        patient_layout.addWidget(patient_name_label)

        date_label = QLabel(f"Avaliação: {record.get('data', '')}")
        date_label.setStyleSheet(
            f"""
            color: #6B7280;
            font-size: 13px;
            font-weight: 400;
            font-family: 'Segoe UI', -apple-system, sans-serif;
        """
        )
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        patient_layout.addWidget(date_label)
        patient_card.setLayout(patient_layout)

        # Sombra sutil
        shadow_patient = QGraphicsDropShadowEffect(patient_card)
        shadow_patient.setBlurRadius(8)
        shadow_patient.setOffset(0, 1)
        shadow_patient.setColor(QColor(0, 0, 0, 10))
        patient_card.setGraphicsEffect(shadow_patient)

        content_layout.addWidget(patient_card)

        # Card do resultado (cores suaves)
        result_card = QFrame()
        result_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {soft_bg_color};
                padding: 20px;
            }}
            """
        )
        result_layout = QVBoxLayout()
        result_layout.setSpacing(6)

        title = QLabel(f"{icon}  Nível de Risco: {level}")
        title.setStyleSheet(
            f"""
            color: {level_color_strong}; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';
            """
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        score_label = QLabel(f"Pontuação: {record.get('score', 0)} pontos")
        score_label.setStyleSheet(
            f"""
            color: {text_color}; font-size: 15px; font-weight: 600; font-family: 'Segoe UI';
            """
        )
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(title)
        result_layout.addWidget(score_label)
        result_card.setLayout(result_layout)

        # Sombra result_card sutil
        shadow = QGraphicsDropShadowEffect(result_card)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 1)
        shadow.setColor(QColor(0, 0, 0, 12))
        result_card.setGraphicsEffect(shadow)

        content_layout.addWidget(result_card)

        # Card de respostas com melhor organização
        responses_card = QFrame()
        responses_card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 12px;
                border: none;
                padding: 18px 20px;
            }}
        """
        )
        rl = QVBoxLayout()
        rl.setSpacing(10)

        # Título
        resp_title = QLabel("Respostas do Paciente")
        resp_title.setStyleSheet(
            f"color: {DARK_TEXT}; font-size: 15px; font-weight: 700; font-family: 'Segoe UI';"
        )
        rl.addWidget(resp_title)
        rl.addSpacing(8)

        if record.get("responses"):
            for resp in record["responses"]:
                # Frame individual para cada resposta com sombra
                resp_frame = QFrame()
                resp_frame.setStyleSheet(
                    f"""
                    QFrame {{
                        background-color: white;
                        border-radius: 8px;
                        padding: 10px 12px;
                        border: 1px solid {BORDER_COLOR};
                    }}
                """
                )
                resp_frame_layout = QVBoxLayout()
                resp_frame_layout.setContentsMargins(0, 0, 0, 0)
                resp_frame_layout.setSpacing(4)

                # Linha com resposta
                answer_icon = "✓" if resp["resposta"] == "sim" else "✗"
                answer_text = "SIM" if resp["resposta"] == "sim" else "NÃO"
                answer_color = "#059669" if resp["resposta"] == "sim" else "#DC2626"

                line = QLabel(f"Q{resp['question_id']:02d} • {resp['eixo_nome']}")
                line.setStyleSheet(
                    f"color: {DARK_TEXT}; font-size: 13px; font-weight: 600; font-family: 'Segoe UI';"
                )
                line.setWordWrap(True)
                resp_frame_layout.addWidget(line)

                # Resposta com cor
                resp_line = QLabel(
                    f"  {answer_icon} {answer_text}  (+{resp['pontos']} pts)"
                )
                resp_line.setStyleSheet(
                    f"color: {answer_color}; font-size: 13px; font-weight: 700; font-family: 'Segoe UI';"
                )
                resp_frame_layout.addWidget(resp_line)
                resp_frame.setLayout(resp_frame_layout)

                # Sombra individual para cada resposta
                shadow_resp = QGraphicsDropShadowEffect(resp_frame)
                shadow_resp.setBlurRadius(8)
                shadow_resp.setOffset(0, 2)
                shadow_resp.setColor(QColor(0, 0, 0, 15))
                resp_frame.setGraphicsEffect(shadow_resp)

                rl.addWidget(resp_frame)
        else:
            empty = QLabel("Sem respostas registradas.")
            empty.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 13px;")
            rl.addWidget(empty)

        responses_card.setLayout(rl)

        # Sombra externa sutil do card
        shadow2 = QGraphicsDropShadowEffect(responses_card)
        shadow2.setBlurRadius(12)
        shadow2.setOffset(0, 2)
        shadow2.setColor(QColor(0, 0, 0, 20))
        responses_card.setGraphicsEffect(shadow2)

        content_layout.addWidget(responses_card)
        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Barra de ações (botões centralizados)
        actions = QHBoxLayout()
        actions.addStretch(1)

        back_btn = ModernButton("← Voltar ao Histórico", SECONDARY_COLOR)
        back_btn.setMaximumWidth(240)
        back_btn.setMinimumHeight(44)
        back_btn.clicked.connect(self.show_history)
        actions.addWidget(back_btn, 0, Qt.AlignmentFlag.AlignCenter)

        actions.addSpacing(16)

        pdf_btn = ModernButton("Baixar PDF", ACCENT_COLOR)
        pdf_btn.setMaximumWidth(200)
        pdf_btn.setMinimumHeight(44)
        pdf_btn.clicked.connect(lambda: self.export_to_pdf(record))
        actions.addWidget(pdf_btn, 0, Qt.AlignmentFlag.AlignCenter)

        actions.addStretch(1)
        main_layout.addLayout(actions)

        widget.setLayout(main_layout)
        self.stack.addWidget(widget)


def main():
    """Função principal."""
    app = QApplication(sys.argv)

    # Configurar fonte padrão (maior para legibilidade)
    font = QFont("Segoe UI", 13)
    app.setFont(font)

    # Criar e mostrar janela
    window = ExpertSystemApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
