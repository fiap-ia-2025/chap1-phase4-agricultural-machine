# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="img/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%">
  </a>
</p>


## 👥 Grupo XX
<!-- Nome oficial do grupo, se houver. Pode usar um nome criativo também -->

## 👨‍🎓 Integrantes:
- Amanda Vieira Pires (RM565045)
- Ana Gabriela Soares Santos (RM565235)
- Bianca Nascimento de Santa Cruz Oliveira (RM561390)
- Milena Pereira dos Santos Silva (RM565464)
- Nayana Mehta Miazaki (RM565045) 

## 👩‍🏫 Professores:
### Tutor(a)  
-  Lucas Gomes Moreira
### Coordenador(a)  
- André Godoi

---

# 🌿 Sistema de Irrigação Inteligente com ESP32

## 📘 Descrição Geral

Este projeto faz parte de uma solução integrada de **irrigação inteligente com ESP32**, desenvolvida como atividade prática no curso da FIAP. Seu principal objetivo é aplicar conceitos de **automação agrícola**, **monitoramento ambiental**, **programação embarcada** e **persistência de dados**, simulando um cenário real de controle e otimização do uso da água em plantações.

A atividade foi dividida em duas frentes complementares:

1. **Entrega 1 — Monitoramento físico e lógica de irrigação com ESP32**   
   Foco na criação do sistema físico (simulado via Wokwi), que coleta dados do solo e aciona a irrigação automaticamente quando necessário.

 2. **Entrega 2 — Armazenamento, CRUD e API climática e Dashboard em Python**   
   Foco na manipulação dos dados coletados, integração com uma API pública de clima e visualização gráfica dos dados.


## 🎯 Objetivo Geral

Construir uma solução digital de irrigação que seja:
- Sensível às condições reais do solo e clima
- Capaz de tomar decisões autônomas sobre irrigação
- Preparada para armazenar e visualizar dados históricos
- Inteligente o suficiente para considerar informações externas (como previsão de chuva) antes de ativar a bomba
- Fácil de interpretar visualmente através de um dashboard interativo


## 🔧 Entrega 1 — Monitoramento Físico e Lógica de Controle com ESP32

Esta etapa foca na construção de um sistema físico/simulado de irrigação baseado em sensores e lógica embarcada com ESP32, utilizando a IDE VS Code, PlatformIO e a extensão do Wokwi.

### Variáveis monitoradas:

| Variável              | Simulação/Componente             |
|-----------------------|----------------------------------|
| Umidade do solo       | Sensor DHT22                     |
| pH do solo            | Sensor LDR (com conversão para escala 0–14) |
| Presença de fósforo   | Botão com `INPUT_PULLUP`         |
| Presença de potássio  | Botão com `INPUT_PULLUP`         |
| Bomba de irrigação    | LED (simula relé e bomba d’água) |

### Lógica implementada:

- A bomba de irrigação é acionada **somente quando a umidade do solo está abaixo de 40%**.
- A leitura do pH é feita com um LDR analógico e normalizada para a escala 0 a 14 apenas para exibição informativa.
- Os botões simulam a ausência dos nutrientes fósforo e potássio, mas **não afetam diretamente a lógica de irrigação**.
- O LED conectado ao GPIO2 representa visualmente o estado da bomba d’água (ligado = irrigando).

### Tecnologias utilizadas:

- **ESP32 Dev Module** como microcontrolador
- **PlatformIO** com VS Code para desenvolvimento estruturado em C++
- **Wokwi Extension** para simulação do circuito (`diagram.json`) diretamente dentro do VS Code
- **Biblioteca `DHT` da Adafruit**


## 💾 Entrega 2 — Armazenamento de Dados, CRUD e Integração com API Climática (em construção)

Nesta segunda fase do projeto, a equipe irá complementar a solução com uma camada de **persistência e inteligência contextual**, que envolve:

