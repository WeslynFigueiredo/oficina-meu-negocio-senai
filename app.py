import streamlit as st
import google.generativeai as genai
import time
import os
import re
from io import BytesIO

# Importações do ReportLab para geração de PDF em memória
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuração da página Streamlit (Mobile-first & Single Screen no Desktop)
st.set_page_config(
    page_title="Oficina: Meu Negócio - SENAI",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização customizada em CSS: Otimizada para Single Screen no PC e Responsiva no Celular
st.markdown("""
<style>
    /* Transição suave entre etapas */
    @keyframes fadeInSlide {
        0% {
            opacity: 0;
            transform: translateY(10px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .step-card-animated {
        animation: fadeInSlide 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Container Principal */
    .main .block-container {
        padding-top: 0.6rem;
        padding-bottom: 1rem;
        max-width: 620px;
    }

    /* Header do Evento SENAI */
    .header-card {
        background: linear-gradient(135deg, #003366 0%, #0055a5 100%);
        color: white;
        padding: 0.9rem 1rem;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.15);
    }
    .header-card h1 {
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
        line-height: 1.2;
    }
    .header-badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        padding: 0.15rem 0.65rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* Mascote Interativo do SENAI */
    .mascot-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0, 85, 165, 0.06);
    }
    .mascot-avatar {
        font-size: 2.2rem;
        background: #FFFFFF;
        border-radius: 50%;
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0, 51, 102, 0.12);
        animation: floatMascot 3s ease-in-out infinite;
        flex-shrink: 0;
    }
    @keyframes floatMascot {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-3px) rotate(3deg); }
    }
    .mascot-speech {
        font-size: 0.86rem;
        font-weight: 600;
        color: #1E3A8A;
        line-height: 1.3;
    }

    /* Card da Pergunta */
    .step-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.2rem 1.2rem;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }
    .step-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }
    .step-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 0.8rem;
    }

    /* Cards de Resumo */
    .review-item {
        background-color: #F8FAFC;
        border-left: 4px solid #0055a5;
        border-radius: 6px;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.6rem;
    }
    .review-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
        color: #64748B;
    }
    .review-value {
        font-size: 0.92rem;
        font-weight: 600;
        color: #1E293B;
        margin-top: 0.15rem;
    }

    /* Botões Otimizados */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 0.9rem;
    }

    /* Ajustes específicos para Telas Grandes (Desktop Single Screen sem Scroll) */
    @media (min-height: 600px) and (min-width: 769px) {
        .main .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0.4rem !important;
        }
        .header-card {
            padding: 0.65rem 0.8rem !important;
            margin-bottom: 0.5rem !important;
        }
        .header-card h1 {
            font-size: 1.25rem !important;
        }
        .mascot-box {
            padding: 0.5rem 0.8rem !important;
            margin-bottom: 0.6rem !important;
        }
        .mascot-avatar {
            width: 40px !important;
            height: 40px !important;
            font-size: 1.8rem !important;
        }
        .step-container {
            padding: 1rem 1.1rem !important;
            margin-top: 0.3rem !important;
            margin-bottom: 0.6rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da aplicação (st.session_state)
if "step" not in st.session_state:
    st.session_state.step = 1
if "nome_negocio" not in st.session_state:
    st.session_state.nome_negocio = ""
if "oferta_problema" not in st.session_state:
    st.session_state.oferta_problema = ""
if "cliente" not in st.session_state:
    st.session_state.cliente = ""
if "diferencial" not in st.session_state:
    st.session_state.diferencial = ""
if "preco_canal" not in st.session_state:
    st.session_state.preco_canal = ""
if "relatorio" not in st.session_state:
    st.session_state.relatorio = None

# Topo / Header Fixo da Aplicação
st.markdown("""
<div class="header-card">
    <h1>💡 Oficina: Meu Negócio</h1>
    <div style="font-size: 0.9rem; opacity: 0.95;">Entrevista Guiada de Plano de Negócio</div>
    <div class="header-badge">🏭 SENAI • Feirão de Empregabilidade 2026</div>
    <div style="font-size: 0.8rem; margin-top: 0.25rem; opacity: 0.85;">Instrutora: Alene Petrina</div>
</div>
""", unsafe_allow_html=True)

# Leitura segura da chave de API do Gemini
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")

if not api_key or api_key == "SUA_CHAVE_AQUI":
    st.warning("⚠️ **Chave de API não configurada.**")
    st.info("Para utilizar a inteligência artificial, configure o arquivo `.streamlit/secrets.toml` com a sua `GEMINI_API_KEY` ou insira uma chave temporária abaixo:")
    api_key_input = st.text_input("Sua GEMINI_API_KEY (temporária):", type="password")
    if api_key_input:
        api_key = api_key_input.strip()

# Função para chamar a API do Gemini com fallback de modelos e retry em caso de Rate Limit (429)
def gerar_parecer_gemini(nome_negocio, oferta_problema, cliente, diferencial, preco_canal, api_key_val):
    genai.configure(api_key=api_key_val)
    
    prompt = f"""
Você é um consultor sênior especialista em empreendedorismo, inovação e modelos de negócios do SENAI.
Sua função é avaliar fichas simplificadas de plano de negócio preenchidas por alunos durante a oficina ministrada pela instrutora Alene Petrina no evento "Feirão de Empregabilidade 2026".

Dados do projeto fornecidos pelo aluno:
1. Nome do Negócio: {nome_negocio}
2. O que oferece e qual problema resolve: {oferta_problema}
3. Cliente principal: {cliente}
4. Diferencial da proposta: {diferencial}
5. Preço estimado e canal de venda: {preco_canal}

Gere um mini-relatório/parecer didático, encorajador, prático e direto ao ponto (máximo de 10 a 12 linhas no total).

Responda OBRIGATORIAMENTE no seguinte formato Markdown:

### 📊 Termômetro de Viabilidade
[Insira Apenas UMA das opções exatamente como escrito: 🟢 Alta Viabilidade | 🟡 Promissora com Ajustes | 🔴 Rever Proposta]

### 🔎 Diagnóstico Geral
[Insira 2 frases resumindo o conceito do negócio e sua viabilidade prática no mercado atual]

### 💪 Ponto Forte
- [Insira 1 item destacado com o principal diferencial ou vantagem competitiva do projeto]

### ⚠️ Ponto de Atenção
- [Insira 1 item destacando o principal desafio, risco ou gargalo a ser superado]

### 🚀 Dica Prática de MVP
- [Insira 1 ação imediata, simples e de baixíssimo custo para testar a ideia hoje no mundo real]
"""

    candidate_models = [
        "gemini-3.5-flash-lite", 
        "gemini-3.1-flash-lite", 
        "gemini-2.5-flash-lite", 
        "gemini-1.5-flash"
    ]
    max_retries_per_model = 3
    last_exception = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as model_init_err:
            last_exception = model_init_err
            continue

        for attempt in range(max_retries_per_model):
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                is_rate_limit = any(k in error_str for k in ["429", "quota", "resourceexhausted", "limit"])

                if is_rate_limit:
                    if attempt < max_retries_per_model - 1:
                        wait_time = 8 + (attempt * 2)  # 8 a 10 segundos
                        st.toast(
                            f"⏳ Muitas ideias sendo analisadas ao mesmo tempo! Aguardando {wait_time}s na fila...", 
                            icon="⏳"
                        )
                        time.sleep(wait_time)
                    else:
                        st.toast(
                            f"🔄 Limite temporário no modelo {model_name}. Alternando para modelo reserva...", 
                            icon="🔄"
                        )
                        break
                else:
                    st.toast(
                        f"⚠️ Indisponibilidade no modelo {model_name}. Alternando para modelo reserva...", 
                        icon="⚠️"
                    )
                    break

    if last_exception:
        raise last_exception
    else:
        raise RuntimeError("Não foi possível obter resposta de nenhum dos modelos disponíveis.")

# Função auxiliar para gerar relatório em PDF em memória via ReportLab
def gerar_pdf_relatorio(nome_negocio, oferta, cliente, diferencial, preco, relatorio_markdown):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#003366'),
        fontName='Helvetica-Bold',
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0055A5'),
        fontName='Helvetica-Bold',
        spaceAfter=10
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#003366'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4
    )

    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569'),
        fontName='Helvetica-Bold'
    )

    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica'
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica',
        spaceAfter=4
    )

    elements = []

    # Cabeçalho Oficial SENAI
    elements.append(Paragraph("SENAI • Feirão de Empregabilidade 2026", title_style))
    elements.append(Paragraph("Oficina: Meu Negócio | Instrutora: Alene Petrina", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#003366'), spaceAfter=10))

    # Seção 1: Resumo dos Dados do Negócio
    elements.append(Paragraph("📋 Resumo da Ficha de Negócio", section_heading))

    dados_tabela = [
        [Paragraph("Nome do Negócio", label_style), Paragraph(nome_negocio, value_style)],
        [Paragraph("Oferta / Problema", label_style), Paragraph(oferta, value_style)],
        [Paragraph("Cliente Principal", label_style), Paragraph(cliente, value_style)],
        [Paragraph("Diferencial", label_style), Paragraph(diferencial, value_style)],
        [Paragraph("Preço e Canal", label_style), Paragraph(preco, value_style)]
    ]

    tabela = Table(dados_tabela, colWidths=[120, 400])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1'))
    ]))
    
    elements.append(tabela)
    elements.append(Spacer(1, 10))

    # Seção 2: Diagnóstico e Parecer da IA
    elements.append(Paragraph("🤖 Parecer de Viabilidade da IA SENAI", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#0055A5'), spaceAfter=8))

    lines = relatorio_markdown.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        # Formatação simples de negrito para ReportLab Paragraph
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_str)
        
        if line_str.startswith('### '):
            h_text = line_str.replace('### ', '')
            h_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', h_text)
            elements.append(Paragraph(f"<b>{h_text}</b>", ParagraphStyle(
                'SubHeading', parent=section_heading, fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor('#0055A5')
            )))
        elif line_str.startswith('- '):
            b_text = formatted_line[2:]
            elements.append(Paragraph(f"• {b_text}", body_style))
        else:
            elements.append(Paragraph(formatted_line, body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# Função de reset para iniciar um novo teste
def reiniciar_formulario():
    st.session_state.step = 1
    st.session_state.nome_negocio = ""
    st.session_state.oferta_problema = ""
    st.session_state.cliente = ""
    st.session_state.diferencial = ""
    st.session_state.preco_canal = ""
    st.session_state.relatorio = None
    st.rerun()

# Função auxiliar para renderizar o Mascote SENAI
def renderizar_mascote(avatar_emoji, fala_texto):
    st.markdown(f"""
    <div class="mascot-box">
        <div class="mascot-avatar">{avatar_emoji}</div>
        <div class="mascot-speech">{fala_texto}</div>
    </div>
    """, unsafe_allow_html=True)


# --- TELA 1: EXIBIÇÃO DO RESULTADO (Se o relatório já foi gerado) ---
if st.session_state.relatorio is not None:
    st.markdown("""<div class="step-card-animated">""", unsafe_allow_html=True)
    renderizar_mascote(
        "🏆", 
        "Parabéns equipe! O parecer do seu negócio foi gerado pela IA do SENAI. Guarde seu resultado!"
    )
    st.success("✅ **Parecer de Viabilidade Concluído!**")
    
    st.markdown(f"### 📋 Diagnosticando: **{st.session_state.nome_negocio}**")
    st.markdown(st.session_state.relatorio)
    
    # Gerar e disponibilizar o download do PDF em memória
    try:
        pdf_bytes = gerar_pdf_relatorio(
            nome_negocio=st.session_state.nome_negocio,
            oferta=st.session_state.oferta_problema,
            cliente=st.session_state.cliente,
            diferencial=st.session_state.diferencial,
            preco=st.session_state.preco_canal,
            relatorio_markdown=st.session_state.relatorio
        )
        st.write("")
        st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=pdf_bytes,
            file_name="meu_plano_de_negocio_senai.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    except Exception as pdf_err:
        st.warning(f"⚠️ Não foi possível gerar o PDF: {pdf_err}")

    st.balloons()
    st.info("💡 **Dica da oficina:** Baixe o PDF acima ou tire um print desta tela para guardar a avaliação da sua ideia!")
    
    st.markdown("---")
    if st.button("🔄 Refazer Avaliação / Novo Negócio", use_container_width=True):
        reiniciar_formulario()
    st.markdown("""</div>""", unsafe_allow_html=True)

# --- TELA 2: FLUXO PASSO A PASSO (ENTREVISTA GUIADA) ---
else:
    # Barra de Progresso Visual
    if st.session_state.step <= 5:
        progress_val = st.session_state.step / 5
        st.progress(progress_val)
        st.caption(f"📍 **Etapa {st.session_state.step} de 5** ({int(progress_val * 100)}% concluído)")
    else:
        st.progress(1.0)
        st.caption("✅ **Revisão Final** (100% concluído)")

    # Conteúdo da etapa com animação suave de entrada
    st.markdown("""<div class="step-card-animated">""", unsafe_allow_html=True)

    # ETAPA 1: Nome do Negócio
    if st.session_state.step == 1:
        renderizar_mascote(
            "👋", 
            "Olá! Sou o assistente de inovação do SENAI. Vamos dar um nome incrível para a sua ideia?"
        )
        
        st.markdown("""
        <div class="step-container">
            <div class="step-title">🏷️ 1. Qual é o nome da sua ideia ou projeto?</div>
            <div class="step-subtitle">Escolha um nome simples, marcante ou como sua equipe prefere chamar o negócio.</div>
        </div>
        """, unsafe_allow_html=True)
        
        val1 = st.text_input(
            "Nome do Negócio",
            value=st.session_state.nome_negocio,
            placeholder="Ex: Marmitaria Fit Express, TechFix Celulares, EcoClean...",
            label_visibility="collapsed"
        )
        
        st.write("")
        if st.button("Avançar ➜", use_container_width=True, type="primary"):
            if not val1.strip():
                st.warning("⚠️ Por favor, digite o nome do negócio para continuar.")
            else:
                st.session_state.nome_negocio = val1.strip()
                st.session_state.step = 2
                st.rerun()

    # ETAPA 2: Oferta e Problema
    elif st.session_state.step == 2:
        renderizar_mascote(
            "💡", 
            "Toda grande empresa começa resolvendo uma dor real! O que vocês vão oferecer e para quem?"
        )
        
        st.markdown("""
        <div class="step-container">
            <div class="step-title">🎯 2. O que vocês vão oferecer e qual problema resolve?</div>
            <div class="step-subtitle">Explique resumidamente o produto/serviço e qual a dor do cliente que ele resolve.</div>
        </div>
        """, unsafe_allow_html=True)
        
        val2 = st.text_area(
            "Oferta e Problema",
            value=st.session_state.oferta_problema,
            placeholder="Ex: Marmitas diárias saudáveis entregues no trabalho para quem não tem tempo de cozinhar...",
            label_visibility="collapsed",
            height=100
        )
        
        st.write("")
        col_back, col_next = st.columns([1, 2])
        with col_back:
            if st.button("⬅ Voltar", use_container_width=True):
                st.session_state.oferta_problema = val2
                st.session_state.step = 1
                st.rerun()
        with col_next:
            if st.button("Avançar ➜", use_container_width=True, type="primary"):
                if not val2.strip():
                    st.warning("⚠️ Por favor, descreva o que oferecem antes de avançar.")
                else:
                    st.session_state.oferta_problema = val2.strip()
                    st.session_state.step = 3
                    st.rerun()

    # ETAPA 3: Cliente-Alvo
    elif st.session_state.step == 3:
        renderizar_mascote(
            "🔍", 
            "Hora de investigar! Quem é o cliente principal que vai amar e pagar pela sua solução?"
        )
        
        st.markdown("""
        <div class="step-container">
            <div class="step-title">👥 3. Quem é o cliente principal?</div>
            <div class="step-subtitle">Quem são as pessoas ou empresas que mais precisam da sua solução?</div>
        </div>
        """, unsafe_allow_html=True)
        
        val3 = st.text_input(
            "Cliente Principal",
            value=st.session_state.cliente,
            placeholder="Ex: Trabalhadores de escritório da região central, estudantes universitários...",
            label_visibility="collapsed"
        )
        
        st.write("")
        col_back, col_next = st.columns([1, 2])
        with col_back:
            if st.button("⬅ Voltar", use_container_width=True):
                st.session_state.cliente = val3
                st.session_state.step = 2
                st.rerun()
        with col_next:
            if st.button("Avançar ➜", use_container_width=True, type="primary"):
                if not val3.strip():
                    st.warning("⚠️ Por favor, identifique o cliente principal.")
                else:
                    st.session_state.cliente = val3.strip()
                    st.session_state.step = 4
                    st.rerun()

    # ETAPA 4: Diferencial Competitivo
    elif st.session_state.step == 4:
        renderizar_mascote(
            "🚀", 
            "Qual é o seu grande superpoder? O que torna a sua proposta muito melhor que a concorrência?"
        )
        
        st.markdown("""
        <div class="step-container">
            <div class="step-title">⭐ 4. Qual é o grande diferencial da proposta?</div>
            <div class="step-subtitle">Por que o cliente escolheria comprar de você e não dos concorrentes?</div>
        </div>
        """, unsafe_allow_html=True)
        
        val4 = st.text_input(
            "Diferencial",
            value=st.session_state.diferencial,
            placeholder="Ex: Entrega super rápida em 20 min, opção sem glúten/lactose sem taxa extra...",
            label_visibility="collapsed"
        )
        
        st.write("")
        col_back, col_next = st.columns([1, 2])
        with col_back:
            if st.button("⬅ Voltar", use_container_width=True):
                st.session_state.diferencial = val4
                st.session_state.step = 3
                st.rerun()
        with col_next:
            if st.button("Avançar ➜", use_container_width=True, type="primary"):
                if not val4.strip():
                    st.warning("⚠️ Por favor, informe o diferencial competitivo.")
                else:
                    st.session_state.diferencial = val4.strip()
                    st.session_state.step = 5
                    st.rerun()

    # ETAPA 5: Preço e Canal de Venda
    elif st.session_state.step == 5:
        renderizar_mascote(
            "💰", 
            "Vamos aos números e canais! Quanto vai custar e por onde os clientes vão comprar?"
        )
        
        st.markdown("""
        <div class="step-container">
            <div class="step-title">💰 5. Preço estimado e canal de venda</div>
            <div class="step-subtitle">Qual o valor aproximado do produto/serviço e por onde ele será vendido?</div>
        </div>
        """, unsafe_allow_html=True)
        
        val5 = st.text_input(
            "Preço e Canal",
            value=st.session_state.preco_canal,
            placeholder="Ex: R$ 22,00 por marmita. Vendas pelo WhatsApp, Instagram e IFood...",
            label_visibility="collapsed"
        )
        
        st.write("")
        col_back, col_next = st.columns([1, 2])
        with col_back:
            if st.button("⬅ Voltar", use_container_width=True):
                st.session_state.preco_canal = val5
                st.session_state.step = 4
                st.rerun()
        with col_next:
            if st.button("Revisar Ficha 📋", use_container_width=True, type="primary"):
                if not val5.strip():
                    st.warning("⚠️ Por favor, informe o preço e canal de venda.")
                else:
                    st.session_state.preco_canal = val5.strip()
                    st.session_state.step = 6
                    st.rerun()

    # ETAPA 6: Tela de Revisão e Envio
    elif st.session_state.step == 6:
        renderizar_mascote(
            "🎉", 
            "Excelente trabalho! Confira o resumo da sua ficha abaixo e solicite a análise da IA."
        )

        st.markdown("### 📋 Resumo da sua Ficha de Negócio")

        st.markdown(f"""
        <div class="review-item">
            <div class="review-label">🏷️ Nome do Negócio</div>
            <div class="review-value">{st.session_state.nome_negocio}</div>
        </div>
        <div class="review-item">
            <div class="review-label">🎯 Oferta e Problema Resolvido</div>
            <div class="review-value">{st.session_state.oferta_problema}</div>
        </div>
        <div class="review-item">
            <div class="review-label">👥 Cliente Principal</div>
            <div class="review-value">{st.session_state.cliente}</div>
        </div>
        <div class="review-item">
            <div class="review-label">⭐ Diferencial Competitivo</div>
            <div class="review-value">{st.session_state.diferencial}</div>
        </div>
        <div class="review-item">
            <div class="review-label">💰 Preço e Canal de Venda</div>
            <div class="review-value">{st.session_state.preco_canal}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_edit, col_submit = st.columns([1, 2])
        with col_edit:
            if st.button("⬅ Editar Dados", use_container_width=True):
                st.session_state.step = 5
                st.rerun()
                
        with col_submit:
            submit_ai = st.button("Gerar Parecer com IA 🚀", use_container_width=True, type="primary")

        if submit_ai:
            if not api_key or api_key == "SUA_CHAVE_AQUI":
                st.error("❌ Por favor, configure a chave de API do Gemini para continuar.")
            else:
                with st.spinner("🤖 A IA do SENAI está analisando a viabilidade do seu negócio..."):
                    try:
                        relatorio = gerar_parecer_gemini(
                            nome_negocio=st.session_state.nome_negocio,
                            oferta_problema=st.session_state.oferta_problema,
                            cliente=st.session_state.cliente,
                            diferencial=st.session_state.diferencial,
                            preco_canal=st.session_state.preco_canal,
                            api_key_val=api_key
                        )
                        st.session_state.relatorio = relatorio
                        st.rerun()
                    except Exception as err:
                        st.error(f"❌ Erro ao consultar o serviço do Gemini: {err}")
                        st.info("Por favor, verifique sua chave ou aguarde alguns instantes antes de tentar novamente.")

        st.write("")
        if st.button("🔄 Reiniciar / Nova Ficha", use_container_width=True):
            reiniciar_formulario()

    st.markdown("""</div>""", unsafe_allow_html=True)

# Rodapé Fixo
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.78rem; margin-top: 0.5rem;'>"
    "Feirão de Empregabilidade 2026 • SENAI • Oficina por Alene Petrina"
    "</div>",
    unsafe_allow_html=True
)
