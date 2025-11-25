import streamlit as st
import zipfile

# Configuração básica
st.set_page_config(
    page_title="ORION - Iluminando seu próximo passo",
    page_icon="✨",
    layout="centered",
)

# CSS Persosnalizado
CSS = """
<style>
:root {
  --nebula-blue: #1b3c73;
  --aurora-green: #3ecf8e;
  --stellar-purple: #8a4fff;
  --graphite-black: #111111;
  --space-gray: #f3f5f7;
  --danger-red: #e53935;
  --warning-yellow: #ffb300;
  --success-green: #4caf50;
}

body {
  background: radial-gradient(circle at top left, #e6f0ff 0, #f8fafc 40%, #f3f5f7 100%) !important;
}

.main {
  background-color: transparent;
}

.block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
}

/* CARTÃO PRINCIPAL */
.orion-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 24px 24px 24px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

/* LOGO */
.orion-logo-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.orion-logo-circle {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  background: var(--nebula-blue);
  position: relative;
  overflow: hidden;
}

.orion-logo-circle .orbit {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid rgba(138, 79, 255, 0.6);
  top: 10px;
  left: -12px;
}

.orion-logo-circle .star-main {
  position: absolute;
  width: 16px;
  height: 16px;
  background: var(--aurora-green);
  top: 14px;
  right: 18px;
  border-radius: 999px;
  box-shadow: 0 0 12px rgba(62, 207, 142, 0.8);
}

.orion-logo-circle .star-1,
.orion-logo-circle .star-2 {
  position: absolute;
  width: 8px;
  height: 8px;
  background: var(--stellar-purple);
  border-radius: 999px;
}

.orion-logo-circle .star-1 {
  left: 14px;
  top: 20px;
}

.orion-logo-circle .star-2 {
  bottom: 14px;
  right: 26px;
}

.orion-logo-text h1 {
  font-size: 32px;
  letter-spacing: .12em;
  color: var(--nebula-blue);
  margin: 0;
}

.orion-logo-text p {
  font-size: 14px;
  color: #3c4b6e;
  margin: 0;
}

/* TÍTULOS */
h3.orion-section-title {
  color: var(--nebula-blue);
  margin-top: 1.5rem;
  margin-bottom: 0.25rem;
}

/* DICA */
.orion-hint {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 0.25rem;
}

/* BARRA DE RISCO */
.risk-bar {
  margin-top: 0.5rem;
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: #e2e8f0;
  overflow: hidden;
}

.risk-bar-inner {
  height: 100%;
  width: 0;
  transition: width 0.4s ease;
}

.risk-low { background: var(--success-green); }
.risk-medium { background: var(--warning-yellow); }
.risk-high { background: var(--danger-red); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Tabela de Base

# Risco base de automação por área (0 = sem risco, 1 = risco máximo)
RISCO_BASE_AREA = {
    "atendimento": 0.8,
    "administração": 0.7,
    "indústria": 0.75,
    "comércio": 0.65,
    "logística": 0.7,
    "tecnologia": 0.4,
    "educação": 0.45,
    "saúde": 0.35,
    "criatividade": 0.3,
    "outros": 0.6,
}

# Sugestões de carreiras por interesse/área

CARREIRAS_SUGERIDAS = {
    "tecnologia": [
        "Desenvolvedor(a) de Software",
        "Engenheiro(a) de Dados",
        "Especialista em Segurança da Informação",
        "Analista de Inteligência Artificial",
    ],
    "pessoas": [
        "UX Reseacher",
        "Psicólogo(a) Organizacional",
        "Analista de Desenvolvimento Humano",
        "Product Owner focado em usuários",
    ],
    "negócios": [
        "Analista de Dados de Negócios",
        "Gestor(a) de Produtos Digitais",
        "Consultor(a) de Transformação Digital",
    ],
    "criatividade": [
        "UI/UX Designer",
        "Designer de Experiências Digitais",
        "Creator de Conteúdo Educacional",
    ],
    "sustentabilidade": [
        "Analista de Sustentabilidade",
        "Gestor(a) de projetos ESG",
        "Especialista em Eficiência Energética",
    ],
}

# Trilhas base de aprendizado (upskilling/reskilling)
TRILHAS_BASE = {
    "tecnologia": [
        "Lógica de Programação",
        "Programação em Python",
        "Estruturas de Dados e Algoritmos",
        "Banco de Dados",
        "Fundamentos de IA e Machine Learning",
    ],
    "dados": [
        "Excel/Planilhas Avançadas",
        "Fundamentos de Estatística",
        "Python para Análise de Dados",
        "Visualização de Dados (Power BI / Tableau)",
        "Machine Learning básico",
    ],
    "soft_skills": [
        "Comunicação Não Violenta",
        "Trabalho em Equipe e Colaboração",
        "Resolução de Problemas Complexos",
        "Gestão do Tempo e Prioridades",
    ],
    "sustentabilidade": [
        "Fundamentos de Energias Renováveis",
        "Eficiência Energética no Ambiente de Trabalho",
        "ESG e Responsabilidade Socioambiental",
    ],
}

# Funções de lógica

# Função prinicpal de cálculo
def processar_perfil(area, interesses, competencias_tec, competencias_soft):
    media_tec = sum(competencias_tec) / len(competencias_tec)
    media_soft = sum(competencias_soft) / len(competencias_soft)

    risco = RISCO_BASE_AREA.get(area, 0.6)

    if area in ["tecnologia", "indústria", "logística", "administração"]:
        if media_tec < 4:
            risco += 0.1
        elif media_tec > 7:
            risco -= 0.05

    if media_soft >= 7:
        risco -= 0.15
    elif media_soft <= 3:
        risco += 0.1
    
    # Limita entre 0 e 1
    risco = max(0, min(1, risco))
    risco_percent = int(risco * 100)

    if risco < 0.33:
        faixas = "baixo"
    elif risco < 0.66:
        faixas = "médio"
    else:
        faixas = "alto"

    # Primeiro pelos interesses declarados
    carreiras = []
    for i in interesses:
        if i in CARREIRAS_SUGERIDAS:
            for c in CARREIRAS_SUGERIDAS[i]:
                if c not in carreiras:
                    carreiras.append(c)
    
    # Se nada foi associado ainda, olha para área atual
    if not carreiras:
        if area == "tecnologia":
            carreiras.extend(CARREIRAS_SUGERIDAS["tecnologia"]).copy()
        elif area in ["atendimento", "comércio", "educação", "saúde"]:
            carreiras.extend(CARREIRAS_SUGERIDAS["pessoas"]).copy()
        elif area in ["administração", "logística"]:
            carreiras.extend(CARREIRAS_SUGERIDAS["negócios"]).copy()
        else:
            # fallback genérico
            carreiras.extend(CARREIRAS_SUGERIDAS["tecnologia"]).copy()
    
    # Se o risco é alto, reforça carreiras de maior futuro digital
    if faixas == "alto":
        for c in CARREIRAS_SUGERIDAS["tecnologia"]:
            if c not in carreiras:
                carreiras.append(c)
    
    carreiras = carreiras[:6]  # limita para não ficar grande

    # Se o risco é alto, foca em tecnologia e dados
    if faixas == "alto":
        trilha = TRILHAS_BASE["tecnologia"] + TRILHAS_BASE["dados"][:3]
    elif faixas == "médio":
        trilha = TRILHAS_BASE["dados"] + ["Introdução à Transformação Digital na sua área"]
    else:
        trilha = TRILHAS_BASE["soft_skills"] + ["Atualização contínua em tendências da sua profissão"]

    # Sustentabilidade como módulo transversal
    trilha += TRILHAS_BASE["sustentabilidade"][:2]
    trilha_final = []
    for t in trilha:
        if t not in trilha_final:
            trilha_final.append(t)
    
    if faixas == "alto":
        explicacao = "Sua área tem forte potencial de automação. Isso não é sentença, mas um convite para acelerar sua adaptação."
    elif faixas =="médio":
        explicacao = "Algumas tarefas tendem a ser automatizadas, mas há muito espaço para quem se atualiza e aprende a trabalhar junto com a tecnologia."
    else:
        explicacao = "Seu trabalho tem componentes humanos fortes e menos substituíveis. Ainda assim, atualização constante é essencial."
    
    mensagem = (
        "A ideia da ORION não é decidir por você, e sim te dar clareza.\n"
        "O futuro do trabalho não é sobre competir com máquinas, mas sobre usar a tecnologia como aliada "
        "para amplificar o que você tem de mais humano."
    )

    return risco_percent, faixas, explicacao, carreiras, trilha_final, mensagem

def texto_de_arquivos_linkedin(arquivos_upload):
    """
    Recebe uma lista de arquivos enviados pelo usuário (UploadedFile),
    que podem ser .zip ou .csv, e devolve um texto único juntando tudo.
    """
    partes = []

    for arq in arquivos_upload:
        nome = arq.name.lower()

        # Se for um ZIP, abrimos e lemos todos os CSVs/Textx lá dentro
        if nome.endswith(".zip"):
            try:
                with zipfile.ZipFile(arq) as zf:
                    for membro in zf.namelist():
                        if membro.lower().endswith((".csv", ".txt")):
                            with zf.open(membro) as f:
                                conteudo = f.read().decode("utf-8", errors="ignore")
                                partes.append(conteudo)
            except Exception as e:
                st.warning(f"Não consegui ler o ZIP {arq.name}: {e}")
        else:
            ## CSV solto
            try:
                conteudo = arq.read().decode("utf-8", errors="ignore")
                partes.append(conteudo)
            except Exception as e:
                st.warning(f"Não consegui ler o arquivo {e}")
    return "\n".join(partes)

def analisar_linkedin(texto_bruto: str):
    """
    Lê o texto colado do LinkedIn e faz um chute de:
    - área
    - interesses
    - competências técnicas e comportamentais (0 a 10)
    """
    t = texto_bruto.lower()

    # Área
    if any(p in t for p in ["desenvolvedor", "developer", "programador", "software", "data", "dados"]):
        area = "tecnologia"
    elif any(p in t for p in ["vendas", "comercial", "sales", "vendedor", "lojista"]):
        area = "comércio"
    elif any(p in t for p in ["call center", "atendimento", "suporte"]):
        area = "atendimento"             
    elif any(p in t for p in ["logística", "supply chain", "estoque"]):
        area = "logística"             
    elif any(p in t for p in ["professor", "educação", "docente"]):
        area = "educação"
    elif any(p in t for p in ["enfermeiro", "hospital", "clínica", "saúde"]):
        area = "saúde"             
    elif any(p in t for p in ["designer", "ux", "ui", "criativo", "criatividade"]):
        area = "criatividade"             
    else:
        area = "outros"
    
    # Interesses
    interesses = []
    if any(p in t for p in ["python", "java", "dados", "data", "ia", "machine learning", "tecnologia"]):
        interesses.append("tecnologia")
    if any(p in t for p in ["cliente", "pessoas", "time", "equipe", "atendimento", "gestão de pessoas"]):
        interesses.append("pessoas")
    if any(p in t for p in ["negócios", "business", "vendas", "estratégia", "marketing"]):
        interesses.append("negócios")
    if any(p in t for p in ["design", "criativo", "conteúdo", "arte"]):
        interesses.append("criatividade")
    if any(p in t for p in ["sustentável", "sustentabilidade", "esg", "impacto ambiental"]):
        interesses.append("sustentabilidade")

    if not interesses:
        interesses = ["tecnologia"] if area == "tecnologia" else ["negócios"]
    
    # Helper para níveis técnicos
    def nivel(alta, media):
        if any(p in t for p in alta):
            return 8
        if any(p in t for p in media):
            return 6
        return 4
    
    tec_prog = nivel(
        ["python", "java", "c#", "javascript", "developer", "desenvolvedor"],
        ["sistemas", "programação"]
    )
    tec_dados = nivel(
        ["analista de dados", "data analyst", "analytics", "bi"],
        ["excel", "planilhas", "relatórios"]
    )
    tec_auto = nivel(
        ["automação", "rpa", "scripts"],
        ["otimização de processos"]
    )
    tec_sec = nivel(
        ["segurança da informação", "security"],
        ["lgpd", "governança"]
    )
    tec_cloud = nivel(
        ["aws", "azure", "gcp", "cloud"],
        ["servidor", "infraestrutura"]
    )
    tec_ia = nivel(
        ["inteligência artificial", "ia", "machine learning", "ml"],
        ["modelos preditivos"]
    )

    # Soft skills
    def soft_nivel(palavras):
        if any(p in t for p in palavras):
            return 8
        return 6
    
    soft_com = soft_nivel(["comunicação", "apresentações", "relacionamento"])
    soft_cri = soft_nivel(["criativo", "inovação", "design thinking"])
    soft_colab = soft_nivel(["time", "equipe", "colaboração", "squad"])
    soft_prob = soft_nivel(["problemas complexos", "resolução de problemas", "melhoria contínua"])
    soft_emp = soft_nivel(["empatia", "escuta", "atendimento humano"])
    soft_crit = soft_nivel(["análise crítica", "pensamento crítico", "estratégia"])

    competencias_tec = [tec_prog, tec_dados, tec_auto, tec_sec, tec_cloud, tec_ia]
    competencias_soft =[soft_com, soft_cri, soft_colab, soft_prob, soft_emp, soft_crit]

    # remove duplicados preservando ordem
    interesses = list(dict.fromkeys(interesses))

    return area, interesses, competencias_tec, competencias_soft

def exibir_relatorio(nome_exibicao, idade, emprego, area, interesses, competencias_tec, competencias_soft):
    (
        risco_percent,
        faixas,
        explicacao,
        carreiras,
        trilha,
        mensagem,
    ) = processar_perfil(area, interesses, competencias_tec, competencias_soft)

    # Relatório em texto para download
    relatorio_texto = []
    relatorio_texto.append("RELATÓRIO ORION - VISÃO DO FUTUTRO PROFISSIONAL\n")
    relatorio_texto.append(f"Nome: {nome_exibicao}")
    relatorio_texto.append(f"Idade: {idade}")
    relatorio_texto.append(f"Emprego atual: {emprego or 'não informado'}")
    relatorio_texto.append(f"Área: {area}")
    relatorio_texto.append(
        "Interesses: " + (", ".join(interesses) if interesses else "não informado")
    )
    relatorio_texto.append("")
    relatorio_texto.append(f"Risco de automação: {risco_percent}% ({faixas.upper()})")
    relatorio_texto.append(explicacao)
    relatorio_texto.append("")
    relatorio_texto.append("Caminhos de carreira sugeridos:")
    for c in carreiras:
        relatorio_texto.append(f"- {c}")
    relatorio_texto.append("")
    relatorio_texto.append("Trilha de aprendizado sugerida:")
    for i, passo in enumerate(trilha, start=1):
        relatorio_texto.append(f"{i}. {passo}")
    relatorio_texto.append("")
    relatorio_texto.append("Mensagem final:")
    relatorio_texto.append(mensagem)

    relatorio_texto = "\n".join(relatorio_texto)

    # Exibição na tela
    st.markdown("---")
    st.markdown(
        f"<p style='font-size:14px; color:#0f172a;'>"
        f"{nome_exibicao}, com base nas informações que você compartilhou, "
        f"a ORION montou uma visão do seu cenário atual e próximos passos possíveis."
        f"</p>",
        unsafe_allow_html=True,
    )

    # Risco
    st.markdown("#### Risco de automação")
    st.write(f"**Estimativa:** {risco_percent}% ({faixas.upper()})")
    st.write(explicacao)

    bar_class = "risk-low" if faixas == "baixo" else "risk-medium" if faixas == "médio" else "risk-high"
    st.markdown(
        f"""
        <div class="risk-bar">
            <div class="risk-bar-inner {bar_class}" style="width:{risco_percent}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Carreiras
    st.markdown("#### Caminhos de carreir sugeridos")
    for c in carreiras:
        st.markdown(f"- {c}")
    
    # Trilha
    st.markdown("##### Trilha de aprendizado sugerida")
    for i, passo in enumerate(trilha, start=1):
        st.markdown(f"{i}. {passo}")

    st.markdown("###### Mensagem final")
    st.write(mensagem)
    return relatorio_texto

