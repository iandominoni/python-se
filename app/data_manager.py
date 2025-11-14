"""
Módulo de gerenciamento de dados (perguntas e histórico).
"""

import os
import sys
import json


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
    """Gerencia o histórico de avaliações com cache em arquivo."""

    def __init__(self):
        self.history = []
        self.cache_file = self._get_cache_path()
        self._load_from_cache()

    def _get_cache_path(self):
        """Retorna o caminho do arquivo de cache."""
        if getattr(sys, "frozen", False):
            # Se for executável PyInstaller, salva no diretório do executável
            base_path = os.path.dirname(sys.executable)
        else:
            # Modo desenvolvimento
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, "history_cache.json")

    def _load_from_cache(self):
        """Carrega o histórico do arquivo de cache com limite de registros."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Manter apenas os últimos 100 registros para performance
                    self.history = data[-100:] if len(data) > 100 else data
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []

    def _save_to_cache(self):
        """Salva o histórico no arquivo de cache."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")

    def add_assessment(self, assessment_data):
        """Adiciona uma avaliação ao histórico e salva no cache."""
        self.history.append(assessment_data)
        self._save_to_cache()

    def get_assessment(self, index):
        """Retorna uma avaliação específica."""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None

    def get_all(self):
        """Retorna todas as avaliações."""
        return self.history

    def get_count(self):
        """Retorna o número de avaliações."""
        return len(self.history)
