# 🏥 Sistema de Avaliação de Risco - DSM-5# 🏥 Sistema de Avaliação de Risco - DSM-5# Sistema Especialista de Avaliação de Risco - DSM-5

-instalar no windows pyinstaller --onefile --windowed --exclude-module=numpy --exclude-module=pandas --exclude-module=scipy --exclude-module=matplotlib --add-data "questions.json;." main.py
Sistema de triagem para avaliação de risco de transtornos alimentares baseado em critérios do DSM-5 com interface moderna multiplataforma.Sistema de triagem para avaliação de risco de transtornos alimentares baseado em critérios do DSM-5 com interface moderna multiplataforma.## 📋 Descrição do Projeto

## 📋 Sobre o Projeto## 📋 Sobre o ProjetoUm sistema especialista em Python que realiza uma avaliação de risco baseada em critérios do DSM-5 (Manual Diagnóstico e Estatístico de Transtornos Mentais). O sistema utiliza perguntas binárias ("Sim" ou "Não") para avaliar comportamentos relacionados a transtornos alimentares em quatro eixos distintos:

- **22 perguntas** distribuídas em **5 eixos temáticos**- **22 perguntas** distribuídas em **5 eixos temáticos**- **Eixo 1**: Comportamento Alimentar (4 perguntas)

- **Histórico persistente** de todas as avaliações com detalhes completos

- **Interface modular** separada por plataforma:- **Histórico persistente** de todas as avaliações com detalhes completos- **Eixo 2**: Imagem Corporal (4 perguntas)

  - **Windows**: Tkinter (sem dependências externas)

  - **Linux/WSL**: PySide6 (Qt nativo)- **Interface modular** separada por plataforma:- **Eixo 3**: Emoção e Autoconceito (4 perguntas)

- **Design profissional** e responsivo

- **Visualização detalhada** de respostas com justificativas - **Windows**: Tkinter (sem dependências externas)- **Eixo 4**: Controle e Rotina (5 perguntas)

### 5 Eixos de Avaliação - **Linux/WSL**: PySide6 (Qt nativo)

1. **Eixo 1 — Comportamento Alimentar** (4 perguntas)- **Design profissional** e responsivo**Total**: 17 perguntas com pontuação progressiva e classificação automática de risco.

2. **Eixo 2 — Imagem Corporal** (4 perguntas)

3. **Eixo 3 — Emoção e Autoconceito** (4 perguntas)- **Visualização detalhada** de respostas com justificativas

4. **Eixo 4 — Controle e Rotina** (5 perguntas)

5. **Eixo 5 — Percepção do Problema** (5 perguntas)---

---### 5 Eixos de Avaliação

## 📁 Estrutura do Projeto## ✨ Funcionalidades Principais

````````1. **Eixo 1 — Comportamento Alimentar** (4 perguntas)

python-SE/

├── README.md                    # Este arquivo (instruções universais)2. **Eixo 2 — Imagem Corporal** (4 perguntas)- ✅ **Interface moderna e responsiva** com design profissional

├── questions.json               # Base de dados (raiz - compartilhada)

│3. **Eixo 3 — Emoção e Autoconceito** (4 perguntas)- ✅ **17 perguntas** distribuídas em 4 eixos temáticos

├── windows/                     # Versão Windows (Tkinter)

│   ├── main.py                  # Aplicação principal4. **Eixo 4 — Controle e Rotina** (5 perguntas)- ✅ **Histórico de avaliações** - acompanhe suas avaliações anteriores

│   ├── config.py                # Configurações (cores, ranges)

│   ├── data_manager.py          # Gerenciamento de dados5. **Eixo 5 — Percepção do Problema** (5 perguntas)- ✅ **Menu principal** com botões para iniciar teste ou ver histórico

│   ├── utils.py                 # Utilitários (cálculos, formatação)

│   ├── ui_components_windows.py # Componentes Tkinter- ✅ **Resultado final apenas com nível de risco** (sem mostrar pontos)

│   └── questions.json           # Cópia local

│---- ✅ **Não fecha ao clicar OK** - continua na tela de resultados

