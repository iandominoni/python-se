"""
Módulo de gerenciamento de dados (perguntas e histórico).
Agora usa SQLite para persistência de respostas.
"""

import os
import sys
import json
from db import Database


def load_questions():
    """Carrega as perguntas do arquivo JSON."""
    try:
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(base_path, "questions.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


class QuestionManager:
    """Gerencia o fluxo de perguntas e cálculo de pontuação."""

    def __init__(self, questions_data):
        self.questions_data = questions_data
        self.responses = (
            []
        )  # Lista de respostas: [(eixo_idx, q_idx, pergunta_id, resposta, pontos), ...]
        self.score = 0
        self.current_eixo_index = 0
        self.current_question_index = 0
        self.total_questions = sum(
            len(eixo["perguntas"]) for eixo in self.questions_data["eixos"]
        )

    def get_current_question_number(self):
        """Retorna o número da pergunta atual (1-indexado)."""
        return (
            sum(
                len(self.questions_data["eixos"][i]["perguntas"])
                for i in range(self.current_eixo_index)
            )
            + self.current_question_index
            + 1
        )

    def get_current_eixo(self):
        """Retorna o eixo atual."""
        return self.questions_data["eixos"][self.current_eixo_index]

    def get_current_question(self):
        """Retorna a pergunta atual."""
        eixo = self.get_current_eixo()
        if self.current_question_index < len(eixo["perguntas"]):
            return eixo["perguntas"][self.current_question_index]
        return None

    def answer_question(self, response):
        """Processa uma resposta e avança para a próxima pergunta."""
        question = self.get_current_question()
        if not question:
            return False

        # Determinar pontos baseado na resposta
        if response == "sim":
            points = question.get("peso_sim", question.get("peso", 0))
        else:  # "nao"
            points = question.get("peso_nao", 1)

        # Registrar resposta
        self.responses.append(
            {
                "eixo_index": self.current_eixo_index,
                "question_index": self.current_question_index,
                "question_id": question["id"],
                "eixo_nome": self.get_current_eixo()["nome"],
                "pergunta_texto": question["texto"],
                "justificativa": question.get("justificativa", ""),
                "resposta": response,
                "pontos": points,
            }
        )

        self.score += points

        # Avançar para próxima pergunta
        self.current_question_index += 1

        if self.current_question_index >= len(self.get_current_eixo()["perguntas"]):
            self.current_eixo_index += 1
            self.current_question_index = 0

        return self.current_eixo_index < len(self.questions_data["eixos"])

    def is_finished(self):
        """Verifica se o questionário acabou."""
        return self.current_eixo_index >= len(self.questions_data["eixos"])

    def reset(self):
        """Reseta o gerenciador para um novo questionário."""
        self.responses = []
        self.score = 0
        self.current_eixo_index = 0
        self.current_question_index = 0


class HistoryManager:
    """Gerencia o histórico de avaliações usando SQLite."""

    def __init__(self):
        self.db = Database()

    def add_assessment(self, assessment_data):
        """
        Adiciona uma avaliação ao banco de dados.

        Args:
            assessment_data: Dicionário com:
                - patient_name: Nome do paciente
                - level: Nível de risco
                - score: Pontuação
                - responses: Lista de respostas
                - data: Data/hora da avaliação
        """
        # Salvar avaliação + respostas atomicamente
        return self.db.save_avaliacao_with_respostas(
            nome_paciente=assessment_data["patient_name"],
            nivel_risco=assessment_data["level"],
            pontuacao=assessment_data["score"],
            respostas=assessment_data["responses"],
        )

    def get_assessment(self, index):
        """Retorna uma avaliação específica (ordenada por índice reverso)."""
        avaliacoes = self.db.get_avaliacoes()
        if 0 <= index < len(avaliacoes):
            avaliacao = avaliacoes[index]
            # Adicionar respostas
            respostas = self.db.get_respostas_avaliacao(avaliacao["id"])
            # Renomear 'eixo' para 'eixo_nome' para compatibilidade com PDF generator
            for resp in respostas:
                if "eixo" in resp and "eixo_nome" not in resp:
                    resp["eixo_nome"] = resp.pop("eixo")
            avaliacao["responses"] = respostas
            # 'data' já vem formatada do db.get_avaliacoes()
            return avaliacao
        return None

    def get_all(self):
        """Retorna todas as avaliações."""
        return self.db.get_avaliacoes()

    def get_count(self):
        """Retorna o número de avaliações."""
        return self.db.get_total_avaliacoes()
