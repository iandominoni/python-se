"""Versão Linux modular usando PySide6 com histórico detalhado de respostas.
Design moderno e responsivo com suporte a múltiplos eixos.
Plataforma: Linux/WSL
"""

import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor

from config import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    DANGER_COLOR,
    LIGHT_BG,
    WHITE,
)
from data_manager import load_questions, QuestionManager, HistoryManager
from utils import get_risk_level, get_color_by_level, get_message_by_level
from ui_components_linux import UIHelper, HistoryCardWidget


class ExpertSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Avaliação de Risco - DSM-5")
        self.setGeometry(100, 100, 900, 700)

        questions_data = load_questions()
        if not questions_data:
            sys.exit(1)

        self.question_manager = QuestionManager(questions_data)
        self.history_manager = HistoryManager()
        self.current_screen = "menu"
        self.selected_history_index = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.show_menu()

    def clear_layout(self):
        """Limpa o layout central"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_menu(self):
        """Exibe o menu inicial"""
        self.clear_layout()
        self.current_screen = "menu"

        # Header
        header = UIHelper.create_header(
            "Sistema de Avaliação de Risco",
            "Transtornos Alimentares - Critérios DSM-5",
            SECONDARY_COLOR,
        )
        self.layout.addWidget(header)

        # Conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        desc_text = f"""Bem-vindo ao sistema de avaliação!

Este questionário contém {self.question_manager.total_questions} perguntas
estruturadas em 5 eixos temáticos.

