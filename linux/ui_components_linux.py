"""
Módulo de componentes UI para Linux (PySide6).
"""

from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

from config import PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, LIGHT_BG, WHITE


class UIHelper:
    """Classe auxiliar para criação de componentes UI - Linux."""

    @staticmethod
    def create_button(text, command, bg_color):
        """Cria um botão estilizado para Linux."""
        btn = QPushButton(text)
        btn.setFont(QFont("Ubuntu", 11, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(command)
        btn.setMinimumHeight(50)
        btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {bg_color};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {UIHelper._darken_color(bg_color)};
            }}
            QPushButton:pressed {{
                background-color: {UIHelper._darken_color(bg_color, 40)};
            }}
        """
        )
        return btn

    @staticmethod
    def _darken_color(color, amount=20):
        """Escurece uma cor hexadecimal."""
        color = color.lstrip("#")
        darkened = "#" + "".join(
            hex(max(0, int(color[i : i + 2], 16) - amount))[2:].zfill(2)
            for i in (0, 2, 4)
        )
        return darkened

    @staticmethod
    def create_header(title, subtitle="", bg_color=SECONDARY_COLOR):
        """Cria um header com título - Linux."""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setFont(QFont("Ubuntu", 20, QFont.Weight.Bold))
        title_label.setStyleSheet(
            f"color: {WHITE}; background-color: {bg_color}; padding: 15px;"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Ubuntu", 10))
            subtitle_label.setStyleSheet(
                f"color: {LIGHT_BG}; background-color: {bg_color}; padding: 5px;"
            )
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(subtitle_label)

        header.setStyleSheet(f"background-color: {bg_color};")
        return header

    @staticmethod
    def create_progress_bar(progress_percentage):
        """Cria uma barra de progresso - Linux."""
        progress_frame = QFrame()
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        # Barra de progresso simplificada com QFrame
        bar = QFrame()
        bar.setMinimumHeight(6)
        bar.setMaximumHeight(6)

        width_pct = int((progress_percentage / 100) * 100)
        bar.setStyleSheet(
            f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27AE60, stop:{progress_percentage/100:.2f} #27AE60, stop:1 #ECF0F1);
                border: none;
            }}
        """
        )
        progress_layout.addWidget(bar)

        progress_frame.setStyleSheet(f"background-color: {LIGHT_BG};")
        return progress_frame


class HistoryCardWidget:
    """Widget para exibir um card de histórico - Linux."""

    @staticmethod
    def create_card(number, data, on_view_details=None):
        """Cria um card de histórico."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {LIGHT_BG};
                border-radius: 5px;
                padding: 10px;
            }}
        """
        )
        card.setMinimumHeight(70)

        card_layout = QHBoxLayout(card)
        card_layout.setSpacing(5)

        # Informações
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)

        info_text = f"Avaliação #{number} - {data['data']}"
        info_label = QLabel(info_text)
        info_label.setFont(QFont("Ubuntu", 11, QFont.Weight.Bold))
        info_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; background-color: transparent;"
        )
        info_layout.addWidget(info_label)

        result_text = f"Nível: {data['level']} | Score: {data['score']}"
        result_label = QLabel(result_text)
        result_label.setFont(QFont("Ubuntu", 10))
        result_label.setStyleSheet(f"color: #7F8C8D; background-color: transparent;")
        info_layout.addWidget(result_label)

        card_layout.addWidget(info_widget)

        # Botão para ver detalhes
        if on_view_details:
            details_btn = UIHelper.create_button(
                "Ver Detalhes →", lambda: on_view_details(number - 1), SECONDARY_COLOR
            )
            details_btn.setMaximumWidth(150)
            card_layout.addWidget(details_btn)

        return card