└── linux/                       # Versão Linux/WSL (PySide6)

    ├── main.py                  # Aplicação principal- ✅ **Barra de progresso visual** durante o questionário

    ├── config.py                # Configurações (cores, ranges)

    ├── data_manager.py          # Gerenciamento de dados## 📁 Estrutura do Projeto- ✅ **Classificação automática** de risco com cores:

    ├── utils.py                 # Utilitários (cálculos, formatação)

    ├── ui_components_linux.py   # Componentes PySide6- **Baixo** (0-10) - Verde ✅

    └── questions.json           # Cópia local

```````- **Médio** (11-20) - Amarelo ⚠️



---python-SE/  - **Alto** (21-30) - Vermelho 🔴



## ✨ Funcionalidades├── README.md                    # Este arquivo (instruções universais)  - **Crítico** (31+) - Vermelho Escuro ⛔



- ✅ **22 perguntas** em 5 eixos temáticos├── questions.json               # Base de dados (raiz - compartilhada)- ✅ **Arquitetura modular** baseada em JSON para fácil expansão

- ✅ **Histórico persistente** com detalhes de cada resposta

- ✅ **Visualização detalhada** - Clique "Ver Detalhes" para:│- ✅ **Tkinter puro** - sem dependências externas, executável otimizado

  - Todas as 22 respostas do questionário

  - Cada resposta organizada por eixo├── windows/                     # Versão Windows (Tkinter)

  - Símbolo visual: ✓ SIM (verde) ou ✗ NÃO (vermelho)

  - **Texto completo da pergunta**│   ├── main.py                  # Aplicação principal---

  - **Justificativa/contexto da pergunta**

  - Pontos atribuídos por resposta│   ├── config.py                # Configurações (cores, ranges)

  - Resumo com pontuação total e nível de risco

- ✅ **Menu intuitivo** com navegação suave│   ├── data_manager.py          # Gerenciamento de dados## 🎨 Interface Moderna

- ✅ **Barra de progresso** atualizada em tempo real (redimensionável)

- ✅ **Pontuação dinâmica** - pesos diferentes para Sim/Não por pergunta│   ├── utils.py                 # Utilitários (cálculos, formatação)

- ✅ **Classificação de risco** com cores:

  - **Baixo** (0-15) - Verde│   ├── ui_components_windows.py # Componentes Tkinter- **Design profissional** com paleta de cores harmônica

  - **Médio** (16-35) - Amarelo

  - **Alto** (36-56) - Vermelho│   ├── questions.json           # Cópia local- **Componentes estilizados** e responsivos

  - **Crítico** (57+) - Vermelho Escuro

- ✅ **Não fecha automaticamente** - continua acessível│   └── README.md                # Instruções Windows- **Navegação intuitiva** entre telas (Menu → Quiz → Resultados → Histórico)

- ✅ **Arquitetura modular** - fácil de manter e estender

│- **Feedback visual** com barra de progresso

---

└── linux/                       # Versão Linux/WSL (PySide6)- **Mensagens contextualizadas** para cada nível de risco

## 🚀 Início Rápido

    ├── main.py                  # Aplicação principal- **Botões com efeito hover** para melhor UX

### Windows

    ├── config.py                # Configurações (cores, ranges)

```cmd

cd windows    ├── data_manager.py          # Gerenciamento de dados---

python main.py

```    ├── utils.py                 # Utilitários (cálculos, formatação)



**Primeira vez?** Tkinter já vem com Python, nenhuma instalação extra necessária!    ├── ui_components_linux.py   # Componentes PySide6## 📁 Estrutura dos Arquivos



### Linux/WSL    ├── questions.json           # Cópia local



```bash    └── README.md                # Instruções Linux```

cd linux

pip install PySide6```python-SE/

python main.py

```├── main_windows_tk.py      # ← Aplicação principal (Tkinter - Recomendado!)



------├── main.py                 # Versão Linux/WSL (PySide6 - uso opcional)



## 📖 Como Usar├── questions.json          # Base de dados das perguntas (17 perguntas)



### Menu Inicial## ✨ Funcionalidades├── build_optimized.py      # Script para gerar .exe otimizado



- **▶ Iniciar Avaliação** - Comece um novo teste├── main_windows_tk.spec    # Spec do PyInstaller (customizado)

- **📋 Histórico** - Veja todas as suas avaliações anteriores

- ✅ **22 perguntas** em 5 eixos temáticos├── BUILD_GUIDE.md          # Guia detalhado para gerar build

### Durante a Avaliação

