from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os


class PDFGenerator:
    """Gerador de PDFs para prontuários de pacientes."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Configura estilos customizados para o PDF."""
        # Estilo para título
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#0D7377"),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Estilo para subtítulo
        self.styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=self.styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("#0D7377"),
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Estilo para seções
        self.styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=self.styles["Heading2"],
                fontSize=13,
                textColor=colors.HexColor("#0D7377"),
                spaceAfter=8,
                spaceBefore=10,
                fontName="Helvetica-Bold",
            )
        )

        # Estilo para texto normal
        self.styles.add(
            ParagraphStyle(
                name="CustomNormal",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceAfter=6,
                alignment=TA_LEFT,
            )
        )

    def generate_prontuario(self, record, output_path=None):
        """
        Gera um prontuário PDF do paciente.

        Args:
            record: Dicionário com dados da avaliação

        Returns:
            Caminho do arquivo PDF gerado
        """
        if not output_path:
            patient_name = record.get("patient_name", "Paciente").replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"prontuario_{patient_name}_{timestamp}.pdf"

        # Criar documento PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        # Lista de elementos para o PDF
        story = []

        # Título
        story.append(Paragraph("PRONTUÁRIO DE AVALIAÇÃO", self.styles["CustomTitle"]))
        story.append(Spacer(1, 0.2 * inch))

        # Informações do paciente
        patient_info = [
            [
                Paragraph("<b>Nome do Paciente:</b>", self.styles["CustomNormal"]),
                Paragraph(
                    record.get("patient_name", "Não informado"),
                    self.styles["CustomNormal"],
                ),
            ],
            [
                Paragraph("<b>Data da Avaliação:</b>", self.styles["CustomNormal"]),
                Paragraph(record.get("data", "N/A"), self.styles["CustomNormal"]),
            ],
        ]

        patient_table = Table(patient_info, colWidths=[2.5 * inch, 3.5 * inch])
        patient_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E0F2FE")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB")),
                ]
            )
        )
        story.append(patient_table)
        story.append(Spacer(1, 0.3 * inch))

        # Resultado da avaliação
        level = record.get("level", "N/A")
        score = record.get("score", 0)

        # Determinar cor baseada no nível
        level_colors = {
            "Baixo": "#059669",
            "Médio": "#D97706",
            "Alto": "#DC2626",
            "Crítico": "#991B1B",
        }
        level_color = level_colors.get(level, "#0D7377")

        result_info = [
            [
                Paragraph("<b>Nível de Risco:</b>", self.styles["CustomNormal"]),
                Paragraph(
                    f"<font color='{level_color}'><b>{level}</b></font>",
                    self.styles["CustomNormal"],
                ),
            ],
            [
                Paragraph("<b>Pontuação Total:</b>", self.styles["CustomNormal"]),
                Paragraph(f"{score} pontos", self.styles["CustomNormal"]),
            ],
        ]

        result_table = Table(result_info, colWidths=[2.5 * inch, 3.5 * inch])
        result_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FED7D7")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB")),
                ]
            )
        )
        story.append(result_table)
        story.append(Spacer(1, 0.3 * inch))

        # Respostas detalhadas
        story.append(
            Paragraph("HISTÓRICO DE RESPOSTAS DETALHADO", self.styles["SectionTitle"])
        )

        responses = record.get("responses", [])
        if responses:
            # Agrupar respostas por eixo
            responses_by_eixo = {}
            for resp in responses:
                eixo = resp.get("eixo_nome", "Sem eixo")
                if eixo not in responses_by_eixo:
                    responses_by_eixo[eixo] = []
                responses_by_eixo[eixo].append(resp)

            # Exibir respostas por eixo
            for eixo, eixo_responses in responses_by_eixo.items():
                story.append(Paragraph(f"<b>{eixo}</b>", self.styles["SectionTitle"]))

                # Criar descrição detalhada para cada questão
                for resp in eixo_responses:
                    question_id = resp.get("question_id", "N/A")
                    pergunta_texto = resp.get(
                        "pergunta_texto", "Pergunta não disponível"
                    )
                    resposta = resp.get("resposta", "N/A")
                    resposta_text = "SIM" if resposta in ("sim", True) else "NÃO"
                    pontos = resp.get("pontos", 0)
                    resposta_color = (
                        "#059669" if resposta in ("sim", True) else "#DC2626"
                    )

                    # Criar estilo para questão
                    question_style = ParagraphStyle(
                        name=f"Question{question_id}",
                        parent=self.styles["Normal"],
                        fontSize=10,
                        spaceAfter=8,
                        leftIndent=20,
                        textColor=colors.black,
                    )

                    # Pergunta
                    question_text = Paragraph(
                        f"<b>Q{question_id:02d}:</b> {pergunta_texto}",
                        question_style,
                    )
                    story.append(question_text)

                    # Resposta com cor
                    answer_style = ParagraphStyle(
                        name=f"Answer{question_id}",
                        parent=self.styles["Normal"],
                        fontSize=10,
                        spaceAfter=12,
                        leftIndent=40,
                        textColor=colors.HexColor(resposta_color),
                    )
                    answer_text_para = Paragraph(
                        f"<b>Resposta:</b> <b>{resposta_text}</b> (+{pontos} pts)",
                        answer_style,
                    )
                    story.append(answer_text_para)

                story.append(Spacer(1, 0.2 * inch))
        else:
            story.append(
                Paragraph(
                    "Nenhuma resposta registrada.",
                    self.styles["CustomNormal"],
                )
            )

        # Rodapé
        story.append(Spacer(1, 0.3 * inch))
        story.append(
            Paragraph(
                f"<i>Prontuário gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</i>",
                self.styles["CustomNormal"],
            )
        )
        story.append(
            Paragraph(
                "<i>Este documento é confidencial e destina-se apenas ao uso profissional.</i>",
                self.styles["CustomNormal"],
            )
        )

        # Compilar PDF
        doc.build(story)

        return output_path