# INTERFACE STREAMLIT
with st.container():
    # Logo
    st.markdown(
     """
     <div class="orion-logo-wrap">
          <div class="orion-logo-circle">
            <div class="orbit"></div>
            <div class="star-main"></div>
            <div class="star-1"></div>
            <div class="star-2"></div>
          </div>
          <div class="orion-logo-text">
            <h1>ORION</h1>
            <p>Iluminando seu próximo passo.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    aba_manual, aba_linkedin = st.tabs(
        ["Preencher manualmente", "Usar dados do LinkedIn"]
    )

    # Aba Manual
    with aba_manual:
        with st.form("manual_form"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input(
                    "Como você quer ser chamado(a)?", 
                    "",
                    key="nome",
                    )
            with col2:
                idade = st.number_input(
                    "Idade", 
                    min_value=14, 
                    max_value=100, 
                    value=20, 
                    step=1,
                    key="idade",
                )
            
            emprego = st.text_input(
                "Emprego / função", 
                "",
                key="emprego",
                )

            area = st.selectbox(
                "Área em que você atua você",
                options=[
                    "atendimento",
                    "administração",
                    "indústria",
                    "comércio",
                    "logística",
                    "tecnologia",
                    "educação",
                    "saúde",
                    "criatividade",
                    "outros",
                ],
                index=5,
            )

            st.markdown('<h3 class="orion-section-title">Interesses Gerais</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="orion-hint">Selecione o que mais combina com você.</p>',
                unsafe_allow_html=True,
            )
            interesses = st.multiselect(
                "Marque seus interesses principais:",
                options=["tecnologia", "pessoas", "negócios", "criatividade", "sustentabilidade"],
                default=["tecnologia"],
                key="interesses",
            )

            st.markdown('<h3 class="orion-select-title">Competências técnicas</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="orion-hint">0 = não tenho, 10 = muito forte.</p>',
                unsafe_allow_html=True,
            )

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                tec_prog = st.slider("Programação", 0, 10, 5, key="tec_prog")
                tec_dados = st.slider("Análise de dados", 0, 10, 5, key="tec_dados")
                tec_auto = st.slider("Automação", 0, 10, 5, key="tec_auto")
            with col_t2:
                tec_sec = st.slider("Segurança da informação", 0, 10, 5, key="tec_sec")
                tec_cloud = st.slider("Cloud", 0, 10, 5, key="tec_cloud")
                tec_ia = st.slider("Inteligência artificial", 0, 10, 5, key="tec_ia")
            
            st.markdown('<h3 class="orion-section-title">Competências comportamentais</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p class="orion-hunt">Seja sincero, a ideia é te exergar de verdade.</p',
                unsafe_allow_html=True,
            )

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                soft_com = st.slider("Comunicação", 0, 10, 6, key="sotf_com")
                soft_cri = st.slider("Criatividade", 0, 10, 6, key="soft_cri")
                sotf_colab = st.slider("Colaboração", 0, 10, 6, key="soft_colab")
            with col_s2:
                soft_prob = st.slider("Resolução de problemas", 0, 10, 6, key="soft_prob")
                soft_empt = st.slider("Empatia", 0, 10, 6, key="soft_emp")
                soft_crit = st.slider("Pensamento crítico", 0, 10, 6, key="soft_crit")
            
            submitted_manual = st.form_submit_button("Gerar relatório ORION")
        
        if submitted_manual:
            nome_exibicao = nome or "Você"
            competencias_tec = [tec_prog, tec_dados, tec_auto, tec_sec, tec_cloud, tec_ia]
            competencias_soft = [soft_com, soft_cri, sotf_colab, soft_prob, soft_empt, soft_crit]

            relatorio_texto = exibir_relatorio(
                nome_exibicao,
                idade,
                emprego,
                area,
                interesses,
                competencias_tec,
                competencias_soft,
            )

            # Botões
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Baixar relatório (.txt)",
                    data=relatorio_texto,
                    file_name="relatorio_orion.txt",
                    mime="text/plain",
                )
            with col2:
                if st.button("Limpar e recomeçar"):
                    st.session_state.clear()
                    st.rerun()
    
    # Aba LinkedIn
    with aba_linkedin:
        st.markdown(
            """
            Cole aqui o texto do seu LinkedIn (seção "Sobre" e/ou principais experiências)
            <strong>ou</strong> envie o arquivo de exportação que o LinkedIn te mandou
            (aquele ZIP cheio de CSVs).
            A ORION vai tentar entender sua área, interesses e competências a partir disso
            e montar o relatório automaticamente. Depois você pode refinar pelo modo manual
            se quiser.
            """,
            unsafe_allow_html=True,
        )

        with st.form("linkedin_form"):
            col1, col2 = st.columns(2)
            with col1:
                nome_li = st.text_input(
                    "Como você quer ser chamado(a)?", key="nome_li"
                )
            with col2:
                idade_li = st.number_input(
                    "Idade (opcional)",
                    min_value=14,
                    max_value=100,
                    value=25,
                    step=1,
                    key="idade_li",
                )

            emprego_li = st.text_input(
                "Título atual no LinkedIn (ex: Desenvolvedor Backend, Analista de Dados...)",
                key="emprego_li",
            )

            texto_li = st.text_area(
                "Cole aqui o texto do seu LinkedIn (opcional se você enviar arquivos):",
                height=220,
                key="texto_li",
            )

            arquivos_li = st.file_uploader(
                "Ou envie o arquivo ZIP que o LinkedIn te mandou, ou os CSVs da pasta:",
                type=["zip", "csv"],
                accept_multiple_files=True,
                key="arquivos_li",
            )

            submitted_li = st.form_submit_button("Gerar relatório a partir do LinkedIn")

        if submitted_li:
            # Decide de onde vem o texto
            if arquivos_li:
                texto_fonte = texto_de_arquivos_linkedin(arquivos_li)
            else:
                texto_fonte = texto_li
            if not texto_fonte.strip():
                st.warning(
                    "Cole algum texto do LinkedIn OU envie o ZIP/CSVs da exportação "
                    "para eu conseguir analisar."
                )
            else:
                (
                    area_li,
                    interesses_li,
                    competencias_tec_li,
                    competencias_soft_li,
                ) = analisar_linkedin(texto_fonte)

                st.info(
                    f"Detectei automaticamente a área **{area_li}** "
                    f"e interesses: {', '.join(interesses_li)}. "
                    "É só uma estimativa, mas já dá uma boa base para o relatório."
                )

                nome_exibicao = nome_li or "Você"

                relatorio_texto_li = exibir_relatorio(
                    nome_exibicao,
                    idade_li,
                    emprego_li,
                    area_li,
                    interesses_li,
                    competencias_tec_li,
                    competencias_soft_li,
                )

                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Baixar relatório (.txt)",
                        data=relatorio_texto_li,
                        file_name="relatorio_orion_linkedin.txt",
                        mime="text/plain",
                    )
                with col2:
                    if st.button("Limpar e reiniciar (LinkedIn)"):
                        st.session_state.clear()
                        st.rerun()

# Rodapé
st.markdown(
    "<p style='text-align:center; font-size:12px; color:#6b7280; margin-top:1.5rem;'>"
    "©ORION – Por Fernando e Gabriel. Projeto acadêmico para explorar o futuro do trabalho com tecnologia e humanidade."
    "</p>",
    unsafe_allow_html=True
)