Comportamento • Imagem • Emoção • Controle • Percepção"""

        desc_label = QLabel(desc_text)
        desc_label.setFont(QFont("Ubuntu", 12))
        desc_label.setStyleSheet(f"color: {WHITE}; background-color: {PRIMARY_COLOR};")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(desc_label)

        # Botões
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(15)

        start_btn = UIHelper.create_button(
            "▶ Iniciar Avaliação", self.start_quiz, SUCCESS_COLOR
        )
        history_btn = UIHelper.create_button(
            "📋 Histórico", self.show_history, SECONDARY_COLOR
        )

        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(history_btn)

        content_layout.addWidget(btn_frame)
        content_layout.addStretch()

        content_widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        self.layout.addWidget(content_widget)

    def show_history(self):
        """Exibe o histórico de avaliações"""
        self.clear_layout()
        self.current_screen = "history"

        # Header
        header = UIHelper.create_header("Histórico de Avaliações", "", SECONDARY_COLOR)
        self.layout.addWidget(header)

        # Conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        if self.history_manager.get_count() == 0:
            empty_label = QLabel("Nenhuma avaliação realizada ainda.")
            empty_label.setFont(QFont("Ubuntu", 12))
            empty_label.setStyleSheet(
                f"color: {LIGHT_BG}; background-color: {PRIMARY_COLOR};"
            )
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(empty_label)
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setSpacing(10)

            for idx, record in enumerate(self.history_manager.get_all()):
                card = HistoryCardWidget.create_card(
                    idx + 1, record, self.show_history_details
                )
                scroll_layout.addWidget(card)

            scroll_layout.addStretch()
            scroll_content.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
            scroll.setWidget(scroll_content)
            content_layout.addWidget(scroll)

        content_widget.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        self.layout.addWidget(content_widget)

        # Botão Voltar
        back_btn = UIHelper.create_button("← Voltar", self.show_menu, SECONDARY_COLOR)
        self.layout.addWidget(back_btn)

    def show_history_details(self, index):
        """Exibe detalhes completos de uma avaliação do histórico"""
        self.clear_layout()
        self.current_screen = "history_details"
        self.selected_history_index = index

        assessment = self.history_manager.get_assessment(index)
        if not assessment:
            self.show_history()
            return

        # Header
        header_text = f"Avaliação #{index + 1} - {assessment['data']}"
        header = UIHelper.create_header(header_text, "", SECONDARY_COLOR)
        self.layout.addWidget(header)

        # Conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Agrupar respostas por eixo
        responses_by_eixo = {}
        for response in assessment["responses"]:
            eixo_name = response.get("eixo_nome", "Desconhecido")
            if eixo_name not in responses_by_eixo:
                responses_by_eixo[eixo_name] = []
            responses_by_eixo[eixo_name].append(response)

        # Exibir respostas organizadas por eixo
        for eixo_name, responses in responses_by_eixo.items():
            # Header do eixo
            eixo_frame = QFrame()
            eixo_frame.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {SECONDARY_COLOR};
                    border-radius: 3px;
                    padding: 8px;
                }}
            """
            )
            eixo_layout = QVBoxLayout(eixo_frame)
            eixo_layout.setContentsMargins(10, 5, 10, 5)

            eixo_label = QLabel(eixo_name)
            eixo_label.setFont(QFont("Ubuntu", 12, QFont.Weight.Bold))
            eixo_label.setStyleSheet(f"color: {WHITE}; background-color: transparent;")
            eixo_layout.addWidget(eixo_label)

            eixo_frame.setLayout(eixo_layout)
            scroll_layout.addWidget(eixo_frame)

            # Respostas do eixo
            for response in responses:
                response_frame = QFrame()
                response_frame.setStyleSheet(
                    f"""
                    QFrame {{
                        background-color: {LIGHT_BG};
                        border-left: 4px solid {SECONDARY_COLOR};
                        border-radius: 3px;
                        padding: 10px;
                    }}
                """
                )
                response_layout = QVBoxLayout(response_frame)
                response_layout.setSpacing(5)

                # Número da pergunta e resposta
                resposta_tipo = response.get("resposta", "").upper()
                resposta_cor = SUCCESS_COLOR if resposta_tipo == "SIM" else DANGER_COLOR
                resposta_symbol = "✓ SIM" if resposta_tipo == "SIM" else "✗ NÃO"

                header_response = QLabel()
                header_response.setText(
                    f"Q{response.get('question_index', 0) + 1:02d}: "
                    f"<span style='color: {resposta_cor}'><b>{resposta_symbol}</b></span>"
                )
                header_response.setFont(QFont("Ubuntu", 10, QFont.Weight.Bold))
                header_response.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; background-color: transparent;"
                )
                response_layout.addWidget(header_response)

                # Texto da pergunta
                question_text = QLabel(response.get("pergunta_texto", ""))
                question_text.setFont(QFont("Ubuntu", 10))
                question_text.setStyleSheet(
                    f"color: {PRIMARY_COLOR}; background-color: transparent;"
                )
                question_text.setWordWrap(True)
                response_layout.addWidget(question_text)

                # Justificativa (se existir)
                if response.get("justificativa"):
                    justif_text = QLabel(response.get("justificativa", ""))
                    justif_text.setFont(QFont("Ubuntu", 8))
                    justif_text.setStyleSheet(
                        f"color: #7F8C8D; background-color: transparent; font-style: italic;"
                    )
                    justif_text.setWordWrap(True)
                    response_layout.addWidget(justif_text)

                # Pontos
                points_text = f"Pontos: +{response.get('pontos', 0)}"
                points_label = QLabel(points_text)
                points_label.setFont(QFont("Ubuntu", 9))
                points_label.setStyleSheet(
                    f"color: {SECONDARY_COLOR}; background-color: transparent;"
                )
                response_layout.addWidget(points_label)

                response_frame.setLayout(response_layout)
                scroll_layout.addWidget(response_frame)

        scroll_layout.addStretch()
        scroll_content.setStyleSheet(f"background-color: {PRIMARY_COLOR};")
        scroll.setWidget(scroll_content)
        self.layout.addWidget(scroll)

        # Frame de resumo
        summary_frame = QFrame()
        summary_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {SECONDARY_COLOR};
                border-radius: 5px;
                padding: 15px;
            }}
        """
        )
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setSpacing(5)

        total_label = QLabel(f"Pontuação Total: {assessment['score']}")
        total_label.setFont(QFont("Ubuntu", 12, QFont.Weight.Bold))
        total_label.setStyleSheet(f"color: {WHITE}; background-color: transparent;")
        summary_layout.addWidget(total_label)

        risk_color = get_color_by_level(assessment["level"])
        level_label = QLabel(f"Nível de Risco: {assessment['level']}")
        level_label.setFont(QFont("Ubuntu", 12, QFont.Weight.Bold))
        level_label.setStyleSheet(
            f"color: {risk_color}; background-color: transparent;"
        )
        summary_layout.addWidget(level_label)

        self.layout.addWidget(summary_frame)

        # Botão voltar
        back_btn = UIHelper.create_button(
            "← Voltar ao Histórico", self.show_history, SECONDARY_COLOR
        )
        self.layout.addWidget(back_btn)

    def start_quiz(self):
        """Inicia o questionário"""
        self.question_manager.reset()
        self.display_question()

    def display_question(self):
        """Exibe uma pergunta"""
        self.clear_layout()
        self.current_screen = "quiz"

        if self.question_manager.is_finished():
            self.show_results()
            return

        question = self.question_manager.get_current_question()
        eixo = self.question_manager.get_current_eixo()
        current_number = self.question_manager.get_current_question_number()
        progress_pct = (current_number / self.question_manager.total_questions) * 100

        # Header
        header = UIHelper.create_header(eixo["nome"], "", SECONDARY_COLOR)
        self.layout.addWidget(header)

        # Progress
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        progress_label = QLabel(
            f"Pergunta {current_number} de {self.question_manager.total_questions}"
        )
        progress_label.setFont(QFont("Ubuntu", 10))
        progress_label.setStyleSheet(
            f"color: {LIGHT_BG}; background-color: {SECONDARY_COLOR}; padding: 8px;"
        )
        progress_layout.addWidget(progress_label)

        progress_bar = UIHelper.create_progress_bar(progress_pct)
        progress_layout.addWidget(progress_bar)

        progress_widget.setStyleSheet(f"background-color: {SECONDARY_COLOR};")
        self.layout.addWidget(progress_widget)

        # Conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)

        question_label = QLabel(question["texto"])
        question_label.setFont(QFont("Ubuntu", 14))
        question_label.setStyleSheet(
            f"color: {WHITE}; background-color: {PRIMARY_COLOR};"
        )
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setWordWrap(True)
        content_layout.addWidget(question_label)

        # Botões
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(15)

        yes_btn = UIHelper.create_button(
            "✓ Sim", lambda: self.answer("sim"), SUCCESS_COLOR
        )
        no_btn = UIHelper.create_button(
            "✗ Não", lambda: self.answer("nao"), DANGER_COLOR
        )

        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)

        content_layout.addWidget(btn_frame)
        content_layout.addStretch()

        content_widget.setStyleSheet(
            f"background-color: {PRIMARY_COLOR}; padding: 30px;"
        )
        self.layout.addWidget(content_widget)

    def answer(self, response):
        """Processa uma resposta"""
        has_more = self.question_manager.answer_question(response)

        if has_more:
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        """Exibe o resultado final"""
        self.clear_layout()
        self.current_screen = "results"

        risk_level = get_risk_level(self.question_manager.score)
        color = get_color_by_level(risk_level)

        # Header
        header = UIHelper.create_header("✓ Avaliação Concluída!", "", color)
        self.layout.addWidget(header)

        # Conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Resultado
        level_label = QLabel(f"Nível de Risco: {risk_level}")
        level_label.setFont(QFont("Ubuntu", 18, QFont.Weight.Bold))
        level_label.setStyleSheet(
            f"color: {color}; background-color: {LIGHT_BG}; padding: 15px; border-radius: 5px;"
        )
        level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(level_label)

        # Mensagem
        msg_label = QLabel(get_message_by_level(risk_level))
        msg_label.setFont(QFont("Ubuntu", 11))
        msg_label.setStyleSheet(f"color: {WHITE}; background-color: {PRIMARY_COLOR};")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        content_layout.addWidget(msg_label)

        # Score
        score_label = QLabel(f"Pontuação Total: {self.question_manager.score}")
        score_label.setFont(QFont("Ubuntu", 9))
        score_label.setStyleSheet(
            f"color: {LIGHT_BG}; background-color: {PRIMARY_COLOR};"
        )
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(score_label)

        # Nota
        note_label = QLabel(
            "⚠ Ferramenta de triagem educacional.\nNão substitui avaliação clínica profissional."
        )
        note_label.setFont(QFont("Ubuntu", 8))
        note_label.setStyleSheet(f"color: #E74C3C; background-color: {PRIMARY_COLOR};")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(note_label)

        content_layout.addStretch()

        content_widget.setStyleSheet(
            f"background-color: {PRIMARY_COLOR}; padding: 30px;"
        )
        self.layout.addWidget(content_widget)

        # Salvar no histórico
        assessment_data = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "level": risk_level,
            "score": self.question_manager.score,
            "responses": self.question_manager.responses,
        }
        self.history_manager.add_assessment(assessment_data)

        # Botões
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(15)

        again_btn = UIHelper.create_button(
            "▶ Outra Avaliação", self.show_menu, SUCCESS_COLOR
        )
        history_btn = UIHelper.create_button(
            "📋 Histórico", self.show_history, SECONDARY_COLOR
        )

        btn_layout.addWidget(again_btn)
        btn_layout.addWidget(history_btn)

        self.layout.addWidget(btn_frame)


def main():
    app = QApplication(sys.argv)
    window = ExpertSystemApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
