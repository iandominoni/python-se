"""Versão Windows modular usando Tkinter com histórico detalhado de respostas.
Este arquivo é pensado para ser empacotado com PyInstaller (--onefile --windowed).
Design moderno e responsivo com suporte a múltiplos eixos.
Plataforma: Windows
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    DANGER_COLOR,
    LIGHT_BG,
    WHITE,
)
from data_manager import load_questions, QuestionManager, HistoryManager
from utils import get_risk_level, get_color_by_level, get_message_by_level
from ui_components_windows import UIHelper, HistoryCardWidget


class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Avaliação de Risco - DSM-5")
        self.geometry("800x650")
        self.configure(bg=PRIMARY_COLOR)
        self.resizable(True, True)

        # Carregar dados
        questions_data = load_questions()
        if not questions_data:
            self.destroy()
            return

        self.question_manager = QuestionManager(questions_data)
        self.history_manager = HistoryManager()
        self.current_screen = "menu"
        self.selected_history_index = None

        self.main_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.show_menu()

    def clear_frame(self):
        """Limpa o frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        """Exibe o menu inicial"""
        self.clear_frame()
        self.current_screen = "menu"

        UIHelper.create_header(
            self.main_frame,
            "Sistema de Avaliação de Risco",
            "Transtornos Alimentares - Critérios DSM-5",
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=40)

        desc = tk.Label(
            content,
            text=f"Bem-vindo ao sistema de avaliação!\n\n"
            f"Este questionário contém {self.question_manager.total_questions} perguntas\n"
            "estruturadas em 5 eixos temáticos.\n\n"
            "Comportamento • Imagem • Emoção • Controle • Percepção",
            font=("Segoe UI", 12),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            justify="center",
        )
        desc.pack(pady=20)

        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=30, fill="x")

        start_btn = UIHelper.create_button(
            btn_frame, "▶ Iniciar Avaliação", self.start_quiz, SUCCESS_COLOR
        )
        start_btn.pack(side="left", padx=10, fill="x", expand=True)

        history_btn = UIHelper.create_button(
            btn_frame, "📋 Histórico", self.show_history, SECONDARY_COLOR
        )
        history_btn.pack(side="left", padx=10, fill="x", expand=True)

    def show_history(self):
        """Exibe o histórico de avaliações"""
        self.clear_frame()
        self.current_screen = "history"

        UIHelper.create_header(self.main_frame, "Histórico de Avaliações")

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        if self.history_manager.get_count() == 0:
            empty_label = tk.Label(
                content,
                text="Nenhuma avaliação realizada ainda.",
                font=("Segoe UI", 12),
                bg=PRIMARY_COLOR,
                fg=LIGHT_BG,
            )
            empty_label.pack(pady=50)
        else:
            canvas = tk.Canvas(content, bg=PRIMARY_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=PRIMARY_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for idx, record in enumerate(self.history_manager.get_all()):
                self._create_history_item(scrollable_frame, idx + 1, record)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        back_btn = UIHelper.create_button(
            self.main_frame, "← Voltar", self.show_menu, SECONDARY_COLOR
        )
        back_btn.pack(pady=15, fill="x", padx=20)

    def _create_history_item(self, parent, number, data):
        """Cria um item de histórico com detalhes"""
        HistoryCardWidget.create_card(parent, number, data, self.show_history_details)

    def start_quiz(self):
        """Inicia o questionário"""
        self.question_manager.reset()
        self.display_question()

    def display_question(self):
        """Exibe uma pergunta"""
        self.clear_frame()
        self.current_screen = "quiz"

        if self.question_manager.is_finished():
            self.show_results()
            return

        question = self.question_manager.get_current_question()
        eixo = self.question_manager.get_current_eixo()
        current_number = self.question_manager.get_current_question_number()
        progress_pct = (current_number / self.question_manager.total_questions) * 100

        UIHelper.create_header(self.main_frame, eixo["nome"])

        progress_frame = tk.Frame(self.main_frame, bg=SECONDARY_COLOR)
        progress_frame.pack(fill="x")

        UIHelper.create_progress_bar(progress_frame, progress_pct)

        counter_label = tk.Label(
            progress_frame,
            text=f"Pergunta {current_number} de {self.question_manager.total_questions}",
            font=("Segoe UI", 10),
            bg=SECONDARY_COLOR,
            fg=LIGHT_BG,
            pady=5,
        )
        counter_label.pack()

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=30, pady=40)

        question_label = tk.Label(
            content,
            text=question["texto"],
            font=("Segoe UI", 14),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            wraplength=740,
            justify="center",
        )
        question_label.pack(pady=30, fill="both", expand=True)

        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=30, fill="x")

        yes_btn = UIHelper.create_button(
            btn_frame, "✓ Sim", lambda: self.answer("sim"), SUCCESS_COLOR
        )
        yes_btn.pack(side="left", padx=10, fill="x", expand=True)

        no_btn = UIHelper.create_button(
            btn_frame, "✗ Não", lambda: self.answer("nao"), DANGER_COLOR
        )
        no_btn.pack(side="left", padx=10, fill="x", expand=True)

    def answer(self, response):
        """Processa uma resposta"""
        has_more = self.question_manager.answer_question(response)

        if has_more:
            self.display_question()
        else:
            self.show_results()

    def show_history_details(self, index):
        """Exibe detalhes de uma avaliação do histórico"""
        self.clear_frame()
        self.current_screen = "history_details"

        assessment = self.history_manager.get_assessment(index)
        if not assessment:
            self.show_history()
            return

        # Header
        UIHelper.create_header(
            self.main_frame,
            f"Detalhes da Avaliação #{index + 1}",
            f"Data: {assessment['data']} | Nível: {assessment['level']}",
        )

        # Conteúdo com scroll
        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(content, bg=PRIMARY_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=PRIMARY_COLOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Exibir respostas por eixo
        current_eixo = None
        for resp in assessment["responses"]:
            if resp["eixo_nome"] != current_eixo:
                current_eixo = resp["eixo_nome"]

                # Título do eixo
                eixo_frame = tk.Frame(scrollable_frame, bg=SECONDARY_COLOR)
                eixo_frame.pack(fill="x", pady=(10, 5), padx=5)

                eixo_label = tk.Label(
                    eixo_frame,
                    text=current_eixo,
                    font=("Segoe UI", 12, "bold"),
                    bg=SECONDARY_COLOR,
                    fg=WHITE,
                    pady=8,
                    padx=10,
                )
                eixo_label.pack(anchor="w")

            # Resposta individual
            resp_frame = tk.Frame(scrollable_frame, bg=LIGHT_BG)
            resp_frame.pack(fill="x", pady=5, padx=10)

            # Número e tipo de resposta
            response_symbol = "✓ SIM" if resp["resposta"] == "sim" else "✗ NÃO"
            response_color = (
                SUCCESS_COLOR if resp["resposta"] == "sim" else DANGER_COLOR
            )

            header_frame = tk.Frame(resp_frame, bg=LIGHT_BG)
            header_frame.pack(fill="x", padx=10, pady=(8, 0))

            q_label = tk.Label(
                header_frame,
                text=f"Q{resp['question_id']:02d}: {response_symbol}",
                font=("Segoe UI", 10, "bold"),
                bg=LIGHT_BG,
                fg=response_color,
            )
            q_label.pack(anchor="w")

            # Pergunta
            question_label = tk.Label(
                resp_frame,
                text=resp["pergunta_texto"],
                font=("Segoe UI", 9),
                bg=LIGHT_BG,
                fg=PRIMARY_COLOR,
                wraplength=700,
                justify="left",
            )
            question_label.pack(anchor="w", fill="x", padx=10, pady=5)

            # Justificativa (se existir)
            if resp.get("justificativa"):
                justif_label = tk.Label(
                    resp_frame,
                    text=resp["justificativa"],
                    font=("Segoe UI", 8, "italic"),
                    bg=LIGHT_BG,
                    fg="#7F8C8D",
                    wraplength=700,
                    justify="left",
                )
                justif_label.pack(anchor="w", fill="x", padx=10, pady=(0, 5))

            # Pontuação
            points_label = tk.Label(
                resp_frame,
                text=f"Pontos: +{resp['pontos']}",
                font=("Segoe UI", 8),
                bg=LIGHT_BG,
                fg="#7F8C8D",
            )
            points_label.pack(anchor="e", padx=10, pady=(0, 8))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Resumo final
        summary_frame = tk.Frame(self.main_frame, bg=LIGHT_BG)
        summary_frame.pack(fill="x", pady=10, padx=20)

        summary_text = (
            f"Total: {assessment['score']} pontos | Nível: {assessment['level']}"
        )
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=("Segoe UI", 10, "bold"),
            bg=LIGHT_BG,
            fg=PRIMARY_COLOR,
            pady=10,
        )
        summary_label.pack()

        # Botão Voltar
        back_btn = UIHelper.create_button(
            self.main_frame, "← Voltar ao Histórico", self.show_history, SECONDARY_COLOR
        )
        back_btn.pack(pady=10, fill="x", padx=20)

    def show_results(self):
        """Exibe o resultado final"""
        self.clear_frame()
        self.current_screen = "results"

        risk_level = get_risk_level(self.question_manager.score)
        color = get_color_by_level(risk_level)

        UIHelper.create_header(
            self.main_frame, "✓ Avaliação Concluída!", bg_color=color
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        result_frame = tk.Frame(content, bg=LIGHT_BG, relief="flat")
        result_frame.pack(fill="x", pady=20)

        level_label = tk.Label(
            result_frame,
            text=f"Nível de Risco: {risk_level}",
            font=("Segoe UI", 18, "bold"),
            bg=LIGHT_BG,
            fg=color,
            pady=15,
        )
        level_label.pack()

        msg_label = tk.Label(
            content,
            text=get_message_by_level(risk_level),
            font=("Segoe UI", 11),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            wraplength=700,
            justify="center",
        )
        msg_label.pack(pady=15)

        score_label = tk.Label(
            content,
            text=f"Pontuação Total: {self.question_manager.score}",
            font=("Segoe UI", 9),
            bg=PRIMARY_COLOR,
            fg=LIGHT_BG,
        )
        score_label.pack(pady=5)

        note_label = tk.Label(
            content,
            text="⚠ Ferramenta de triagem educacional.\nNão substitui avaliação clínica profissional.",
            font=("Segoe UI", 8),
            bg=PRIMARY_COLOR,
            fg="#E74C3C",
            justify="center",
        )
        note_label.pack(pady=10)

        assessment_data = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "level": risk_level,
            "score": self.question_manager.score,
            "responses": self.question_manager.responses,
        }
        self.history_manager.add_assessment(assessment_data)

        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=20, fill="x")

        again_btn = UIHelper.create_button(
            btn_frame, "▶ Outra Avaliação", self.show_menu, SUCCESS_COLOR
        )
        again_btn.pack(side="left", padx=10, fill="x", expand=True)

        history_btn = UIHelper.create_button(
            btn_frame, "📋 Histórico", self.show_history, SECONDARY_COLOR
        )
        history_btn.pack(side="left", padx=10, fill="x", expand=True)


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()
