# 🛸 LunarGuard — Sistema de Monitoramento Visual de Base Lunar

> FIAP Global Solution 2025 · Space Connect · Tecnologia Espacial Aplicada a Desafios Reais

---

## 📌 Descrição da Solução

A NASA e empresas privadas planejam bases lunares permanentes com presença humana contínua e operação parcialmente remota da Terra. Nesse cenário, um sistema de vigilância inteligente é essencial para garantir a segurança dos astronautas e da infraestrutura crítica.

**LunarGuard** é um sistema de monitoramento visual em tempo real que:

- **Detecta movimento** em câmeras de vigilância da base usando subtração de fundo (MOG2)
- **Define zonas restritas** (ex: Núcleo de Controle, Reator de Energia) e alerta quando há intrusão
- **Detecta quedas e colapso** de astronautas usando análise de pose corporal (MediaPipe Pose)
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
     └──► MediaPipe Pose → Análise de Landmarks → Detecção de Queda
     │
     ▼
Overlay HUD + Alertas Visuais → Exibição
```

---

## 📦 Bibliotecas Utilizadas

| Biblioteca | Uso |
|---|---|
| `opencv-python` | Captura de vídeo, background subtraction, desenho, exibição |
| `mediapipe` | Detecção de pose corporal (skeleton landmarks) |
| `numpy` | Operações auxiliares de array |

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
| `Q` | Sair |
| `R` | Resetar o background subtractor (útil ao mudar de cena) |
| `Z` | Mostrar/ocultar as zonas de segurança |

---

### 7. Desativar o ambiente virtual (quando terminar)

```bash
deactivate
```

---

## 🗂️ Estrutura do Projeto

```
lunarguard/
├── main.py                 # Entry point principal
├── requirements.txt
├── README.md
├── detector/
│   ├── motion.py           # Detecção de movimento (MOG2 + contornos)
│   ├── zone.py             # Gerenciamento de zonas restritas
│   └── pose.py             # Detecção de queda via MediaPipe Pose
└── ui/
    └── overlay.py          # HUD, alertas e desenho sobre o frame
```

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| Nome do integrante 1 | RM00000 |
| Nome do integrante 2 | RM00000 |
| Nome do integrante 3 | RM00000 |

---

## 🔗 Contexto — FIAP Global Solution 2025

Este projeto foi desenvolvido como resposta ao desafio **Space Connect**, que propõe o uso de tecnologia, dados e inovação para resolver desafios da Terra e ampliar as possibilidades da economia espacial. O LunarGuard conecta diretamente o problema de segurança em bases lunares com aplicações práticas em infraestruturas críticas terrestres.