- ✅ **Histórico persistente** com detalhes de cada resposta├── README.md               # Este arquivo

- Leia a pergunta na tela

- Veja o eixo temático no topo- ✅ **Visualização detalhada** - Clique "Ver Detalhes" para:└── requirements_windows.txt # Dependências (apenas para dev)

- Acompanhe o progresso com a barra visual

- Clique em **✓ Sim** ou **✗ Não** para responder  - Todas as 22 respostas do questionário```



### Visualizar Histórico  - Cada resposta organizada por eixo



1. Clique em **"📋 Histórico"** no menu  - Símbolo visual: ✓ SIM (verde) ou ✗ NÃO (vermelho)---

2. Veja a lista de todas as avaliações realizadas

3. Clique em **"Ver Detalhes →"** em qualquer avaliação para ver:  - **Texto completo da pergunta**

   - Todas as 22 respostas

   - Justificativa de cada pergunta  - **Justificativa/contexto da pergunta**## 🚀 Como Executar no Windows

   - Pontuação individual

   - Resultado final  - Pontos atribuídos por resposta



### Resultado Final  - Resumo com pontuação total e nível de risco### Opção 1: Executável Pré-compilado (Recomendado para Usuários)



- Visualize o **Nível de Risco**- ✅ **Menu intuitivo** com navegação suave

- Leia a mensagem interpretativa

- Escolha fazer outra avaliação ou ver histórico- ✅ **Barra de progresso** atualizada em tempo realSe você recebeu um `.exe` compilado:

- A aplicação continua aberta

- ✅ **Pontuação dinâmica** - pesos diferentes para Sim/Não por pergunta

---

- ✅ **Classificação de risco** com cores:1. **Clique duas vezes** no arquivo `main_windows_tk.exe`

## 📊 Escala de Risco

  - **Baixo** (0-32) - Verde2. Clique em "Executar de qualquer forma" se o Windows avisar sobre segurança

| Pontuação | Nível    | Interpretação                        |

|-----------|----------|--------------------------------------|  - **Médio** (33-42) - Amarelo3. **Nenhuma instalação necessária!** 🎉

| 0-15      | Baixo    | Sem indícios clínicos significativos |

| 16-35     | Médio    | Relação desajustada com alimentação  |  - **Alto** (43-52) - Vermelho

| 36-56     | Alto     | Padrões disfuncionais               |

| 57+       | Crítico  | Possível transtorno alimentar ativo |  - **Crítico** (53+) - Vermelho Escuro### Opção 2: Usando Python (Para Desenvolvimento)



---- ✅ **Não fecha automaticamente** - continua acessível



## 🔨 Como Buildar- ✅ **Arquitetura modular** - fácil de manter e estender#### Pré-requisitos



### Windows - Gerar Executável (.exe)



#### Passo 1: Instalar PyInstaller---- Python 3.8 ou superior instalado ([Baixar Python](https://www.python.org/downloads/))



Abra o **Prompt de Comando (CMD)** e execute:- Windows 7 ou superior



```cmd## 🚀 Início Rápido

pip install pyinstaller

```#### Passos



#### Passo 2: Acessar pasta Windows### Windows



```cmd1. **Baixe ou clone este repositório** para uma pasta no seu computador

cd windows

``````cmd



#### Passo 3: Gerar executável (Método Simples)cd windows2. **Abra o Prompt de Comando (cmd) ou PowerShell**



```cmdpython main.py

pyinstaller --onefile --windowed --add-data "questions.json;." main.py

``````3. **Navegue até a pasta do projeto:**



✅ **Resultado**: O arquivo `main.exe` estará em `dist\main.exe`



#### Passo 4 (Opcional): Com Otimizações**Primeira vez?** Tkinter já vem com Python, nenhuma instalação extra necessária!   ```cmd



Se quiser um executável menor, abra o **CMD** (não PowerShell) e execute:   cd C:\caminho\para\python-SE



```cmd### Linux/WSL   ```

cd windows

pyinstaller --onefile --windowed --exclude-module=numpy --exclude-module=pandas --exclude-module=scipy --exclude-module=matplotlib --add-data "questions.json;." main.py

````````

`````bash4. **(Opcional) Crie um ambiente virtual:**

**Resultado esperado**: ~40-50 MB (apenas Tkinter)

cd linux

---

pip install PySide6  # Apenas primeira vez   ```cmd

