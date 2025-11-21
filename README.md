# 🧠 Sistema Especialista de Avaliação de Risco — DSM-5

## 📋 Descrição do Projeto

Este projeto é um **sistema especialista de avaliação de risco** que realiza uma **triagem baseada em critérios do DSM-5 (Manual Diagnóstico e Estatístico de Transtornos Mentais)** para identificar indicadores de transtornos alimentares.

O sistema utiliza perguntas binárias ("Sim" ou "Não") para avaliar comportamentos relacionados a **transtornos alimentares** em cinco eixos temáticos:

- **Eixo 1:** Comportamento Alimentar (4 perguntas)
- **Eixo 2:** Imagem Corporal (4 perguntas)
- **Eixo 3:** Emoção e Autoconceito (4 perguntas)
- **Eixo 4:** Controle e Rotina (5 perguntas)
- **Eixo 5:** Percepção do Problema (5 perguntas)

**Total:** 22 perguntas, com pontuação baseada em critérios clínicos e classificação automática de risco.

---

## 🚀 Funcionalidades Principais

- ✅ Interface gráfica moderna e intuitiva
- ✅ 22 perguntas distribuídas em **5 eixos temáticos**
- ✅ Exibição de progresso durante o questionário
- ✅ Pontuação progressiva baseada em **critérios clínicos**
- ✅ Classificação automática de risco:
  - **Baixo** → Indicadores mínimos
  - **Médio** → Indicadores moderados
  - **Alto** → Indicadores significativos
  - **Crítico** → Indicadores graves
- ✅ **Histórico de avaliações** — Salva e recupera avaliações anteriores
- ✅ **Geração de prontuários em PDF** — Documento detalhado com resultados
- ✅ **Envio por email** — Compartilhe resultados de forma segura
- ✅ **Visualização de respostas** — Revise respostas e resultados anteriores
- ✅ Arquitetura modular com base em **JSON** (fácil expansão e manutenção)

---

## 🧩 Estrutura de Arquivos

```
python-SE/
├── main.py                 # Aplicação principal
├── questions.json          # Base de dados com perguntas e critérios
├── db.py                   # Gerenciamento de histórico
├── pdf_generator.py        # Geração de prontuários em PDF
├── email_sender.py         # Envio de resultados por email
├── accordion.py            # Componentes de interface
├── config.py               # Configurações da aplicação
├── .env.example            # Template para configuração de email
└── README.md               # Documentação do projeto
```

---

## ⚠️ Aviso Importante

Este é um **projeto acadêmico e educacional**. O sistema é uma ferramenta de **triagem** e seus resultados:

- **NÃO substituem** a avaliação de um profissional de saúde qualificado
- **NÃO devem ser utilizados** para diagnóstico clínico real
- São apenas para **fins educacionais e de pesquisa**

Qualquer pessoa com preocupações sobre sua saúde mental deve consultar um profissional credenciado.
