import os

os.environ["QT_QPA_PLATFORM"] = "xcb"
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt


class ExpertSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Especialista - Avaliação de Risco")
        self.setGeometry(100, 100, 600, 400)

        self.questions_data = self.load_questions()
        if not self.questions_data:
            sys.exit(1)  # Termina se as perguntas não puderem ser carregadas

        self.current_eixo_index = 0
        self.current_question_index = 0
        self.score = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.question_label = QLabel(self)
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("font-size: 16px; margin: 20px;")

        self.buttons_layout = QHBoxLayout()
        self.yes_button = QPushButton("Sim")
        self.yes_button.setStyleSheet("font-size: 14px; padding: 10px 20px;")
        self.yes_button.clicked.connect(lambda: self.answer("sim"))

        self.no_button = QPushButton("Não")
        self.no_button.setStyleSheet("font-size: 14px; padding: 10px 20px;")
        self.no_button.clicked.connect(lambda: self.answer("nao"))

        self.buttons_layout.addWidget(self.yes_button)
        self.buttons_layout.addWidget(self.no_button)

        self.layout.addWidget(self.question_label)
        self.layout.addLayout(self.buttons_layout)

        self.start_quiz()

    def load_questions(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.show_error("Erro", "Arquivo 'questions.json' não encontrado.")
            return None
        except json.JSONDecodeError:
            self.show_error("Erro", "Erro ao decodificar o arquivo 'questions.json'.")
            return None

    def start_quiz(self):
        if self.questions_data and self.current_eixo_index < len(
            self.questions_data["eixos"]
        ):
            self.display_question()
        else:
            self.show_results()

    def display_question(self):
        eixo = self.questions_data["eixos"][self.current_eixo_index]
        self.setWindowTitle(eixo["nome"])
        if self.current_question_index < len(eixo["perguntas"]):
            question = eixo["perguntas"][self.current_question_index]
            self.question_label.setText(question["texto"])
        else:
            self.show_results()

    def answer(self, response):
        eixo = self.questions_data["eixos"][self.current_eixo_index]
        question = eixo["perguntas"][self.current_question_index]

        if response == "sim":
            self.score += question["peso"]

        self.current_question_index += 1
        self.display_question()

    def get_risk_level(self):
        if self.score <= 10:
            return "Baixo"
        elif 11 <= self.score <= 20:
            return "Médio"
        elif 21 <= self.score <= 30:
            return "Alto"
        else:
            return "Crítico"

    def show_results(self):
        risk_level = self.get_risk_level()
        result_text = (
            f"Avaliação Concluída!\n\n"
            f"Pontuação Total: {self.score}\n"
            f"Nível de Risco: {risk_level}"
        )

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Resultado da Avaliação")
        msg_box.setText(result_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()
        self.close()

    def show_error(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpertSystemApp()
    window.show()
    sys.exit(app.exec())