### Linux - Executável Estático (Opcional)

python main.py   python -m venv venv

Para criar um executável Linux:

```   venv\Scripts\activate

```bash

cd linux````

pip install pyinstaller

pyinstaller --onefile --add-data "questions.json:." main.py---

`````

5. **Instale as dependências** (Tkinter geralmente já vem com Python):

O executável estará em: `linux/dist/main`

## 📖 Como Usar

**Nota**: No Linux é mais comum usar Python + PySide6 diretamente, não gerar executável.

```cmd

---

### Menu Inicial   pip install --upgrade pip

## ⚙️ Requisitos

```

### Windows

- Python 3.8+- **▶ Iniciar Avaliação** - Comece um novo teste

- Tkinter (já incluído com Python)

- 50 MB espaço livre (se usar executável)- **📋 Histórico** - Veja todas as suas avaliações anteriores6. **Execute a aplicação:**

### Linux/WSL### Durante a Avaliação ```cmd

- Python 3.8+

- PySide6 6.5+ (instala via pip)python main_windows_tk.py

- Qt6 libraries (geralmente já presentes)

- Leia a pergunta na tela ```

---

- Veja o eixo temático no topo

## ⚠️ Avisos Importantes

- Acompanhe o progresso com a barra visualA janela da aplicação se abrirá automaticamente! 🎉

**Este sistema é uma ferramenta de triagem educacional.**

- Clique em **✓ Sim** ou **✗ Não** para responder

⛔ **NÃO substitui avaliação clínica profissional**

---

Para diagnosticar transtornos alimentares ou qualquer condição de saúde mental, consulte um profissional qualificado (psicólogo, psiquiatra ou nutricionista).

### Visualizar Histórico

---

## 📖 Como Usar a Aplicação

## 🔐 Segurança

1. Clique em **"📋 Histórico"** no menu

- ✅ **Dados Locais** - Todas as avaliações ficam apenas na memória

- ✅ **Sem Internet** - A aplicação não se conecta a nenhum servidor2. Veja a lista de todas as avaliações realizadas1. **Menu Inicial** - Escolha entre:

- ✅ **Open Source** - Código transparente e auditável

- ⚠️ **Windows**: Se receber aviso de segurança do SmartScreen, clique "Executar de qualquer forma"3. Clique em **"Ver Detalhes →"** em qualquer avaliação para ver:

--- - Todas as 22 respostas - "Iniciar Avaliação" para começar um novo teste

## 🐛 Troubleshooting - Justificativa de cada pergunta - "Histórico" para ver suas avaliações anteriores

**P: Erro "ModuleNotFoundError: No module named 'PySide6'" (Linux)** - Pontuação individual

```bash

pip install PySide6   - Resultado final2. **Durante o Questionário:**

