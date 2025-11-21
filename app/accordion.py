"""
Componente Acordeon para PyQt6.
Exibe eixos temáticos com contagem de respostas sim/não.
"""

from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont
from config import (
    SECONDARY_COLOR,
    PRIMARY_COLOR,
    ACCENT_COLOR,
    DARK_TEXT,
    LIGHT_BG,
    BORDER_COLOR,
)


class AccordionItem(QFrame):
    """Item de acordeon com header e conteúdo expansível."""

    response_changed = pyqtSignal(int, str)  # resposta_id, novo_valor

    def __init__(self, eixo_nome, respostas, db, parent=None, avaliacao_id=None):
        super().__init__(parent)
        self.eixo_nome = eixo_nome
        self.respostas = respostas
        self.db = db
        self.avaliacao_id = avaliacao_id
        self.is_expanded = False
        self.content_widget = None

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: transparent;
                border-radius: 0px;
                border: none;
                margin: 4px 0px;
            }}
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header do acordeon
        self.header = self._create_header()
        layout.addWidget(self.header)

        # Conteúdo (inicialmente vazio, criado ao expandir)
        self.content_container = QFrame()
        self.content_container.setStyleSheet(
            "background-color: transparent; border: none;"
        )
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_container.setLayout(self.content_layout)
        self.content_container.setMaximumHeight(0)  # Inicialmente colapsado

        layout.addWidget(self.content_container)
        self.setLayout(layout)

    def _create_header(self):
        header = QFrame()
        header.setStyleSheet(
            f"""
            QFrame {{
                background-color: {SECONDARY_COLOR};
                border-radius: 6px;
                padding: 10px 14px;
                border: none;
            }}
        """
        )
        header.setCursor(Qt.CursorShape.PointingHandCursor)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Seta de expansão (SVG simples em texto)
        self.arrow_label = QLabel("▶")
        self.arrow_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; font-size: 12px; font-weight: bold; text-align: center;"
        )
        self.arrow_label.setMaximumWidth(16)
        header_layout.addWidget(self.arrow_label)

        # Nome do eixo
        eixo_label = QLabel(self.eixo_nome)
        eixo_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; font-size: 14px; font-weight: 600; font-family: 'Poppins';"
        )
        header_layout.addWidget(eixo_label, 1)

        # Contagem de respostas (sem emojis)
        contagem = self.db.get_contagem_respostas(
            self.eixo_nome, avaliacao_id=self.avaliacao_id
        )
        sim_count = contagem.get("sim", 0)
        nao_count = contagem.get("nao", 0)

        count_label = QLabel(f"[✓ {sim_count}  ✗ {nao_count}]")
        count_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; font-size: 12px; font-weight: 600; font-family: 'Poppins';"
        )
        count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_label = count_label  # Guardar referência para atualizar depois
        header_layout.addWidget(count_label, 0)

        header.setLayout(header_layout)

        # Tornar clicável
        header.mousePressEvent = lambda e: self.toggle()

        return header

    def toggle(self):
        """Expande ou colapa o acordeon."""
        if not self.is_expanded:
            self.expand()
        else:
            self.collapse()

    def expand(self):
        """Expande o acordeon."""
        if self.is_expanded:
            return

        self.is_expanded = True
        self.arrow_label.setText("▼")

        # Criar conteúdo se não existir
        if not self.content_widget:
            self._create_content()

        # Animar expansão
        self.content_container.setMaximumHeight(2000)  # Altura grande o suficiente

    def collapse(self):
        """Colapa o acordeon."""
        if not self.is_expanded:
            return

        self.is_expanded = False
        self.arrow_label.setText("▶")
        self.content_container.setMaximumHeight(0)

    def _create_content(self):
        """Cria o widget de conteúdo com as perguntas."""
        # Limpar layout anterior
        while self.content_layout.count():
            self.content_layout.takeAt(0).widget().deleteLater()

        # Container do conteúdo
        self.content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(16, 12, 16, 12)
        content_layout.setSpacing(10)

        if not self.respostas:
            label = QLabel("Nenhuma resposta registrada ainda")
            label.setStyleSheet(
                f"color: #999; font-size: 12px; font-family: 'Poppins';"
            )
            content_layout.addWidget(label)
        else:
            for resposta in self.respostas:
                question_item = self._create_question_item(resposta)
                content_layout.addWidget(question_item)

        content_layout.addStretch()
        self.content_widget.setLayout(content_layout)
        self.content_layout.addWidget(self.content_widget)

    def _create_question_item(self, resposta):
        """Cria um item de pergunta com checkbox para alterar resposta."""
        item = QFrame()
        item.setStyleSheet(
            f"""
            QFrame {{
                background-color: {PRIMARY_COLOR};
                border-radius: 4px;
                padding: 8px 10px;
            }}
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Texto da pergunta
        pergunta_label = QLabel(resposta["pergunta_texto"])
        pergunta_label.setStyleSheet(
            f"color: {DARK_TEXT}; font-size: 12px; font-weight: 600; font-family: 'Poppins'; line-height: 1.3;"
        )
        pergunta_label.setWordWrap(True)
        layout.addWidget(pergunta_label)

        # Checkboxes para resposta
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(12)

        resposta_atual = resposta.get("resposta", "").lower()

        # Checkbox SIM (verde quando marcado)
        sim_checkbox = QCheckBox("✓ Sim")
        sim_checkbox.setChecked(resposta_atual == "sim")
        sim_color = "#16A34A" if resposta_atual == "sim" else DARK_TEXT
        sim_checkbox.setStyleSheet(
            f"QCheckBox {{ color: {sim_color}; font-size: 11px; font-weight: {'bold' if resposta_atual == 'sim' else 'normal'}; font-family: 'Poppins'; }}"
        )
        sim_checkbox.stateChanged.connect(
            lambda: self._on_response_changed(
                resposta["id"], "sim", sim_checkbox, nao_checkbox
            )
        )
        checkbox_layout.addWidget(sim_checkbox)

        # Checkbox NÃO (vermelho quando marcado)
        nao_checkbox = QCheckBox("✗ Não")
        nao_checkbox.setChecked(resposta_atual == "nao")
        nao_color = "#DC2626" if resposta_atual == "nao" else DARK_TEXT
        nao_checkbox.setStyleSheet(
            f"QCheckBox {{ color: {nao_color}; font-size: 11px; font-weight: {'bold' if resposta_atual == 'nao' else 'normal'}; font-family: 'Poppins'; }}"
        )
        nao_checkbox.stateChanged.connect(
            lambda: self._on_response_changed(
                resposta["id"], "nao", sim_checkbox, nao_checkbox
            )
        )
        checkbox_layout.addWidget(nao_checkbox)

        checkbox_layout.addStretch()
        layout.addLayout(checkbox_layout)

        item.setLayout(layout)
        return item

    def _on_response_changed(self, resposta_id, novo_valor, sim_cb, nao_cb):
        """Callback ao alterar resposta."""
        # Desbloquear sinais para evitar loops
        sim_cb.blockSignals(True)
        nao_cb.blockSignals(True)

        if novo_valor == "sim":
            sim_cb.setChecked(True)
            nao_cb.setChecked(False)
            # Verde para SIM marcado
            sim_cb.setStyleSheet(
                f"QCheckBox {{ color: #16A34A; font-size: 11px; font-weight: bold; font-family: 'Poppins'; }}"
            )
            # Cinza para NÃO desmarcado
            nao_cb.setStyleSheet(
                f"QCheckBox {{ color: {DARK_TEXT}; font-size: 11px; font-weight: normal; font-family: 'Poppins'; }}"
            )
        else:
            sim_cb.setChecked(False)
            nao_cb.setChecked(True)
            # Cinza para SIM desmarcado
            sim_cb.setStyleSheet(
                f"QCheckBox {{ color: {DARK_TEXT}; font-size: 11px; font-weight: normal; font-family: 'Poppins'; }}"
            )
            # Vermelho para NÃO marcado
            nao_cb.setStyleSheet(
                f"QCheckBox {{ color: #DC2626; font-size: 11px; font-weight: bold; font-family: 'Poppins'; }}"
            )

        sim_cb.blockSignals(False)
        nao_cb.blockSignals(False)

        # Atualizar no banco de dados
        self.db.update_resposta(resposta_id, novo_valor)

        # Atualizar contagem no header
        self.update_count()

        # Emitir sinal
        self.response_changed.emit(resposta_id, novo_valor)

    def update_count(self):
        """Atualiza a contagem de respostas no header."""
        contagem = self.db.get_contagem_respostas(
            self.eixo_nome, avaliacao_id=self.avaliacao_id
        )
        sim_count = contagem.get("sim", 0)
        nao_count = contagem.get("nao", 0)
        self.count_label.setText(f"[✓ {sim_count}  ✗ {nao_count}]")


class AccordionWidget(QWidget):
    """Widget container com múltiplos acordeons (um por eixo)."""

    def __init__(self, db, eixos, parent=None, avaliacao_id=None):
        super().__init__(parent)
        self.db = db
        self.eixos = eixos
        self.avaliacao_id = avaliacao_id
        self.acordeons = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Criar um acordeon para cada eixo
        for eixo_nome in eixos:
            respostas = self.db.get_respostas_by_eixo(
                eixo_nome, avaliacao_id=avaliacao_id
            )
            acordeon = AccordionItem(
                eixo_nome, respostas, self.db, avaliacao_id=avaliacao_id
            )
            self.acordeons.append(acordeon)
            layout.addWidget(acordeon)

        layout.addStretch()
        self.setLayout(layout)

    def refresh_all(self):
        """Atualiza todos os acordeons com dados do BD."""
        for acordeon in self.acordeons:
            acordeon.respostas = self.db.get_respostas_by_eixo(
                acordeon.eixo_nome, avaliacao_id=self.avaliacao_id
            )
            acordeon.update_count()
            if acordeon.is_expanded and acordeon.content_widget:
                acordeon._create_content()
