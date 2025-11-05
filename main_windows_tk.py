"""Versão Windows leve usando Tkinter (módulo da stdlib) para reduzir o tamanho do executável.
Este arquivo é pensado para ser empacotado com PyInstaller (--onefile --windowed).
"""

import os
import sys
import json
import tkinter as tk
from tkinter import messagebox


def load_questions():
    try:
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(base_path, "questions.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'questions.json' não encontrado.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Erro ao decodificar o arquivo 'questions.json'.")
        return None


class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Especialista - Avaliação de Risco")
        self.geometry("600x300")

        self.questions_data = load_questions()
        if not self.questions_data:
            self.destroy()
            return

        self.current_eixo_index = 0
        self.current_question_index = 0
        self.score = 0
        self.total_questions = sum(
            len(eixo["perguntas"]) for eixo in self.questions_data["eixos"]
        )

        self.progress_label = tk.Label(self, text="", font=(None, 12))
        self.progress_label.pack(pady=10)

        self.question_label = tk.Label(
            self, text="", wraplength=560, justify="center", font=(None, 14)
        )
        self.question_label.pack(pady=30)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack()

        yes_btn = tk.Button(
            buttons_frame, text="Sim", width=10, command=lambda: self.answer("sim")
        )
        yes_btn.pack(side="left", padx=10)

        no_btn = tk.Button(
            buttons_frame, text="Não", width=10, command=lambda: self.answer("nao")
        )
        no_btn.pack(side="left", padx=10)

        self.display_question()

    def display_question(self):
        eixo = self.questions_data["eixos"][self.current_eixo_index]
        if self.current_question_index < len(eixo["perguntas"]):
            question = eixo["perguntas"][self.current_question_index]
            current_question_number = (
                sum(
                    len(self.questions_data["eixos"][i]["perguntas"])
                    for i in range(self.current_eixo_index)
                )
                + self.current_question_index
                + 1
            )
            self.progress_label.config(
                text=f"Pergunta {current_question_number} de {self.total_questions}"
            )
            self.question_label.config(text=question["texto"])
            self.title(eixo["nome"])
        else:
            self.show_results()

    def answer(self, response):
        eixo = self.questions_data["eixos"][self.current_eixo_index]
        question = eixo["perguntas"][self.current_question_index]
        if response == "sim":
            self.score += question.get("peso", 0)

        self.current_question_index += 1

        if self.current_question_index < len(eixo["perguntas"]):
            self.display_question()
        else:
            self.current_eixo_index += 1
            self.current_question_index = 0
            if self.current_eixo_index < len(self.questions_data["eixos"]):
                self.display_question()
            else:
                self.show_results()

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
        messagebox.showinfo("Resultado da Avaliação", result_text)
        self.destroy()


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()