```

### Resultado Final - Leia a pergunta exibida na tela

**P: Erro "questions.json não encontrado"**

- Verifique se o arquivo existe na mesma pasta que `main.py`- Veja o eixo temático no topo

**P: Barra de progresso não preenche completamente (Windows)**- Visualize o **Nível de Risco** - Acompanhe o progresso com a barra visual

- Corrigido na versão atual - redimensiona dinamicamente

- Leia a mensagem interpretativa - Clique em "✓ Sim" ou "✗ Não" para responder

**P: Justificativa não aparece no histórico**

- Verifique se está usando a versão mais recente- Escolha fazer outra avaliação ou ver histórico

- Limpe o histórico anterior (armazenado em memória)

- A aplicação continua aberta3. **Resultado Final:**

**P: PyInstaller gera erro no Windows**

- Tente usar `cmd.exe` ao invés de PowerShell--- - Visualize apenas o **Nível de Risco** (sem pontos visíveis)

- Se usar PowerShell, não use `^` para quebra de linha, use uma linha

- Leia a mensagem interpretativa

---

## 📊 Escala de Risco - Escolha para fazer outra avaliação ou ver histórico

## 📝 Changelog

- **A aplicação NÃO fecha automaticamente**

### v3.0 (Atual - Novembro 2025)

| Pontuação | Nível | Interpretação |

**Novidades:**

- ✨ Adicionado Eixo 5 (Percepção do Problema) com 5 novas perguntas|-----------|----------|--------------------------------------|4. **Histórico:**

- ✨ **Histórico detalhado** com visualização de todas as respostas

- ✨ **Justificativas das perguntas** aparecem no histórico| 0-32 | Baixo | Sem indícios clínicos significativos | - Veja todas as suas avaliações anteriores

- ✨ Separação em plataformas (Windows/Linux)

- ✨ Windows: Tkinter (sem dependências externas)| 33-42 | Médio | Relação desajustada com alimentação | - Data, hora e nível de risco de cada teste

- ✨ Linux: PySide6 (componentes Qt nativos)

- 🔧 Pontuação dinâmica (peso_sim e peso_nao)| 43-52 | Alto | Padrões disfuncionais | - Volte ao menu a qualquer momento

- 🔧 Barra de progresso redimensionável

- 🐛 Corrigido redimensionamento de componentes| 53+ | Crítico | Possível transtorno alimentar ativo |

### v2.0---

- Interface redesenhada

- Sistema de histórico---

- Barra de progresso visual

- Cores por nível de risco## 📊 Interpretação dos Resultados

### v1.0## 🔨 Como Buildar

- Interface básica

- Questionário funcional| Nível | Pontuação | Significado |

- Classificação simples

### Windows - Gerar Executável (.exe)| ---------- | --------- | ---------------------------------------------------- |

---

| ✅ Baixo | 0-10 | Sem indícios clínicos significativos |

**Versão**: 3.0

**Última atualização**: Novembro de 2025 #### Pré-requisitos| ⚠️ Médio | 11-20 | Relação emocional desajustada com alimentação/imagem |

**Plataformas**: Windows (Tkinter) | Linux/WSL (PySide6)

**Linguagem**: Python 3.8+ ```cmd| 🔴 Alto | 21-30 | Padrões disfuncionais em desenvolvimento |

**Licença**: Educacional

pip install pyinstaller| ⛔ Crítico | 31+ | Possível transtorno alimentar ativo |

````

---

#### Método 1: Automático (Recomendado)

```cmd## 🔧 Gerando um Executável Otimizado

cd windows

pyinstaller --onefile --windowed --add-data "questions.json;." main.py### Método Rápido

````

No **PowerShell ou CMD.exe** (no Windows):

O executável estará em: `windows/dist/main.exe`

#### Método 2: Com Otimizações# 1. Instale PyInstaller

````cmdpip install --upgrade pip pyinstaller

cd windows

pyinstaller --onefile --windowed ^# 2. Gere o executável otimizado

  --exclude-module=numpy ^python build_optimized.py

  --exclude-module=pandas ^```

  --exclude-module=scipy ^

  --exclude-module=matplotlib ^O `.exe` estará em `dist\main_windows_tk.exe`

  --add-data "questions.json;." ^

  main.py
````

### Método com .spec File

````powershell

**Resultado esperado**: ~40-50 MB (apenas Tkinter)# Gere usando o arquivo spec customizado

pyinstaller main_windows_tk.spec

---```



### Linux - Executável Estático (Opcional)Veja `BUILD_GUIDE.md` para instruções detalhadas e troubleshooting.



Para criar um executável Linux:---



```bash## ⚡ Otimizações Aplicadas

cd linux

pip install pyinstaller- **Apenas Tkinter** - Nenhuma biblioteca GUI externa (PySide6, PyQt, etc)

- **Módulos excluídos** - pip, setuptools, email, http, urllib, unittest, etc

pyinstaller --onefile --add-data "questions.json:." main.py- **Arquivo único** - `--onefile` para facilitar distribuição

