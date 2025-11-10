# 📦 Guia de Build - Sistema DSM-5# 📦 Guia de Build Otimizado - Windows

## Windows - Gerar Executável## ⚡ Método Rápido (Recomendado)

### Método Rápido (3 passos)No **PowerShell ou CMD.exe** (no Windows, não use WSL):

#### 1️⃣ Abra o **Prompt de Comando (CMD)**```powershell

# 1. Instale PyInstaller

Procure por "cmd" no Windows e abra.pip install --upgrade pip pyinstaller

#### 2️⃣ Instale PyInstaller (primeira vez)# 2. Gere o executável otimizado

python build_optimized.py

`cmd`

pip install pyinstaller

```O `.exe`estará em`dist\main_windows_tk.exe`

#### 3️⃣ Navegue até a pasta e gere o executável---

```cmd## 🔧 Método Alternativo com .spec

cd C:\caminho\para\python-SE\windows

pyinstaller --onefile --windowed --add-data "questions.json;." main.pySe preferir usar o arquivo `.spec` customizado:

```

````powershell

**Pronto!** O executável estará em: `dist\main.exe`# Gere o executável usando o spec

pyinstaller main_windows_tk.spec

---```



## Windows - Build com Otimizações---



Se quiser um arquivo .exe menor (~40-50 MB):## 📊 O que foi otimizado



```cmd✅ **Tkinter apenas** - Nenhuma biblioteca externa (PySide6, PyQt, etc)

cd C:\caminho\para\python-SE\windows✅ **Módulos excluídos** - pip, setuptools, email, http, urllib, unittest, etc

pyinstaller --onefile --windowed ^✅ **Arquivo único** - `--onefile` para facilitar distribuição

  --exclude-module=numpy ^✅ **Sem console** - `--windowed` para app profissional

  --exclude-module=pandas ^✅ **Tamanho mínimo** - Espera-se ~30-40 MB

  --exclude-module=scipy ^

  --exclude-module=matplotlib ^---

  --add-data "questions.json;." ^

  main.py## ✨ Checklist pré-build

````

- [ ] `main_windows_tk.py` existe e funciona (`python main_windows_tk.py`)

**Nota**: Se o `^` (quebra de linha) não funcionar, coloque tudo em uma linha:- [ ] `questions.json` está no mesmo diretório

- [ ] PyInstaller instalado (`pip list | grep pyinstaller`)

````cmd- [ ] Windows 7+

pyinstaller --onefile --windowed --exclude-module=numpy --exclude-module=pandas --exclude-module=scipy --exclude-module=matplotlib --add-data "questions.json;." main.py

```---



---## 🎯 Se tiver problemas



## Explicação dos Parâmetros**Erro: "questions.json not found"**



| Parâmetro | Significado |- Verifique se o arquivo está no mesmo diretório de `main_windows_tk.py`

|-----------|------------|- Regenere com: `pyinstaller --clean main_windows_tk.spec`

| `--onefile` | Gera um único executável (mais fácil distribuir) |

| `--windowed` | Sem janela de console (mais profissional) |**Executável muito grande (>80 MB)?**

| `--exclude-module=X` | Remove biblioteca X do build (deixa menor) |

| `--add-data "questions.json;."` | Inclui o arquivo JSON no executável |- Verifique se tem DLLs extras em `dist\`

| `main.py` | Arquivo principal a ser compilado |- Remova manualmente se necessário

- Execute: `python build_optimized.py` novamente

---

**Windows SmartScreen warning?**

## Troubleshooting

- É normal para executáveis não assinados

### ❌ Erro: "pyinstaller: command not found"- Clique em "Executar de qualquer forma"

**Solução**: Instale o PyInstaller:- Para remover, você precisaria de um certificado de código (pago)

```cmd

pip install pyinstaller---

````

## 📝 Comandos úteis

### ❌ Erro: "questions.json not found"

**Solução**: Verifique se o arquivo existe na pasta `windows/````powershell

```cmd# Ver tamanho do executável

dir questions.json(Get-Item "dist\main_windows_tk.exe").Length / 1MB

```

# Limpar builds anteriores

### ❌ Executável muito grande (>100 MB)Remove-Item -Recurse -Force build, dist, "\*.spec"

**Solução**: Use o método com otimizações (exclude-module)

# Listar módulos incluídos (debug)

### ❌ Windows SmartScreen avisa "App não verificado"pyinstaller -c main_windows_tk.py # cria um com console

**Solução**: Clique em "Executar de qualquer forma" - é normal para apps não assinados```

### ❌ Erro com "^" no PowerShell

**Solução**: Use `cmd.exe` ao invés de PowerShell, ou coloque tudo em uma linha

---

## Linux - Gerar Executável

```bash
cd ~/python-SE/linux
pip install pyinstaller
pyinstaller --onefile --add-data "questions.json:." main.py
```

O executável estará em: `linux/dist/main`

**Nota**: No Linux é mais comum rodar direto com Python:

```bash
pip install PySide6
python main.py
```

---

## Verificar Resultado

### Windows

Procure por `main.exe` na pasta:

```
python-SE\windows\dist\main.exe
```

Dê um duplo clique para executar!

### Linux

Execute:

```bash
./linux/dist/main
```

---

## Tamanho Esperado dos Arquivos

| Plataforma | Método    | Tamanho    |
| ---------- | --------- | ---------- |
| Windows    | Simples   | ~50 MB     |
| Windows    | Otimizado | ~40 MB     |
| Linux      | Otimizado | ~80-100 MB |

---

## Dicas Extras

### 🔄 Regenerar após mudanças no código

Sempre que modificar `main.py`, `data_manager.py`, etc., regenere o executável:

```cmd
cd windows
pyinstaller --onefile --windowed --add-data "questions.json;." main.py
```

### 📁 Limpar builds antigos

Para remover builds anteriores:

```cmd
rmdir /s dist build
del main.spec
```

### ✅ Testar antes de fazer build

Sempre teste a aplicação antes:

```cmd
cd windows
python main.py
```

---

## Próximos Passos

✅ Build concluído? Distribua o arquivo `main.exe` para usuários!  
Eles não precisam instalar Python ou nenhuma dependência.

---

**Última atualização**: Novembro 2025
