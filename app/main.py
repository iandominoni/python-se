"""Versão Windows PROFISSIONAL usando Tkinter com histórico detalhado de respostas.
Este arquivo é pensado para ser empacotado com PyInstaller (--onefile --windowed).
Design moderno, profissional e otimizado para projeção em telas grandes.
Sistema de responsividade integrado (VW/VH).
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
    ACCENT_COLOR,
    PURPLE,
    PINK,
    ORANGE,
    GREEN,
    BLUE,
    TEAL,
    INDIGO,
    LEVEL_COLORS,
    LEVEL_ICONS,
    MOTIVATIONAL_MESSAGES,
    EIXO_COLORS,
    FONT_SIZES,
    DARK_TEXT,
)
from data_manager import load_questions, QuestionManager, HistoryManager
from utils import get_risk_level, get_color_by_level, get_message_by_level
from ui_components_windows import UIHelper, HistoryCardWidget
from responsive import ResponsiveHelper, vw, vh, responsive_font, responsive_padding


class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Avaliação de Risco - DSM-5")

        # Inicializar sistema de responsividade ANTES de usar

        # Configuração inicial responsiva
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Definir tamanho baseado na resolução (85% da tela)
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)

        # Centralizar janela
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(bg=PRIMARY_COLOR)
        self.resizable(True, True)

        # Inicializar ResponsiveHelper após geometry estar definida
        ResponsiveHelper.initialize(self)

        # Configurar peso das linhas/colunas para responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configurar responsividade do main_frame
        self.main_frame.grid_rowconfigure(0, weight=0)  # Header fixo
        self.main_frame.grid_rowconfigure(1, weight=1)  # Conteúdo expansível
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Registrar callback para redesenho em redimensionamento
        ResponsiveHelper.register_callback(self._on_window_resized)

        self.show_menu()

    def _on_window_resized(self, width, height):
        """Callback quando a janela é redimensionada - redesenha a tela atual."""
        # Redesenhar apenas se mudança significativa
        if self.current_screen == "menu":
            self.show_menu()
        elif self.current_screen == "quiz" and hasattr(
            self.question_manager, "current_eixo_index"
        ):
            self.display_question()
        elif self.current_screen == "history":
            self.show_history()

    def _on_resize(self, event):
        """Removido - agora usa ResponsiveHelper"""
        pass

    def clear_frame(self):
        """Limpa o frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        """Exibe o menu inicial"""
        self.clear_frame()
        self.current_screen = "menu"

        # Header profissional
        UIHelper.create_header(
            self.main_frame,
            "Sistema de Avaliação de Risco",
            "Transtornos Alimentares - Critérios DSM-5",
            SECONDARY_COLOR,
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # Estatísticas do usuário
        stats_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        stats_frame.pack(fill="x", pady=20)

        total_assessments = self.history_manager.get_count()

        UIHelper.create_stat_card(
            stats_frame, "Avaliações", total_assessments, "chart", PURPLE
        )
        UIHelper.create_stat_card(
            stats_frame,
            "Perguntas",
            self.question_manager.total_questions,
            "list",
            BLUE,
        )
        UIHelper.create_stat_card(stats_frame, "Eixos", 5, "star", PINK)

        # Descrição
        desc = tk.Label(
            content,
            text=f"Este questionário contém {self.question_manager.total_questions} perguntas estruturadas\n"
            "em 5 eixos temáticos para avaliação de risco.\n\n"
            "Comportamento Alimentar  •  Imagem Corporal  •  Emoção e Autocontrole\n"
            "Controle de Peso  •  Percepção e Cognição",
            font=("Segoe UI", FONT_SIZES["body"]),
            bg=PRIMARY_COLOR,
            fg=LIGHT_BG,
            justify="center",
        )
        desc.pack(pady=20)

        # Botões de ação
        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=30, fill="x", padx=20)

        start_btn = UIHelper.create_button(
            btn_frame,
            "Iniciar Nova Avaliação",
            self.start_quiz,
            SUCCESS_COLOR,
        )
        start_btn.pack(side="left", padx=10, fill="x", expand=True)

        history_btn = UIHelper.create_button(
            btn_frame,
            "Visualizar Histórico",
            self.show_history,
            INDIGO,
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

            # Habilitar scroll com mouse wheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

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
        """Exibe uma pergunta com opção de voltar"""
        self.clear_frame()
        self.current_screen = "quiz"

        if self.question_manager.is_finished():
            self.ask_patient_name()
            return

        question = self.question_manager.get_current_question()
        eixo = self.question_manager.get_current_eixo()
        current_number = self.question_manager.get_current_question_number()
        progress_pct = (current_number / self.question_manager.total_questions) * 100

        # Determinar cor do eixo
        eixo_color = EIXO_COLORS.get(eixo["nome"], INDIGO)

        UIHelper.create_header(self.main_frame, eixo["nome"], bg_color=eixo_color)

        progress_frame = tk.Frame(self.main_frame, bg=SECONDARY_COLOR)
        progress_frame.pack(fill="x")

        UIHelper.create_progress_bar(progress_frame, progress_pct, show_text=True)

        counter_label = tk.Label(
            progress_frame,
            text=f"•  Pergunta {current_number} de {self.question_manager.total_questions}",
            font=("Segoe UI", FONT_SIZES["label"], "bold"),
            bg=SECONDARY_COLOR,
            fg=WHITE,
            pady=8,
        )
        counter_label.pack()

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=30)

        # Card da pergunta
        question_card = tk.Frame(content, bg=ACCENT_COLOR, relief="flat")
        question_card.pack(fill="both", expand=True, pady=20)

        question_inner = tk.Frame(question_card, bg=ACCENT_COLOR)
        question_inner.pack(fill="both", expand=True, padx=40, pady=40)

        question_label = tk.Label(
            question_inner,
            text=question["texto"],
            font=("Segoe UI", FONT_SIZES["header"], "bold"),
            bg=ACCENT_COLOR,
            fg=WHITE,
            wraplength=850,
            justify="center",
        )
        question_label.pack(fill="both", expand=True)

        # Botões de resposta
        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=25, fill="x", padx=60)

        yes_btn = UIHelper.create_button(
            btn_frame,
            "Sim",
            lambda: self.answer(True),
            SUCCESS_COLOR,
        )
        yes_btn.pack(side="left", padx=10, fill="x", expand=True)

        no_btn = UIHelper.create_button(
            btn_frame,
            "Não",
            lambda: self.answer(False),
            DANGER_COLOR,
        )
        no_btn.pack(side="left", padx=15, fill="x", expand=True)

        # Botão voltar ao menu (confirma antes)
        back_frame = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        back_frame.pack(fill="x", padx=40, pady=(0, 15))

        back_btn = UIHelper.create_button(
            back_frame,
            "Cancelar Avaliação",
            self.confirm_cancel_assessment,
            ACCENT_COLOR,
        )
        back_btn.pack(fill="x")

    def confirm_cancel_assessment(self):
        """Confirma se o usuário deseja realmente cancelar"""
        self.clear_frame()

        UIHelper.create_header(
            self.main_frame,
            "Confirmar Cancelamento",
            "Tem certeza que deseja cancelar esta avaliação?",
            DANGER_COLOR,
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=50, pady=50)

        warning_card = tk.Frame(content, bg=WARNING_COLOR, relief="flat")
        warning_card.pack(fill="x", pady=20)

        warning_inner = tk.Frame(warning_card, bg=WARNING_COLOR)
        warning_inner.pack(padx=40, pady=30)

        warning_text = tk.Label(
            warning_inner,
            text="ATENÇÃO: Todos os dados desta avaliação serão perdidos.\n"
            "Esta ação não pode ser desfeita.",
            font=("Segoe UI", FONT_SIZES["body"], "bold"),
            bg=WARNING_COLOR,
            fg=WHITE,
            justify="center",
        )
        warning_text.pack()

        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=30, fill="x", padx=50)

        cancel_btn = UIHelper.create_button(
            btn_frame,
            "Sim, Cancelar",
            self.show_menu,
            DANGER_COLOR,
        )
        cancel_btn.pack(side="left", padx=10, fill="x", expand=True)

        continue_btn = UIHelper.create_button(
            btn_frame,
            "Não, Continuar Avaliação",
            self.display_question,
            SUCCESS_COLOR,
        )
        continue_btn.pack(side="left", padx=10, fill="x", expand=True)

    def answer(self, response):
        """Processa uma resposta"""
        # Converter boolean para string "sim"/"nao"
        response_str = "sim" if response else "nao"
        has_more = self.question_manager.answer_question(response_str)

        if has_more:
            self.display_question()
        else:
            self.ask_patient_name()

    def ask_patient_name(self):
        """Solicita o nome do paciente antes de mostrar os resultados"""
        self.clear_frame()
        self.current_screen = "patient_name"

        UIHelper.create_header(
            self.main_frame,
            "Questionário Completo",
            "Por favor, informe o nome do paciente",
            SECONDARY_COLOR,
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=20)

        instruction_label = UIHelper.create_label_with_icon(
            content,
            "Nome do Paciente:",
            "user",
            ("Segoe UI", FONT_SIZES["header"]),
            PRIMARY_COLOR,
            WHITE,
        )
        instruction_label.pack(pady=(20, 10))

        # Campo de entrada para o nome
        self.name_entry = tk.Entry(
            content,
            font=("Segoe UI", FONT_SIZES["body"]),
            bg=LIGHT_BG,
            fg=DARK_TEXT,
            relief="flat",
            justify="center",
        )
        self.name_entry.pack(pady=10, ipady=12, fill="x", padx=100)
        self.name_entry.focus()

        # Permitir pressionar Enter para continuar
        self.name_entry.bind("<Return>", lambda e: self.save_name_and_show_results())

        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=30, fill="x")

        continue_btn = UIHelper.create_button(
            btn_frame,
            "Salvar e Continuar",
            self.save_name_and_show_results,
            SUCCESS_COLOR,
        )
        continue_btn.pack(fill="x", padx=100)

        skip_btn = UIHelper.create_button(
            btn_frame, "Continuar Anônimo", lambda: self.show_results("Anônimo"), BLUE
        )
        skip_btn.pack(fill="x", padx=100, pady=(10, 0))

    def save_name_and_show_results(self):
        """Salva o nome do paciente e mostra os resultados"""
        patient_name = self.name_entry.get().strip()
        if not patient_name:
            patient_name = "Anônimo"
        self.show_results(patient_name)

    def show_history_details(self, index):
        """Exibe detalhes de uma avaliação do histórico"""
        self.clear_frame()
        self.current_screen = "history_details"

        assessment = self.history_manager.get_assessment(index)
        if not assessment:
            self.show_history()
            return

        # Nome do paciente
        patient_name = assessment.get("patient_name", "Anônimo")

        # Header
        UIHelper.create_header(
            self.main_frame,
            f"Detalhes da Avaliação #{index + 1}",
            f"Paciente: {patient_name} | Data: {assessment['data']} | Nível: {assessment['level']}",
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

        # Habilitar scroll com mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

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

        # Cleanup do evento quando sair da tela
        def cleanup():
            canvas.unbind_all("<MouseWheel>")

        self.bind("<Destroy>", lambda e: cleanup())

    def show_results(self, patient_name="Anônimo"):
        """Exibe o resultado final - design profissional otimizado para projeção"""
        self.clear_frame()
        self.current_screen = "results"

        risk_level = get_risk_level(self.question_manager.score)
        color = LEVEL_COLORS.get(risk_level, SUCCESS_COLOR)
        icon = LEVEL_ICONS.get(risk_level, "●")

        # Header com cor do nível de risco
        UIHelper.create_header(
            self.main_frame,
            "Avaliação Concluída",
            "Resultado da Avaliação de Risco",
            color,
        )

        content = tk.Frame(self.main_frame, bg=PRIMARY_COLOR)
        content.pack(fill="both", expand=True, padx=50, pady=20)

        # Card do paciente
        patient_card = tk.Frame(content, bg=SECONDARY_COLOR, relief="flat")
        patient_card.pack(fill="x", pady=(0, 20))

        patient_inner = tk.Frame(patient_card, bg=SECONDARY_COLOR)
        patient_inner.pack(padx=40, pady=25)

        patient_label = UIHelper.create_label_with_icon(
            patient_inner,
            f"Paciente: {patient_name}",
            "user",
            ("Segoe UI", FONT_SIZES["title"], "bold"),
            SECONDARY_COLOR,
            WHITE,
        )
        patient_label.pack()

        # Card de resultado principal (grande e destacado)
        result_card = tk.Frame(content, bg=color, relief="flat")
        result_card.pack(fill="x", pady=20)

        result_inner = tk.Frame(result_card, bg=color)
        result_inner.pack(padx=50, pady=40)

        # Nível de risco em destaque
        level_label = tk.Label(
            result_inner,
            text=f"{icon}  NÍVEL DE RISCO: {risk_level.upper()}",
            font=("Segoe UI", 36, "bold"),
            bg=color,
            fg=WHITE,
        )
        level_label.pack(pady=(0, 15))

        # Pontuação
        score_label = tk.Label(
            result_inner,
            text=f"Pontuação Total: {self.question_manager.score} pontos",
            font=("Segoe UI", FONT_SIZES["header"], "bold"),
            bg=color,
            fg=WHITE,
        )
        score_label.pack()

        # Aviso importante profissional
        note_card = tk.Frame(content, bg=SECONDARY_COLOR, relief="flat")
        note_card.pack(fill="x", pady=20)

        note_inner = tk.Frame(note_card, bg=SECONDARY_COLOR)
        note_inner.pack(padx=40, pady=30)

        note_title = tk.Label(
            note_inner,
            text="AVISO IMPORTANTE",
            font=("Segoe UI", FONT_SIZES["header"], "bold"),
            bg=SECONDARY_COLOR,
            fg=WARNING_COLOR,
        )
        note_title.pack(pady=(0, 12))

        note_label = tk.Label(
            note_inner,
            text="Esta avaliação é uma ferramenta de triagem e os resultados podem apresentar variações.\n\n"
            "A interpretação clínica deve considerar idade, contexto e histórico individual.\n\n"
            "Este instrumento NÃO substitui a avaliação de um profissional de saúde qualificado.",
            font=("Segoe UI", FONT_SIZES["label"]),
            bg=SECONDARY_COLOR,
            fg=LIGHT_BG,
            justify="center",
            wraplength=850,
        )
        note_label.pack()

        # Salvar no histórico
        assessment_data = {
            "patient_name": patient_name,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "level": risk_level,
            "score": self.question_manager.score,
            "responses": self.question_manager.responses,
        }
        self.history_manager.add_assessment(assessment_data)

        # Botões de ação
        btn_frame = tk.Frame(content, bg=PRIMARY_COLOR)
        btn_frame.pack(pady=35, fill="x", padx=60)

        again_btn = UIHelper.create_button(
            btn_frame,
            "Nova Avaliação",
            self.show_menu,
            SUCCESS_COLOR,
        )
        again_btn.pack(side="left", padx=10, fill="x", expand=True)

        hist_btn = UIHelper.create_button(
            btn_frame, "Ver Histórico", self.show_history, INDIGO
        )
        hist_btn.pack(side="left", padx=15, fill="x", expand=True)


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()
