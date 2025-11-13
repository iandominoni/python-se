import tkinter as tk
from tkinter import font as tkfont
import random
from config import *


class RoundedButton(tk.Canvas):

    def __init__(
        self,
        parent,
        text,
        command,
        bg_color,
        hover_color=None,
        fg_color=WHITE,
        font_tuple=None,
        width=250,
        height=60,
        corner_radius=15,
        **kwargs,
    ):
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color or UIHelper.lighten_color(bg_color, 15)
        self.fg_color = fg_color
        self.font_tuple = font_tuple or ("Segoe UI", FONT_SIZES["button"], "bold")
        self.corner_radius = corner_radius
        self.is_hover = False
        self.width = width
        self.height = height

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            relief="flat",
            bd=0,
            **kwargs,
        )

        # Bind de eventos
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event=None):
        """Redesenha o botão quando redimensionado."""
        self.draw_button()

    def draw_button(self):
        """Desenha o botão com bordas arredondadas."""
        self.delete("all")

        # Obter dimensões
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Cores
        current_bg = self.hover_color if self.is_hover else self.bg_color

        # Desenhar retângulo arredondado
        self._draw_rounded_rect(
            2,
            2,
            width - 2,
            height - 2,
            radius=self.corner_radius,
            fill=current_bg,
            outline="",
        )

        # Desenhar texto
        center_x = width / 2
        center_y = height / 2
        self.create_text(
            center_x,
            center_y,
            text=self.text,
            fill=self.fg_color,
            font=self.font_tuple,
            width=width - 40,
        )

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        """Desenha um retângulo com cantos arredondados."""
        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_click(self, event):
        """Executa o comando ao clicar."""
        if self.command:
            self.command()

    def _on_enter(self, event):
        """Efeito ao passar do mouse."""
        self.is_hover = True
        self.draw_button()
        self.config(cursor="hand2")

    def _on_leave(self, event):
        """Remove efeito ao sair do mouse."""
        self.is_hover = False
        self.draw_button()
        self.config(cursor="arrow")

    def pack(self, **kwargs):
        """Override do pack para manter tamanho do canvas."""
        kwargs.setdefault("padx", 10)
        kwargs.setdefault("pady", 10)
        super().pack(**kwargs)


class UIHelper:
    @staticmethod
    def create_button(parent, text, command, bg_color, hover_color=None, icon=None):
        """Cria um botão com bordas arredondadas."""
        btn = RoundedButton(
            parent,
            text=text,
            command=command,
            bg_color=bg_color,
            hover_color=hover_color or UIHelper.lighten_color(bg_color, 15),
            fg_color=WHITE,
            font_tuple=("Segoe UI", FONT_SIZES["button"], "bold"),
            width=250,
            height=60,
            corner_radius=15,
        )
        btn.pack(padx=10, pady=10, fill="x", expand=False)
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

        # Título com fundo branco
        title_frame = tk.Frame(content_frame, bg=WHITE)
        title_frame.pack(padx=10, pady=5)
        title_label = tk.Label(
            title_frame,
            text=title,
            font=("Segoe UI", FONT_SIZES["title"], "bold"),
            bg=WHITE,
            fg=DARK_TEXT,
            padx=20,
            pady=10,
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
        progress_container = tk.Frame(parent, bg=LIGHT_BG)
        progress_container.pack(fill="x", pady=8)
        bg_bar = tk.Frame(progress_container, bg="#e0e0e0", height=16)
        bg_bar.pack(fill="x", padx=30, pady=12)
        parent.update_idletasks()
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 950
        progress_width = (progress_percentage / 100) * (parent_width - 60)
        bar_color = (
            ACCENT_COLOR
            if progress_percentage < 33
            else SECONDARY_COLOR if progress_percentage < 66 else SECONDARY_COLOR
        )
        progress_fill = tk.Frame(bg_bar, bg=bar_color, height=16)
        progress_fill.place(x=0, y=0, width=max(4, progress_width), height=16)
        if show_text:
            percentage_label = tk.Label(
                progress_container,
                text=f"{int(progress_percentage)}% Concluído",
                font=("Segoe UI", FONT_SIZES["label"], "bold"),
                bg=LIGHT_BG,
                fg=DARK_TEXT,
            )
            percentage_label.pack(pady=(0, 8))

    @staticmethod
    def create_stat_card(parent, label, value, icon="", color=PURPLE):
        card = tk.Frame(
            parent, bg=color, relief="raised", borderwidth=1, highlightthickness=0
        )
        card.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        inner = tk.Frame(card, bg=color)
        inner.pack(fill="both", expand=True, padx=16, pady=16)
        value_label = tk.Label(
            inner, text=str(value), font=("Segoe UI", 24, "bold"), bg=color, fg=WHITE
        )
        value_label.pack(pady=5)
        label_label = tk.Label(
            inner,
            text=label,
            font=("Segoe UI", FONT_SIZES["label"] - 2),
            bg=color,
            fg=WHITE,
            pady=4,
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

        card_container = tk.Frame(
            parent, bg=LIGHT_BG, relief="raised", borderwidth=1, highlightthickness=0
        )
        card_container.pack(fill="x", pady=12, padx=15)

        side_bar = tk.Frame(card_container, bg=level_color, width=6)
        side_bar.pack(side="left", fill="y")

        card = tk.Frame(
            card_container,
            bg=LIGHT_BG,
            relief="raised",
            borderwidth=1,
            highlightthickness=0,
        )
        card.pack(side="left", fill="both", expand=True)

        info_frame = tk.Frame(card, bg=LIGHT_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=25, pady=20)

        patient_name = data.get("patient_name", "Paciente sem nome")
        patient_label = tk.Label(
            info_frame,
            text=patient_name,
            font=("Segoe UI", FONT_SIZES["header"], "bold"),
            bg=LIGHT_BG,
            fg=DARK_TEXT,
        )
        patient_label.pack(anchor="w", pady=(0, 8))

        info_text = f"Avaliação #{number}  •  {data['data']}"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", FONT_SIZES["label"]),
            bg=LIGHT_BG,
            fg="#999999",
        )
        info_label.pack(anchor="w", pady=3)

        result_text = f"{level_icon}  {level}  •  {data['score']} pontos"
        result_label = tk.Label(
            info_frame,
            text=result_text,
            font=("Segoe UI", FONT_SIZES["body"], "bold"),
            bg=LIGHT_BG,
            fg=level_color,
        )
        result_label.pack(anchor="w", pady=3)

        if on_view_details:
            btn_frame = tk.Frame(card, bg=LIGHT_BG)
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
