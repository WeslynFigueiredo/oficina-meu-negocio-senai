<div align="center">

# 💡 Oficina: Meu Negócio — SENAI

### Entrevista Guiada de Plano de Negócio com Diagnóstico Inteligente por IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://oficina-meu-negocio-senai.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%20Lite-orange?style=for-the-badge&logo=googlegemini&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Engine-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Produção-success?style=for-the-badge)

<p align="center">
  <b>Aplicação Web Mobile-First desenvolvida para o Feirão de Empregabilidade 2026 do SENAI.</b><br>
  Oficina ministrada pela instrutora <b>Alene Petrina</b>.
</p>

[🌐 Acessar a Aplicação Online](https://oficina-meu-negocio-senai.streamlit.app) • [📱 Acesso via QR Code](#-acesso-rápido-via-qr-code)

</div>

---

## 🎯 Sobre o Projeto

Durante workshops presenciais com rotações curtas (15 a 20 minutos), preencher fichas extensas em papel gera atrito e reduz o tempo de discussão prática. Esta aplicação digitaliza e dinamiza essa etapa:

* **Interface Conversacional Passo a Passo:** Conduz equipes através de 5 perguntas centrais com barra de progresso em tempo real e assistente virtual interativo.
* **Avaliação Imediata com IA:** A API do **Google Gemini** analisa a proposta e gera um diagnóstico sintetizado com Termômetro de Viabilidade, Pontos Fortes, Atenção e Dica Prática de MVP.
* **Exportação Pronta em PDF:** Os alunos baixam o documento com a ficha e o parecer formatados diretamente para o celular em um único clique.

---

## 🚀 Demonstração do Fluxo da Aplicação

```text
[ Etapa 1: Nome ] ➔ [ Etapa 2: Problema/Valor ] ➔ [ Etapa 3: Cliente ] ➔ [ Etapa 4: Diferencial ] ➔ [ Etapa 5: Preço/Canal ]
                                                                                                        │
                                                                                                        ▼
[ 📥 Baixar PDF ] ◄── [ 📊 Parecer de Viabilidade ] ◄── [ 🤖 Google Gemini API ] ◄── [ 📋 Revisão Geral ]
```

---

## 🛠️ Tecnologias e Arquitetura

| Camada | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Interface / Frontend** | [Streamlit](https://streamlit.io/?utm_source=gemini) | Interface reativa orientada a estados (`st.session_state`), otimizada para celular |
| **Motor de IA** | [Google Generative AI](https://ai.google.dev/?utm_source=gemini) | Cadeia de modelos resiliente com prioridade em `gemini-3.5-flash-lite` |
| **Resiliência e Quotas** | Algoritmo de Backoff | Tratamento específico para limitação de taxa (HTTP 429) e alternância automática de modelos |
| **Geração de Documentos** | [ReportLab](https://www.reportlab.com/?utm_source=gemini) | Construção em memória (`BytesIO`) de relatórios PDF com formatação institucional |
| **Deploy & Hospedagem** | [Streamlit Community Cloud](https://streamlit.io/cloud?utm_source=gemini) | Integração contínua e distribuição pública via GitHub |

---

## 🧠 Arquitetura de Resiliência de IA

Para assegurar que as equipes submetam seus projetos simultaneamente sem interrupções por limites da API:

1. **Gestão de Quota:** Utilização dos modelos *Flash Lite* com limite elevado de requisições diárias (500 RPD).
2. **Cadeia de Reserva Automática (Fallback):**
   * `gemini-3.5-flash-lite` (Prioridade)
   * `gemini-3.1-flash-lite` (Reserva Primária)
   * `gemini-2.5-flash-lite` (Reserva Secundária)
   * `gemini-1.5-flash` (Reserva Final)
3. **Retentativas Inteligentes:** Gestão de erros HTTP 429 com pausas adaptativas e aviso visual amigável (`st.toast`).

---

## 💻 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/WeslynFigueiredo/oficina-meu-negocio-senai.git
cd oficina-meu-negocio-senai
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar os segredos locais
Crie o arquivo `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "SUA_CHAVE_DO_GOOGLE_AI_STUDIO"
```

### 4. Iniciar a aplicação
```bash
python -m streamlit run app.py
```

---

## 📱 Acesso Rápido via QR Code

Para apresentações em telões ou slides de abertura, aponte a câmera do celular para o código abaixo:

<div align="center">
  <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://oficina-meu-negocio-senai.streamlit.app" alt="QR Code da Aplicação" width="180" />
  <p><b>https://oficina-meu-negocio-senai.streamlit.app</b></p>
</div>
