# 🛸 LunarGuard — Sistema de Monitoramento Visual de Base Lunar

> FIAP Global Solution 2026 · Space Connect · Tecnologia Espacial Aplicada a Desafios Reais

---

## 🎬 Demo

[![LunarGuard Demo](https://img.shields.io/badge/YouTube-Demo-red?logo=youtube)](https://youtu.be/QNgEQvthIrE)

> Assista à demonstração completa do sistema funcionando em tempo real.

---

## 📌 Descrição da Solução

A NASA e empresas privadas planejam bases lunares permanentes com presença humana contínua e operação parcialmente remota da Terra. Nesse cenário, um sistema de vigilância inteligente é essencial para garantir a segurança dos astronautas e da infraestrutura crítica.

**LunarGuard** é um sistema de monitoramento visual em tempo real que:

- **Detecta movimento** em câmeras de vigilância da base usando subtração de fundo (MOG2)
- **Define zonas restritas** (ex: Núcleo de Controle, Reator de Energia) e alerta quando há intrusão
- **Detecta quedas e colapso** de astronautas usando análise de pose corporal (MediaPipe Pose)
- **Detecta inconsciência** pelo fechamento prolongado dos olhos (MediaPipe Face Landmarker + EAR)
- Exibe um **HUD temático** com status em tempo real, indicadores e alertas visuais

A mesma tecnologia tem aplicação direta na Terra em: fábricas, data centers, hospitais, mineradoras e qualquer instalação crítica.

---

## 🧠 Pipeline de Visão Computacional

```
Câmera/Vídeo
     │
     ▼
Captura de Frame (OpenCV)
     │
     ├──► MOG2 Background Subtraction → Detecção de Movimento → Bounding Boxes
     │         │
     │         └──► Verificação de Zonas Restritas → Alerta de Intrusão
     │
     ├──► MediaPipe Pose → Análise de Landmarks → Detecção de Queda
     │
     └──► MediaPipe Face → EAR (Eye Aspect Ratio) → Detecção de Inconsciência
     │
     ▼
Overlay HUD + Alertas Visuais → Exibição
```

---

## 📦 Bibliotecas Utilizadas

| Biblioteca | Uso |
|---|---|
| `opencv-python` | Captura de vídeo, background subtraction, desenho, exibição |
| `mediapipe` | Detecção de pose corporal e landmarks faciais |
| `numpy` | Operações auxiliares de array |
| `screeninfo` | Resolução do monitor para modo tela cheia |

---

## ⚙️ Instalação e Execução

### 1. Pré-requisitos

- Python **3.10** ou superior instalado
- Git instalado
- Webcam disponível (ou um arquivo de vídeo `.mp4`)

---

### 2. Clone o repositório

```bash
git clone https://github.com/Gabriel-Leao/lunarguard.git
cd lunarguard
```

---

### 3. Crie e ative o ambiente virtual

#### 🍎 Mac / 🐧 Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🪟 Windows (Prompt de Comando)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### 🪟 Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> ⚠️ No PowerShell, caso apareça um erro de permissão, execute antes:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

Após ativar, o terminal exibirá o prefixo `(venv)` no início da linha.

---

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

> Na primeira execução, o sistema baixa automaticamente os modelos do MediaPipe (~28 MB no total).

---

### 5. Execute o projeto

```bash
# Webcam padrão
python main.py

# Segunda câmera (caso a padrão não seja a correta)
python main.py --source 1

# Arquivo de vídeo
python main.py --source caminho/para/video.mp4
```

---

### 6. Teclas durante a execução

| Tecla | Ação |
|---|---|
| `Z` | Mostrar/ocultar zonas e legenda |
| `F` | Alternar tela cheia |
| `R` | Resetar o background |
| `Q` | Sair |

---

### 7. Desativar o ambiente virtual (quando terminar)

```bash
deactivate
```

---

## 🗂️ Estrutura do Projeto

```
lunarguard/
├── main.py
├── requirements.txt
├── README.md
├── detector/
│   ├── motion.py       # Detecção de movimento (MOG2)
│   ├── zone.py         # Zonas restritas
│   ├── pose.py         # Detecção de queda (MediaPipe Pose)
│   └── blink.py        # Detecção de inconsciência (MediaPipe Face + EAR)
└── ui/
    └── overlay.py      # HUD, alertas e desenho sobre o frame
```

---

## Membros do Grupo

| Nome                                  | RM     |
| ------------------------------------- | ------ |
| **Gabriel Leão da Silva**             | 552642 |
| **Matheus Farias de Lima**            | 554254 |
| **Miguel Mauricio Parrado Patarroyo** | 554007 |
| **Pedro Henrique Nardaci Chaves**     | 553988 |
| **Vitor Pinheiro Nascimento**         | 553693 |

---

## 🔗 Contexto — FIAP Global Solution 2026

Este projeto foi desenvolvido como resposta ao desafio **Space Connect**, que propõe o uso de tecnologia, dados e inovação para resolver desafios da Terra e ampliar as possibilidades da economia espacial. O LunarGuard conecta diretamente o problema de segurança em bases lunares com aplicações práticas em infraestruturas críticas terrestres.