- Captura dos dados exibidos no monitor serial (simulando a coleta real de dados ambientais)
- **Armazenamento local em banco de dados relacional** simulado com Python e SQLite
- Implementação das operações **CRUD** (Create, Read, Update, Delete) sobre as leituras
- Integração com uma **API pública de clima** (como a OpenWeather), permitindo:
  - Obter temperatura, umidade do ar e previsão de chuva em tempo real
  - Enriquecer a lógica de irrigação com base em condições externas (ex: se vai chover, a irrigação pode ser adiada)
- Visualização opcional por meio de **dashboard em Python** com bibliotecas como `matplotlib`, `streamlit` ou `seaborn`, trazendo clareza para o usuário final sobre o comportamento do sistema

📌 *Essa etapa será completada e documentada pela segunda parte do grupo.*

## 📁 Estrutura do Projeto

```bash
/chap1-phase3-agricultural-machine
├── parte1_esp32/               # Entrega 1: sistema físico com ESP32
│   ├── src/
│   │   └── main.cpp
│   ├── diagram.json            # Circuito simulado no Wokwi
│   ├── platformio.ini          # Configuração do PlatformIO
│   ├── wokwi.toml              # Caminho para firmware na simulação
│
├── parte2_python/              # Entrega 2: scripts em Python
│   ├── crud_e_armazenamento.py
│   ├── integracao_api_clima.py
│   ├── dashboard.py
│
├── img/                        # Imagens utilizadas no README
│   ├── circuito_diagrama.png   # Print do circuito no Wokwi
│   ├── logo_fiap.png           # Logo da faculdade
│
├── .gitignore                  # Arquivos/pastas ignorados pelo Git
└── README.md                   # Documentação geral do projeto
```
## ▶️ Como Rodar o Projeto

### ✅ Requisitos

- [Visual Studio Code (VS Code)](https://code.visualstudio.com/)
- Extensões instaladas no VS Code:
  - **PlatformIO IDE** (ícone da formiguinha 🐜)
  - **Wokwi for VS Code** (ícone com `<>` da simulação)
- Git instalado na máquina (para clonar o repositório)

---

### 🔧 Passo a Passo

1. **Clone o repositório do projeto**
   - Abra o terminal (ou terminal integrado do VS Code)
   - Execute o comando:

     ```bash
     git clone https://github.com/fiap-ia-2025/chap1-phase3-agricultural-machine
     ```


2. **Compile o projeto com PlatformIO**
   - No VS Code, clique no ícone da formiguinha 🐜 (PlatformIO)
   - Clique em **"Build"** para compilar o `main.cpp`

3. **Execute a simulação com Wokwi**
   - Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac) para abrir a Command Palette
   - Digite `>Wokwi: Start Simulation` e pressione Enter
   - A simulação será aberta no navegador com o firmware já compilado

   > Obs: certifique-se de que o projeto foi compilado primeiro com o botão **Build** do PlatformIO.


4. **Acompanhe os dados no Monitor Serial**
   - O monitor serial da simulação mostrará:
     - Umidade lida pelo DHT22
     - Valor de pH (simulado via LDR)
     - Presença/ausência de fósforo e potássio (botões)
     - Estado da bomba (ligada ou desligada)
    
     [Adicionar parte em python]

---

### 🧪 Dicas para testar

- **Botões pressionados = nutriente ausente**
- **LDR e DHT22** podem ser alterados em tempo real na simulação clicando sobre eles
- A bomba (LED) **acende somente se a umidade estiver abaixo de 40%**


## ✅ Conclusão

O projeto consolida a aplicação prática de tecnologias embarcadas, sensores, automação e ciência de dados para resolver um problema real da agricultura: **o uso eficiente e inteligente da água.** Ao combinar sensores físicos, lógica de controle, banco de dados e integração com fontes externas de informação, a solução oferece um modelo funcional de **agricultura de precisão** em nível educacional.

O desenvolvimento foi feito com foco em clareza, modularidade, boas práticas e documentação, refletindo tanto o aprendizado técnico quanto a capacidade de estruturar soluções completas em equipe.

