<div align="center">

<img src="ORION.png" alt="Logo do ORION" width="260"/>

# 🌌 ORION – Assistente Inteligente de Carreira  

Iluminando seu próximo passo profissional usando **dados, IA leve e muito foco em gente**.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/status-ativo-success)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

</div>

---

## 💡 O que é o ORION?

O **ORION** é uma aplicação construída em **Python + Streamlit** que ajuda pessoas a:

- entender o **risco de automação** da sua área/emprego,
- refletir sobre **novos caminhos de carreira**,  
- enxergar melhor suas **competências técnicas e comportamentais**,  
- receber **trilhas de aprendizado** sugeridas para se atualizar.

O foco é **tecnologia a serviço do humano**: nada de “substituir pessoas”, e sim apoiar decisões de estudo, transição e desenvolvimento.

---

## 🧠 Funcionalidades principais

### 1. Preenchimento manual

O usuário informa:

- Nome e idade  
- Profissão/emprego atual  
- Área de atuação / área de interesse  
- Interesses (ex.: dados, pessoas, negócios, criatividade, sustentabilidade…)  
- Competências técnicas (0 a 10)  
- Competências comportamentais (0 a 10)

O ORION:

- estima o **risco de automação**,
- gera um **texto explicativo humanizado**,
- sugere **carreiras compatíveis**,
- monta uma **trilha de estudos**,
- permite baixar tudo em **`.txt`**.

---

### 2. Análise automática via LinkedIn

Além do modo manual, o app tem uma aba chamada **“Usar dados do LinkedIn”**, onde o usuário pode:

- colar o texto da seção **“Sobre”** / experiências, **ou**
- fazer upload do **arquivo `.zip` de exportação de dados do LinkedIn**  
  (aquele pacote oficial cheio de arquivos `.csv`).

O ORION então:

- lê os textos relevantes (Profile Summary, Skills, Positions, etc.),  
- detecta a **área de atuação**,
- identifica **interesses e palavras-chave**,
- sugere **competências técnicas e soft skills**,
- gera o mesmo relatório completo, de forma automática.

---

## 🛠️ Tecnologias usadas

- **Python 3.12**
- **Streamlit** (interface web)
- **Pandas / CSV / ZIP** para leitura dos dados do LinkedIn
- **HTML + CSS embutido** para componentes visuais (barras de risco, layout, etc.)

---

## 🚀 Como rodar o projeto localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/nandoalmeidam/ORION.git
cd ORION

# 2. (Opcional) Criar ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar a aplicação
streamlit run app.py
