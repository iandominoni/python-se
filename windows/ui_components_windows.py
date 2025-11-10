"""
Módulo de componentes UI para Windows (Tkinter).
"""

import tkinter as tk
from config import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    LIGHT_BG,
    WHITE,
)


class UIHelper:
    """Classe auxiliar para criação de componentes UI - Windows."""

    @staticmethod
    def create_button(parent, text, command, bg_color):
        """Cria um botão estilizado para Windows."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=WHITE,
            font=("Segoe UI", 11, "bold"),
            border=0,
            padx=20,
            pady=12,
            activebackground=UIHelper.darken_color(bg_color),
            activeforeground=WHITE,
            cursor="hand2",
        )
        return btn

    @staticmethod
    def darken_color(color):
        """Escurece uma cor hexadecimal."""
        color = color.lstrip("#")
        return "#" + "".join(
            hex(max(0, int(color[i : i + 2], 16) - 20))[2:].zfill(2) for i in (0, 2, 4)
        )

    @staticmethod
    def create_header(parent, title, subtitle=None, bg_color=SECONDARY_COLOR):
        """Cria um header com título - Windows."""
        header = tk.Frame(parent, bg=bg_color, height=70)
        header.pack(fill="x")

        title_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 20, "bold"),
            bg=bg_color,
            fg=WHITE,
            pady=10,
        )
        title_label.pack()

        if subtitle:
            subtitle_label = tk.Label(
                header,
                text=subtitle,
                font=("Segoe UI", 10),
                bg=bg_color,
                fg=LIGHT_BG,
                pady=5,
            )
            subtitle_label.pack()

    @staticmethod
    def create_progress_bar(parent, progress_percentage):
        """Cria uma barra de progresso - Windows."""
        progress_bar = tk.Frame(parent, bg=LIGHT_BG, height=6)
        progress_bar.pack(fill="x")
        progress_bar.update_idletasks()

        parent_width = parent.winfo_width()
        if parent_width <= 1:
            parent_width = 800  # Valor padrão se ainda não foi renderizado

        progress_width = (progress_percentage / 100) * parent_width
        progress_fill = tk.Frame(
            progress_bar, bg=SUCCESS_COLOR, height=6, width=progress_width
        )
        progress_fill.place(x=0, y=0, width=progress_width, height=6)


class HistoryCardWidget:
    """Widget para exibir um card de histórico - Windows."""

    @staticmethod
    def create_card(parent, number, data, on_view_details=None):
        """Cria um card de histórico."""
        card = tk.Frame(parent, bg=LIGHT_BG, relief="flat")
        card.pack(fill="x", pady=10, padx=5)

        info_frame = tk.Frame(card, bg=LIGHT_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        info_text = f"Avaliação #{number} - {data['data']}"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 11, "bold"),
            bg=LIGHT_BG,
            fg=PRIMARY_COLOR,
        )
        info_label.pack(anchor="w")

        result_text = f"Nível: {data['level']} | Score: {data['score']}"
        result_label = tk.Label(
            info_frame,
            text=result_text,
            font=("Segoe UI", 10),
            bg=LIGHT_BG,
            fg="#7F8C8D",
        )
        result_label.pack(anchor="w")

        # Botão para ver detalhes
        if on_view_details:
            btn_frame = tk.Frame(card, bg=LIGHT_BG)
            btn_frame.pack(side="right", padx=10, pady=10)

            details_btn = tk.Button(
                btn_frame,
                text="Ver Detalhes →",
                command=lambda: on_view_details(number - 1),
                bg=SECONDARY_COLOR,
                fg=WHITE,
                font=("Segoe UI", 9, "bold"),
                border=0,
                padx=12,
                pady=6,
                cursor="hand2",
            )
            details_btn.pack()

        return card
