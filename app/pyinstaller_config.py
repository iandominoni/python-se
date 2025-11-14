# Desabilita strip binaries no Windows
import sys
from PyInstaller.building import build_main

# Monkey patch para evitar strip
original_process_collected_binary = build_main.process_collected_binary


def patched_process_collected_binary(binaries, config, stripping=False):
    """Override para desabilitar strip"""
    return original_process_collected_binary(binaries, config, stripping=False)


build_main.process_collected_binary = patched_process_collected_binary
