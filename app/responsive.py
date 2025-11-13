"""
Sistema de responsividade para Tkinter - Simulação de VW/VH.
"""

import tkinter as tk


class ResponsiveHelper:
    """Gerenciador de dimensionamento responsivo para Tkinter."""

    _instance = None
    _window_width = 1000
    _window_height = 800
    _callbacks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResponsiveHelper, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, root):
        """Inicializa o sistema de responsividade com a janela principal."""
        cls._root = root
        cls._window_width = root.winfo_screenwidth()
        cls._window_height = root.winfo_screenheight()

        # Bind para atualizar dimensões
        root.bind("<Configure>", cls._on_window_resize)

    @classmethod
    def _on_window_resize(cls, event):
        """Callback quando a janela é redimensionada."""
        # Apenas processar eventos da janela principal
        if event.widget == cls._root:
            old_width = cls._window_width
            old_height = cls._window_height

            cls._window_width = event.width
            cls._window_height = event.height

            # Notificar callbacks registrados
            if (
                abs(old_width - cls._window_width) > 20
                or abs(old_height - cls._window_height) > 20
            ):
                for callback in cls._callbacks:
                    try:
                        callback(cls._window_width, cls._window_height)
                    except:
                        pass

    @classmethod
    def register_callback(cls, callback):
        """Registra um callback para ser chamado quando a janela redimensionar."""
        if callback not in cls._callbacks:
            cls._callbacks.append(callback)

    @classmethod
    def vw(cls, percentage):
        """Retorna pixels baseado em porcentagem da largura da janela (viewport width)."""
        return int((percentage / 100) * cls._window_width)

    @classmethod
    def vh(cls, percentage):
        """Retorna pixels baseado em porcentagem da altura da janela (viewport height)."""
        return int((percentage / 100) * cls._window_height)

    @classmethod
    def vmin(cls, percentage):
        """Retorna pixels baseado na menor dimensão."""
        return int((percentage / 100) * min(cls._window_width, cls._window_height))

    @classmethod
    def vmax(cls, percentage):
        """Retorna pixels baseado na maior dimensão."""
        return int((percentage / 100) * max(cls._window_width, cls._window_height))

    @classmethod
    def get_font_size(cls, base_size):
        """Retorna tamanho de fonte adaptativo baseado na resolução."""
        # Escala baseada na largura (referência: 1920px)
        scale_factor = cls._window_width / 1920
        # Limitar entre 0.7x e 1.3x
        scale_factor = max(0.7, min(1.3, scale_factor))
        return int(base_size * scale_factor)

    @classmethod
    def get_padding(cls, base_padding):
        """Retorna padding adaptativo."""
        scale_factor = cls._window_width / 1920
        scale_factor = max(0.6, min(1.5, scale_factor))
        return int(base_padding * scale_factor)


def vw(percentage):
    """Atalho para ResponsiveHelper.vw()"""
    return ResponsiveHelper.vw(percentage)


def vh(percentage):
    """Atalho para ResponsiveHelper.vh()"""
    return ResponsiveHelper.vh(percentage)


def responsive_font(base_size):
    """Atalho para ResponsiveHelper.get_font_size()"""
    return ResponsiveHelper.get_font_size(base_size)


def responsive_padding(base_padding):
    """Atalho para ResponsiveHelper.get_padding()"""
    return ResponsiveHelper.get_padding(base_padding)
