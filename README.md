<<<<<<< HEAD
# 🧠 Sistema Especialista de Avaliação de Risco — DSM-5

## 📋 Descrição do Projeto

Este projeto é um **sistema especialista em Python** que realiza uma **avaliação de risco baseada em critérios do DSM-5 (Manual Diagnóstico e Estatístico de Transtornos Mentais)**.

O sistema utiliza perguntas binárias (“Sim” ou “Não”) para avaliar comportamentos relacionados a **transtornos alimentares** em quatro eixos distintos:

- **Eixo 1:** Comportamento Alimentar (4 perguntas)
- **Eixo 2:** Imagem Corporal (4 perguntas)
- **Eixo 3:** Emoção e Autoconceito (4 perguntas)
- **Eixo 4:** Controle e Rotina (5 perguntas)

**Total:** 17 perguntas, com pontuação progressiva e classificação automática de risco.

O projeto inclui uma **versão GUI leve em Tkinter** (compatível com Windows) e uma versão original em **PyQt** (para Linux).

---

## 🚀 Funcionalidades Principais

- ✅ Interface gráfica simples e intuitiva (**Tkinter**)
- ✅ 17 perguntas distribuídas em **4 eixos temáticos**
- ✅ Exibição de progresso (“Pergunta 5 de 17”)
- ✅ Pontuação progressiva baseada em **pesos definidos no DSM-5**
- ✅ Classificação automática de risco:
  - **0-32** → Baixo
  - **33-42** → Médio
  - **43-52** → Alto
  - **53+** → Crítico
- ✅ Arquitetura modular com base em **JSON** (fácil expansão e manutenção)

---

## 🧩 Estrutura de Arquivos

```bash
python-SE/
├── main_windows_tk.py      # Aplicação principal (Windows)
├── main.py                 # Versão original (Linux/Qt)
├── questions.json          # Base de dados com perguntas e pesos
└── README.md               # Documentação do projeto
```
=======
# 🧠 Sistema Especialista de Avaliação de Risco — DSM-5

## 📋 Descrição do Projeto

Este projeto é um **sistema especialista em Python** que realiza uma **avaliação de risco baseada em critérios do DSM-5 (Manual Diagnóstico e Estatístico de Transtornos Mentais)**.

O sistema utiliza perguntas binárias (“Sim” ou “Não”) para avaliar comportamentos relacionados a **transtornos alimentares** em quatro eixos distintos:

- **Eixo 1:** Comportamento Alimentar (4 perguntas)  
- **Eixo 2:** Imagem Corporal (4 perguntas)  
- **Eixo 3:** Emoção e Autoconceito (4 perguntas)  
- **Eixo 4:** Controle e Rotina (5 perguntas)

**Total:** 17 perguntas, com pontuação progressiva e classificação automática de risco.

O projeto inclui uma **versão GUI leve em Tkinter** (compatível com Windows) e uma versão original em **PyQt** (para Linux).

---

## 🚀 Funcionalidades Principais

- ✅ Interface gráfica simples e intuitiva (**Tkinter**)
- ✅ 17 perguntas distribuídas em **4 eixos temáticos**
- ✅ Exibição de progresso (“Pergunta 5 de 17”)
- ✅ Pontuação progressiva baseada em **pesos definidos no DSM-5**
- ✅ Classificação automática de risco:
  - **0–10** → Baixo  
  - **11–20** → Médio  
  - **21–30** → Alto  
  - **31+** → Crítico
- ✅ Arquitetura modular com base em **JSON** (fácil expansão e manutenção)

---

## 🧩 Estrutura de Arquivos

```bash
python-SE/
├── main_windows_tk.py      # Aplicação principal (Windows)
├── main.py                 # Versão original (Linux/Qt)
├── questions.json          # Base de dados com perguntas e pesos
└── README.md               # Documentação do projeto
>>>>>>> deb100b131edc70461f795ce492d99019a18dcce
