# Sistema Especialista de Avaliação de Risco - DSM-5# Sistema Especialista — build do executável (Windows)

## 📋 Descrição do Projeto
Este repositório contém a aplicação em Python e uma versão leve para Windows (`main_windows_tk.py`) que usa Tkinter (módulo da stdlib) — ideal para gerar um executável menor com PyInstaller.

Um sistema especialista em Python que realiza uma avaliação de risco baseada em critérios do DSM-5 (Manual Diagnóstico e Estatístico de Transtornos Mentais). O sistema utiliza perguntas binárias ("Sim" ou "Não") para avaliar comportamentos relacionados a transtornos alimentares em quatro eixos distintos:Arquivos importantes:

- **Eixo 1**: Comportamento Alimentar (4 perguntas)- `main.py` — versão original (Linux/Qt).

- **Eixo 2**: Imagem Corporal (4 perguntas)- `main_windows_tk.py` — entrypoint leve (Tkinter) para Windows.

- **Eixo 3**: Emoção e Autoconceito (4 perguntas)- `questions.json` — dados usados pela aplicação.

- **Eixo 4**: Controle e Rotina (5 perguntas)- `.gitignore` — já configurado para ignorar `dist/`, `build/`, `*.spec` e `*.exe`.

**Total**: 17 perguntas com pontuação progressiva e classificação automática de risco.Como gerar o .exe (passos mínimos, executar em Windows):

### ✨ Funcionalidades Principais1. Abra PowerShell ou cmd.exe (NO WINDOWS, não use WSL para gerar o .exe Windows).

2. Entre na pasta do projeto (exemplo PowerShell):

- ✅ Interface gráfica intuitiva em Tkinter (compatível com Windows)

- ✅ 17 perguntas distribuídas em 4 eixos temáticos```powershell

- ✅ Pontuação progressiva baseada em pesos predefinidoscd \\\wsl.localhost\Ubuntu\home\iandominoni\projetos\pythonstuff\facul\python-SE

- ✅ Exibição de progresso (ex: "Pergunta 5 de 17")```

- ✅ Classificação automática de risco:

  - **0-10**: Baixo3. Instale o PyInstaller (se ainda não estiver):

  - **11-20**: Médio

  - **21-30**: Alto```powershell

  - **31+**: Críticopy -3 -m pip install --upgrade pip

- ✅ Arquitetura modular baseada em JSON para fácil expansãopy -3 -m pip install pyinstaller

````

---

4. Gere o executável (usa `main_windows_tk.py` e inclui `questions.json`):

## 🚀 Como Executar no Windows

```powershell

### Opção 1: Usando Python (Para Desenvolvimento)py -3 -m PyInstaller --onefile --windowed --add-data "questions.json;." main_windows_tk.py

````

#### Pré-requisitos

- Python 3.8 ou superior instalado ([Baixar Python](https://www.python.org/downloads/))O executável aparecerá em `dist\main_windows_tk.exe`.

- Windows 7 ou superior

Notas sobre tamanho e detecções do Windows

#### Passos

- Usando Tkinter evitamos incluir bibliotecas GUI externas (ex.: PySide6), reduzindo substancialmente o tamanho do .exe.

1. **Baixe ou clone este repositório** para uma pasta no seu computador- Mesmo assim, executáveis gerados por PyInstaller NÃO são assinados. O Windows SmartScreen e alguns antivírus podem mostrar avisos do tipo "Windows SmartScreen can't verify this app" ou marcar o arquivo como potencialmente inseguro.

2. **Abra o Prompt de Comando (cmd) ou PowerShell**

3. **Navegue até a pasta do projeto:**

   ```cmd
   cd C:\caminho\para\python-SE
   ```

4. **(Opcional) Crie um ambiente virtual:**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Instale as dependências** (Tkinter geralmente já vem com Python):

   ```cmd
   pip install --upgrade pip
   ```

6. **Execute a aplicação:**
   ```cmd
   python main_windows_tk.py
   ```

A janela da aplicação se abrirá automaticamente! 🎉

### Opção 2: Usando o Executável (.exe) - Recomendado para Usuários

Se você recebeu um arquivo `.exe` compilado:

1. **Clique duas vezes** no arquivo `.exe` (exemplo: `main_windows_tk.exe`)
2. Clique em "Executar de qualquer forma" se o Windows avisar sobre segurança
3. A aplicação se abrirá automaticamente
4. **Nenhuma instalação de Python é necessária!**

---

## 📖 Como Usar a Aplicação

1. **Inicie o programa** (conforme instruções acima)
2. **Leia a pergunta** exibida na janela
3. **Responda clicando** em "Sim" ou "Não"
4. **Acompanhe o progresso** no topo da janela (ex: Pergunta 5 de 17)
5. **Avance automaticamente** entre os eixos temáticos
6. **Receba o resultado final** com:
   - Pontuação total (0 a 51)
   - Nível de risco classificado

---

## 📊 Interpretação dos Resultados

| Pontuação | Nível de Risco | Significado                                          |
| --------- | -------------- | ---------------------------------------------------- |
| 0-10      | ✅ Baixo       | Sem indícios clínicos significativos                 |
| 11-20     | ⚠️ Médio       | Relação emocional desajustada com alimentação/imagem |
| 21-30     | 🔴 Alto        | Padrões disfuncionais em desenvolvimento             |
| 31+       | ⛔ Crítico     | Possível transtorno alimentar ativo                  |

---

## 📁 Estrutura dos Arquivos

```
python-SE/
├── main_windows_tk.py      # ← Aplicação principal para Windows
├── main.py                 # Versão Linux/WSL (não necessária no Windows)
├── questions.json          # Base de dados das perguntas
└── README.md              # Este arquivo
```

---

## ⚙️ Requisitos do Sistema

- **Windows 7, 8, 10 ou 11**
- **Python 3.8+** (apenas se executando a partir do código-fonte)
- **100 MB** de espaço livre em disco (se usando o executável)
- Conexão com internet: **Não necessária**

---

## 🔧 Gerando um Executável Personalizado (Avançado)

Se deseja criar seu próprio `.exe`:

1. **Instale o PyInstaller** (no Windows):

   ```cmd
   pip install pyinstaller
   ```

2. **Gere o executável:**

   ```cmd
   pyinstaller --onefile --windowed --add-data "questions.json;." main_windows_tk.py
   ```

3. **O arquivo `.exe` estará em:** `dist\main_windows_tk.exe`

---

## ⚠️ Aviso Importante

**Este sistema é uma ferramenta de triagem educacional e NÃO substitui avaliação clínica profissional.**

Para diagnosticar transtornos alimentares ou qualquer condição de saúde mental, consulte um profissional de saúde qualificado (psicólogo, psiquiatra ou nutricionista).

---

## 📞 Suporte

Para dúvidas ou reportar problemas, entre em contato através dos canais oficiais do projeto.

---

**Versão**: 1.0  
**Última atualização**: Novembro de 2025  
**Plataforma**: Windows

