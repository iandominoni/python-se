"""UI Components - Design Profissional Minimalista sem Ícones."""

import tkinter as tk
from tkinter import font as tkfont
import random
from config import *


class UIHelper:
    @staticmethod
    def create_button(parent, text, command, bg_color, hover_color=None, icon=None):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=WHITE,
            font=("Segoe UI", FONT_SIZES["button"], "bold"),
            border=0,
            padx=40,
            pady=20,
            cursor="hand2",
            relief="flat",
        )
        btn.pack()

        def on_enter(e):
            btn.configure(bg=hover_color or UIHelper.lighten_color(bg_color, 15))

        def on_leave(e):
            btn.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    @staticmethod
    def lighten_color(color, amount=20):
        color = color.lstrip("#")
        return "#" + "".join(
            hex(min(255, int(color[i : i + 2], 16) + amount))[2:].zfill(2)
            for i in (0, 2, 4)
        )

    @staticmethod
    def darken_color(color, amount=15):
        color = color.lstrip("#")
        return "#" + "".join(
            hex(max(0, int(color[i : i + 2], 16) - amount))[2:].zfill(2)
            for i in (0, 2, 4)
        )

    @staticmethod
    def create_header(
        parent, title, subtitle=None, bg_color=SECONDARY_COLOR, icon=None
    ):
        header = tk.Frame(parent, bg=bg_color, height=120)
        header.pack(fill="x")
        content_frame = tk.Frame(header, bg=bg_color)
        content_frame.pack(expand=True, pady=20)
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Segoe UI", FONT_SIZES["title"], "bold"),
            bg=bg_color,
            fg=WHITE,
        )
        title_label.pack()
        if subtitle:
            subtitle_label = tk.Label(
                content_frame,
                text=subtitle,
                font=("Segoe UI", FONT_SIZES["subtitle"]),
                bg=bg_color,
                fg=LIGHT_BG,
                pady=8,
            )
            subtitle_label.pack()

    @staticmethod
    def create_progress_bar(parent, progress_percentage, show_text=True):
        progress_container = tk.Frame(parent, bg=SECONDARY_COLOR)
        progress_container.pack(fill="x", pady=8)
        bg_bar = tk.Frame(progress_container, bg=ACCENT_COLOR, height=16)
        bg_bar.pack(fill="x", padx=30, pady=12)
        parent.update_idletasks()
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 950
        progress_width = (progress_percentage / 100) * (parent_width - 60)
        bar_color = (
            INDIGO
            if progress_percentage < 33
            else BLUE if progress_percentage < 66 else SUCCESS_COLOR
        )
        progress_fill = tk.Frame(bg_bar, bg=bar_color, height=16)
        progress_fill.place(x=0, y=0, width=max(4, progress_width), height=16)
        if show_text:
            percentage_label = tk.Label(
                progress_container,
                text=f"{int(progress_percentage)}% Concluído",
                font=("Segoe UI", FONT_SIZES["label"], "bold"),
                bg=SECONDARY_COLOR,
                fg=WHITE,
            )
            percentage_label.pack(pady=(0, 8))

    @staticmethod
    def create_stat_card(parent, label, value, icon="", color=PURPLE):
        card = tk.Frame(parent, bg=color, relief="flat", borderwidth=0)
        card.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        inner = tk.Frame(card, bg=color)
        inner.pack(fill="both", expand=True, padx=12, pady=12)
        value_label = tk.Label(
            inner, text=str(value), font=("Segoe UI", 22, "bold"), bg=color, fg=WHITE
        )
        value_label.pack(pady=3)
        label_label = tk.Label(
            inner,
            text=label,
            font=("Segoe UI", FONT_SIZES["label"] - 3),
            bg=color,
            fg=LIGHT_BG,
            pady=3,
        )
        label_label.pack()
        return card

    @staticmethod
    def get_random_motivational_message():
        return random.choice(MOTIVATIONAL_MESSAGES)

    @staticmethod
    def create_label_with_icon(
        parent, text, icon_key, font_tuple, bg_color, fg_color, **kwargs
    ):
        return tk.Label(
            parent, text=text, font=font_tuple, bg=bg_color, fg=fg_color, **kwargs
        )


class HistoryCardWidget:
    @staticmethod
    def create_card(parent, number, data, on_view_details=None):
        level = data.get("level", "Baixo")
        level_color = LEVEL_COLORS.get(level, PURPLE)
        level_icon = LEVEL_ICONS.get(level, "●")

        card_container = tk.Frame(parent, bg=PRIMARY_COLOR, relief="flat")
        card_container.pack(fill="x", pady=10, padx=15)

        side_bar = tk.Frame(card_container, bg=level_color, width=6)
        side_bar.pack(side="left", fill="y")

        card = tk.Frame(card_container, bg=SECONDARY_COLOR, relief="flat")
        card.pack(side="left", fill="both", expand=True)

        info_frame = tk.Frame(card, bg=SECONDARY_COLOR)
        info_frame.pack(side="left", fill="both", expand=True, padx=25, pady=20)

        patient_name = data.get("patient_name", "Paciente sem nome")
        patient_label = tk.Label(
            info_frame,
            text=patient_name,
            font=("Segoe UI", FONT_SIZES["header"], "bold"),
            bg=SECONDARY_COLOR,
            fg=WHITE,
        )
        patient_label.pack(anchor="w", pady=(0, 8))

        info_text = f"Avaliação #{number}  •  {data['data']}"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", FONT_SIZES["label"]),
            bg=SECONDARY_COLOR,
            fg=LIGHT_BG,
        )
        info_label.pack(anchor="w", pady=3)

        result_text = f"{level_icon}  {level}  •  {data['score']} pontos"
        result_label = tk.Label(
            info_frame,
            text=result_text,
            font=("Segoe UI", FONT_SIZES["body"], "bold"),
            bg=SECONDARY_COLOR,
            fg=level_color,
        )
        result_label.pack(anchor="w", pady=3)

        if on_view_details:
            btn_frame = tk.Frame(card, bg=SECONDARY_COLOR)
            btn_frame.pack(side="right", padx=20, pady=20)
            details_btn = tk.Button(
                btn_frame,
                text="Ver Detalhes  →",
                command=lambda: on_view_details(number - 1),
                bg=level_color,
                fg=WHITE,
                font=("Segoe UI", FONT_SIZES["label"], "bold"),
                border=0,
                padx=20,
                pady=12,
                cursor="hand2",
                relief="flat",
            )
            details_btn.pack()

            def on_enter(e):
                details_btn.configure(bg=UIHelper.lighten_color(level_color))

            def on_leave(e):
                details_btn.configure(bg=level_color)

            details_btn.bind("<Enter>", on_enter)
            details_btn.bind("<Leave>", on_leave)

        return card_container