```- **Sem console** - `--windowed` para app profissional

- **Tamanho esperado** - ~30-40 MB (muito menor que versões com PySide6)

O executável estará em: `linux/dist/main`

---

**Nota**: A forma recomendada no Linux é usar Python + PySide6 diretamente, não gerar executável.

## ⚙️ Requisitos do Sistema

---

- **Windows 7, 8, 10 ou 11**

## ⚙️ Requisitos- **Python 3.8+** (apenas se executando a partir do código-fonte)

- **50 MB** de espaço livre em disco (se usando o executável)

### Windows- Conexão com internet: **Não necessária**

- Python 3.8+

- Tkinter (já incluído com Python)---

- 50 MB espaço livre (se usar executável)

## ⚠️ Aviso Importante

### Linux/WSL

- Python 3.8+**Este sistema é uma ferramenta de triagem educacional e NÃO substitui avaliação clínica profissional.**

- PySide6 6.5+ (instala via pip)

- Qt6 libraries (geralmente já presentes)Para diagnosticar transtornos alimentares ou qualquer condição de saúde mental, consulte um profissional de saúde qualificado (psicólogo, psiquiatra ou nutricionista).



------



## ⚠️ Avisos Importantes## 🔐 Segurança & Avisos do Windows



**Este sistema é uma ferramenta de triagem educacional.**- **SmartScreen Warning**: Executáveis gerados por PyInstaller não são assinados. O Windows pode mostrar "Windows SmartScreen can't verify this app" - é normal para apps não comerciais. Clique em "Executar de qualquer forma".



⛔ **NÃO substitui avaliação clínica profissional**- **Dados Locais**: Todas as avaliações são armazenadas apenas na memória da sessão. Nenhum dado é enviado para servidores externos.



Para diagnosticar transtornos alimentares ou qualquer condição de saúde mental, consulte um profissional qualificado (psicólogo, psiquiatra ou nutricionista).---



---## 📞 Suporte & Troubleshooting



## 🔐 Segurança**P: Dá erro "questions.json não encontrado"**



- ✅ **Dados Locais** - Todas as avaliações ficam apenas na memória- R: Verifique se o arquivo está no mesmo diretório do .exe ou do script Python

- ✅ **Sem Internet** - A aplicação não se conecta a nenhum servidor

- ✅ **Open Source** - Código transparente e auditável**P: Executável muito grande?**

- ⚠️ **Windows**: Se receber aviso de segurança do SmartScreen, clique "Executar de qualquer forma"

- R: Use o script `build_optimized.py` que limpa módulos desnecessários

---

**P: O programa fecha ao clicar OK?**

## 🐛 Troubleshooting

- R: Esse comportamento foi corrigido na nova versão. A app continua aberta após resultados.

**P: Erro "ModuleNotFoundError: No module named 'PySide6'" (Linux)**

```bash---

pip install PySide6

```## 📝 Changelog



**P: Erro "questions.json não encontrado"**### v2.0 (Atual)

- Verifique se o arquivo existe na mesma pasta que `main.py`

- ✨ Interface completamente redesenhada com Tkinter

**P: Barra de progresso não preenche completamente (Windows)**- ✨ Sistema de histórico de avaliações

- Corrigido na versão atual - redimensiona dinamicamente- ✨ Menu principal com navegação

- ✨ Barra de progresso visual

**P: Justificativa não aparece no histórico**- ✨ Cores baseadas no nível de risco

- Verifique se está usando a versão mais recente- ✨ Não mostra pontuação (apenas nível de risco)

- Limpe o histórico anterior (armazenado em memória)- ✨ Não fecha automaticamente ao terminar

- 🔧 Script de build otimizado

---- 🔧 Exclusão de módulos desnecessários



## 📝 Changelog### v1.0 (Anterior)



### v3.0 (Atual - Novembro 2025)- Interface básica com Tkinter

- Questionário funcional

**Novidades:**- Classificação de risco

- ✨ Adicionado Eixo 5 (Percepção do Problema) com 5 novas perguntas

- ✨ **Histórico detalhado** com visualização de todas as respostas---

- ✨ **Justificativas das perguntas** aparecem no histórico

- ✨ Separação em plataformas (Windows/Linux)**Versão**: 2.0

- ✨ Windows: Tkinter (sem dependências externas)**Última atualização**: Novembro de 2025

- ✨ Linux: PySide6 (componentes Qt nativos)**Plataforma**: Windows 7+

- 🔧 Pontuação dinâmica (peso_sim e peso_nao)**Linguagem**: Python 3.8+

- 🔧 Barra de progresso redimensionável
- 🐛 Corrigido redimensionamento de componentes

### v2.0
- Interface redesenhada
- Sistema de histórico
- Barra de progresso visual
- Cores por nível de risco

### v1.0
- Interface básica
- Questionário funcional
- Classificação simples

---

**Versão**: 3.0
**Última atualização**: Novembro de 2025
**Plataformas**: Windows (Tkinter) | Linux/WSL (PySide6)
**Linguagem**: Python 3.8+
**Licença**: Educacional
````
