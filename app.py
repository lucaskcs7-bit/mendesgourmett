import streamlit as st
import urllib.parse
from datetime import date, timedelta

# Configuração da página
st.set_page_config(
    page_title="Mendes Gourmet - Gestão & Encomendas",
    page_icon="🎂",
    layout="wide"
)

# =============================================================================
# ⚙️ CONFIGURAÇÕES DE AGENDAMENTO
# =============================================================================
DIAS_ANTECEDENCIA_MINIMA = 1
DIAS_SEMANA_ATENDIMENTO = [1, 2, 3, 4, 5, 6]  # Terça a Domingo

NOME_DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

# =============================================================================
# 🎨 ESTILIZAÇÃO CSS AVANÇADA (Layout idêntico à imagem)
# =============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #FAF7F2;
        color: #333333;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1150px;
    }

    /* Cartão Principal de Conteúdo */
    .card-box {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02);
        border: 1px solid #EFECE6;
    }

    /* Badge "Pedido artesanal" */
    .badge-artesanal {
        background-color: #F3ECE6;
        color: #8C3B3B;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: inline-block;
    }

    /* Estilo dos Rádios Customizados */
    div[role="radiogroup"] {
        gap: 12px;
    }
    
    div[role="radiogroup"] > label {
        background-color: #FFFFFF !important;
        border: 1px solid #EAE5DE !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.01) !important;
        transition: all 0.2s ease !important;
    }

    div[role="radiogroup"] > label:hover {
        border-color: #8C3B3B !important;
        background-color: #FAF4F2 !important;
    }

    /* Botão Principal */
    .stButton>button {
        background-color: #8C3B3B;
        color: white;
        border-radius: 12px;
        height: 48px;
        width: 100%;
        font-size: 15px;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #722E2E;
        color: white;
    }

    /* Estilo do Botão Voltar */
    div[data-testid="stButton"] button[key="btn_back_3"],
    div[data-testid="stButton"] button[key="btn_back"] {
        background-color: #FFFFFF !important;
        color: #555555 !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02) !important;
    }

    /* Card Confirmação */
    .card-sucesso {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 32px 28px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.03);
        border: 1px solid #EFECE6;
        text-align: center;
        max-width: 480px;
        margin: 0 auto;
    }

    .icon-check {
        width: 46px;
        height: 46px;
        background-color: #EAF1EC;
        border-radius: 50%;
        color: #386641;
        font-size: 20px;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
    }

    .box-resumo-sucesso {
        background-color: #FAF8F5;
        border-radius: 14px;
        padding: 16px;
        margin-top: 20px;
        margin-bottom: 22px;
        border: 1px solid #EFECE6;
        text-align: left;
    }

    .btn-wa-custom {
        background-color: #FFFFFF;
        color: #2D2926;
        border: 1px solid #DCD8D0;
        border-radius: 14px;
        padding: 12px 20px;
        width: 100%;
        text-align: center;
        font-size: 14.5px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        text-decoration: none !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.02);
    }

    /* Admin Styles */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #EFECE6;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.01);
    }
    .metric-title {
        color: #777777;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #2D2926;
        font-size: 26px;
        font-weight: 700;
    }

    .kanban-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #EFECE6;
        margin-bottom: 12px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.01);
    }
    .kanban-tag {
        display: inline-block;
        background-color: #FDF2F2;
        color: #8C3B3B;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Mapeamento de datas
DIAS_SEMANA_PT = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
MESES_PT = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

def formatar_data_pt(dt):
    if not dt:
        return "data a combinar"
    dia_semana = DIAS_SEMANA_PT[dt.weekday()]
    dia = dt.day
    mes = MESES_PT[dt.month - 1]
    ano = dt.year
    return f"{dia_semana}, {dia} de {mes} de {ano}"

# PREÇOS E DADOS INICIAIS
TABELA_PRECOS = {"1 kg": 90.00, "2 kg": 152.00}
ADICIONAL_RECHEIO = {"Ninho com Nutella": 0.00, "Brigadeiro": 0.00, "Doce de Leite": 0.00}

# INICIALIZAÇÃO DE ESTADOS
if "modo" not in st.session_state:
    st.session_state.modo = "cliente"

if "passo" not in st.session_state:
    st.session_state.passo = 1

data_minima_permitida = date.today() + timedelta(days=DIAS_ANTECEDENCIA_MINIMA)

if "pedido" not in st.session_state:
    st.session_state.pedido = {
        "peso": "1 kg",
        "massa": "Chocolate",
        "recheio": "Ninho com Nutella",
        "observacoes": "",
        "total": 90.00
    }

if "cliente" not in st.session_state:
    st.session_state.cliente = {
        "nome": "Lucas Kiodi",
        "whatsapp": "(11) 99999-9999",
        "data_retirada": data_minima_permitida,
        "horario": "12:00"
    }

if "lista_pedidos" not in st.session_state:
    st.session_state.lista_pedidos = [
        {"id": 1, "nome": "Lucas Kiodi", "detalhes": "Bolo 1kg — Ninho com Nutella", "retirada": "16 de set. às 12:00", "status": "Novos Pedidos"},
        {"id": 2, "nome": "Lucas Kiodi", "detalhes": "Bolo 1kg — Ninho com Nutella", "retirada": "16 de set. às 12:00", "status": "Novos Pedidos"},
        {"id": 3, "nome": "Lucas Santos", "detalhes": "Bolo 1kg — Doce de Leite", "retirada": "17 de set. às 14:00", "status": "Novos Pedidos"},
        {"id": 4, "nome": "Antonio Santos", "detalhes": "Bolo 1kg — Doce de Leite", "retirada": "18 de set. às 15:00", "status": "Novos Pedidos"}
    ]

if "catalogo" not in st.session_state:
    st.session_state.catalogo = [
        {"nome": "Morango com Chocolate", "tipo": "Sabor", "qtd": 100},
        {"nome": "Caixa de Leite", "tipo": "Insumo", "qtd": 300}
    ]

# =============================================================================
# BARRA SUPERIOR PARA ALTERNAR ENTRE CLIENTE E ADMIN
# =============================================================================
col_top_l, col_top_r = st.columns([8, 2])
with col_top_r:
    if st.session_state.modo == "cliente":
        if st.button("⚙️ Área Admin", key="toggle_admin"):
            st.session_state.modo = "admin"
            st.rerun()
    else:
        if st.button("🛒 Ver Loja", key="toggle_cliente"):
            st.session_state.modo = "cliente"
            st.session_state.passo = 1
            st.rerun()

# =============================================================================
# 🛍️ MODO CLIENTE (ENCOMENDA ONLINE)
# =============================================================================
if st.session_state.modo == "cliente":

    # -------------------------------------------------------------------------
    # PASSO 1: MONTE SEU BOLO (REPLICADO DA PRIMEIRA IMAGEM)
    # -------------------------------------------------------------------------
    if st.session_state.passo == 1:

        # Header do Topo
        c_head_left, c_head_right = st.columns([7, 3])
        with c_head_left:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 20px;">
                    <div style="background-color: #E8D8D0; border-radius: 14px; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 22px;">
                        🎂
                    </div>
                    <div>
                        <h2 style="margin:0; font-weight: 700; color: #2D2926; font-size: 22px;">Mendes Gourmet</h2>
                        <span style="color: #777777; font-size: 13px;">Confeitaria artesanal</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with c_head_right:
            st.markdown("""
                <div style="text-align: right; margin-top: 8px;">
                    <span class="badge-artesanal">Pedido artesanal</span>
                </div>
            """, unsafe_allow_html=True)

        col_left, col_right = st.columns([2.3, 1])

        with col_left:
            st.markdown("""
                <div class="card-box">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 18px;">
                        <span style="background-color: #8C3B3B; color: white; border-radius: 50%; width: 26px; height: 26px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold;">1</span>
                        <div>
                            <strong style="font-size: 17px; color: #2D2926;">Passo 1: Monte Seu Bolo</strong><br>
                            <span style="color: #888888; font-size: 12.5px;">Escolha cada detalhe com carinho.</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)

            # Peso do Bolo
            st.markdown("<p style='font-weight: 600; color: #2D2926; margin-bottom: 8px; font-size: 14px;'>Qual será o peso do bolo?</p>", unsafe_allow_html=True)
            peso_sel = st.radio(
                "Peso",
                ["1 kg", "2 kg"],
                horizontal=True,
                label_visibility="collapsed",
                key="radio_peso"
            )

            st.write("")
            # Escolha da Massa
            st.markdown("<p style='font-weight: 600; color: #2D2926; margin-bottom: 8px; font-size: 14px;'>Escolha a massa</p>", unsafe_allow_html=True)
            massa_sel = st.radio(
                "Massa",
                ["Baunilha", "Chocolate", "Red Velvet"],
                horizontal=True,
                label_visibility="collapsed",
                key="radio_massa"
            )

            st.write("")
            # Escolha do Recheio
            st.markdown("<p style='font-weight: 600; color: #2D2926; margin-bottom: 8px; font-size: 14px;'>Escolha o recheio</p>", unsafe_allow_html=True)
            recheio_sel = st.radio(
                "Recheio",
                ["Ninho com Nutella", "Brigadeiro", "Doce de Leite"],
                horizontal=True,
                label_visibility="collapsed",
                key="radio_recheio"
            )

            st.write("")
            # Observações do Tema
            st.markdown("<p style='font-weight: 600; color: #2D2926; margin-bottom: 8px; font-size: 14px;'>Observações do Tema/Topo</p>", unsafe_allow_html=True)
            obs_input = st.text_area(
                "Observações",
                placeholder="Descreva o tema, cores, topper ou detalhes especiais...",
                label_visibility="collapsed"
            )
            st.markdown("<p style='color: #A09A95; font-size: 12px; margin-top: 4px;'>Se quiser, conte um pouco sobre a ocasião. Vamos preparar cada detalhe com cuidado.</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            valor_calculado = TABELA_PRECOS[peso_sel] + ADICIONAL_RECHEIO[recheio_sel]

        with col_right:
            st.markdown(f"""
                <div class="card-box">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                        <div style="background-color: #F5EBE6; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #8C3B3B; font-size: 18px;">
                            📋
                        </div>
                        <div>
                            <strong style="font-size: 14.5px; color: #2D2926;">Seu bolo personalizado</strong><br>
                            <span style="font-size: 12px; color: #888888;">Escolha os detalhes para ver o total.</span>
                        </div>
                    </div>
                    <div style="background-color: #FAF7F2; padding: 14px; border-radius: 12px; border: 1px solid #EFECE6; margin-bottom: 20px;">
                        <p style="margin: 0; color: #666666; font-size: 13px;">• <b>Peso:</b> {peso_sel}</p>
                        <p style="margin: 4px 0 0 0; color: #666666; font-size: 13px;">• <b>Massa:</b> {massa_sel}</p>
                        <p style="margin: 4px 0 0 0; color: #666666; font-size: 13px;">• <b>Recheio:</b> {recheio_sel}</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="color: #666666; font-size: 13.5px; font-weight: 500;">Total Estimado:</span>
                        <span style="color: #8C3B3B; font-size: 20px; font-weight: 700;">R$ {valor_calculado:.2f}</span>
                    </div>
            """, unsafe_allow_html=True)

            if st.button("Avançar para Agendamento"):
                st.session_state.pedido = {
                    "peso": peso_sel,
                    "massa": massa_sel,
                    "recheio": recheio_sel,
                    "observacoes": obs_input,
                    "total": valor_calculado
                }
                st.session_state.passo = 2
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PASSO 2: FINALIZAR ENCOMENDA (CORREÇÃO DO BUG DA DATA DE RETIRADA)
    # -------------------------------------------------------------------------
    elif st.session_state.passo == 2:
        col_voltar, col_titulo2 = st.columns([0.05, 0.95])
        with col_voltar:
            if st.button("←", key="btn_back"):
                st.session_state.passo = 1
                st.rerun()

        with col_titulo2:
            st.markdown("<p style='color:#708271; font-weight:700; font-size:12px; letter-spacing:0.8px; margin:0;'>PASSO 2 DE 2</p>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin-top:-2px; font-weight:700; color:#2D2926; font-size:24px;'>Finalizar Encomenda</h2>", unsafe_allow_html=True)

        st.write("")
        col_form2, col_resumo2 = st.columns([2.1, 1.1])

        with col_form2:
            st.markdown("#### **Seu Nome**")
            nome = st.text_input("Nome", value=st.session_state.cliente.get("nome", "Lucas Kiodi"), placeholder="Digite seu nome completo", label_visibility="collapsed")

            st.markdown("#### **Seu WhatsApp**")
            whatsapp = st.text_input("WhatsApp", value=st.session_state.cliente.get("whatsapp", "(11) 99999-9999"), placeholder="(11) 99999-9999", label_visibility="collapsed")
            st.caption("Usaremos este número para confirmar os detalhes da encomenda.")

            st.write("")
            st.markdown("#### **Data de Retirada**")
            
            # =================================================================
            # 🛠️ CORREÇÃO DO BUG StreamlitValueBelowMinError
            # =================================================================
            val_data_retirada = st.session_state.cliente.get("data_retirada", data_minima_permitida)

            # Validação para assegurar que a data nunca é anterior à data mínima permitida
            if not isinstance(val_data_retirada, date) or val_data_retirada < data_minima_permitida:
                val_data_retirada = data_minima_permitida

            st.session_state.cliente["data_retirada"] = val_data_retirada

            data_retirada = st.date_input(
                "Data de Retirada",
                value=val_data_retirada,
                min_value=data_minima_permitida,
                format="DD/MM/YYYY",
                label_visibility="collapsed"
            )

            dia_semana_num = data_retirada.weekday()
            data_valida = True

            if dia_semana_num not in DIAS_SEMANA_ATENDIMENTO:
                data_valida = False
                nome_dia = NOME_DIAS_SEMANA[dia_semana_num]
                st.error(f"⚠️ Não realizamos entregas/retiradas às **{nome_dia}s**. Por favor, selecione outro dia.")

            st.write("")
            st.markdown("#### **Horário de Retirada**")
            horarios = ["12:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
            horario_selecionado = st.selectbox("Horário", horarios, label_visibility="collapsed")

        with col_resumo2:
            p = st.session_state.pedido

            col_ico, col_txt = st.columns([0.15, 0.85])
            with col_ico:
                st.markdown("📋")
            with col_txt:
                st.markdown("<h4 style='margin:0; font-weight:700; color:#3A3332;'>Resumo do pedido</h4>", unsafe_allow_html=True)

            st.write("")
            st.markdown(f"**Bolo {p['peso']} — {p['recheio']} — R$ {p['total']:.2f}**")
            
            obs_status = "Observações incluídas no pedido." if p['observacoes'] else "Sem observações adicionais."
            st.markdown(f"<p style='color:#666666; font-size:14px; margin-top:-10px;'>Massa {p['massa']}. {obs_status}</p>", unsafe_allow_html=True)

            st.divider()

            if st.button("💬 Enviar Encomenda via WhatsApp", key="btn_confirmar_passo2", disabled=not data_valida):
                st.session_state.cliente = {
                    "nome": nome if nome else "Lucas Kiodi",
                    "whatsapp": whatsapp if whatsapp else "",
                    "data_retirada": data_retirada,
                    "horario": horario_selecionado
                }
                st.session_state.lista_pedidos.append({
                    "id": len(st.session_state.lista_pedidos) + 1,
                    "nome": nome if nome else "Lucas Kiodi",
                    "detalhes": f"Bolo {p['peso']} — {p['recheio']}",
                    "retirada": f"{data_retirada.strftime('%d/%m')} às {horario_selecionado}",
                    "status": "Novos Pedidos"
                })
                st.session_state.passo = 3
                st.rerun()

    # -------------------------------------------------------------------------
    # PASSO 3: TELA DE CONFIRMAÇÃO
    # -------------------------------------------------------------------------
    elif st.session_state.passo == 3:
        col_voltar, col_titulo3 = st.columns([0.05, 0.95])
        with col_voltar:
            if st.button("←", key="btn_back_3"):
                st.session_state.passo = 2
                st.rerun()

        with col_titulo3:
            st.markdown("<p style='color:#708271; font-weight:700; font-size:12px; letter-spacing:0.8px; margin:0;'>PASSO 2 DE 2</p>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin-top:-2px; font-weight:700; color:#2D2926; font-size:24px;'>Finalizar Encomenda</h2>", unsafe_allow_html=True)

        st.write("")
        _, col_card, _ = st.columns([1, 2.3, 1])

        with col_card:
            p = st.session_state.pedido
            c = st.session_state.cliente

            data_extenso = formatar_data_pt(c.get('data_retirada'))
            nome_cliente = c.get('nome', 'Lucas Kiodi')
            horario_ret = c.get('horario', '12:00')

            num_whatsapp_confeiteira = "5511999999999"
            msg_wa = (
                f" *NOVA ENCOMENDA - MENDES GOURMET*\n\n"
                f"*Cliente:* {nome_cliente}\n"
                f"*WhatsApp:* {c.get('whatsapp', '')}\n"
                f"*Data de Retirada:* {data_extenso} às {horario_ret}\n\n"
                f"--- *DETALHES DO BOLO* ---\n"
                f"• *Bolo:* {p['peso']}\n"
                f"• *Massa:* {p['massa']}\n"
                f"• *Recheio:* {p['recheio']}\n"
                f"• *Observações:* {p['observacoes'] if p['observacoes'] else 'Nenhuma'}\n\n"
                f"💰 *Valor Total:* R$ {p['total']:.2f}"
            )
            link_wa = f"https://wa.me/{num_whatsapp_confeiteira}?text={urllib.parse.quote(msg_wa)}"

            st.markdown(f"""
                <div class="card-sucesso">
                    <div class="icon-check">✓</div>
                    <h3 style="color: #2D2926; font-weight: 700; margin: 0 0 8px 0; font-size: 19px;">Encomenda salva com sucesso!</h3>
                    <p style="color: #6E6B67; font-size: 13.5px; line-height: 1.45; margin: 0 0 20px 0;">
                        Seu pedido foi registrado. Abra o WhatsApp para enviar a mensagem pronta e combinar os últimos detalhes.
                    </p>
                    <div class="box-resumo-sucesso">
                        <p style="font-weight: 700; color: #2D2926; margin: 0 0 4px 0; font-size: 13.5px;">Pedido de {nome_cliente}</p>
                        <p style="color: #55524F; margin: 0 0 4px 0; font-size: 13px;">Bolo {p['peso']} — {p['recheio']}</p>
                        <p style="color: #8C8883; margin: 0; font-size: 12.5px;">R$ {p['total']:.2f} · {data_extenso} às {horario_ret}</p>
                    </div>
                    <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                        <div class="btn-wa-custom">
                            <span style="font-size: 16px;">💬</span>
                            <span>Abrir WhatsApp com a Mensagem</span>
                        </div>
                    </a>
                </div>
            """, unsafe_allow_html=True)

            st.write("")
            if st.button("Acessar área administrativa", key="btn_admin"):
                st.session_state.modo = "admin"
                st.rerun()

# =============================================================================
# 🏢 MODO ADMINISTRATIVO
# =============================================================================
else:
    with st.sidebar:
        st.markdown("### 🎂 **Mendes Gourmet**")
        st.caption("Gestão de confeitaria")
        st.divider()

        menu_opcao = st.radio(
            "Navegação",
            ["📊 Dashboard", "📦 Pedidos", "🍰 Catálogo & Sabores", "📅 Agenda", "⚙️ Configurações"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.markdown("<p style='font-size:12px; color:#888;'>Mendes Gourmet · Gestão artesanal</p>", unsafe_allow_html=True)

    col_adm_header, col_adm_user = st.columns([7, 3])
    with col_adm_header:
        st.markdown("<p style='color:#8C3B3B; font-weight:700; font-size:11px; letter-spacing:1px; margin:0;'>MENDES GOURMET</p>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top:-5px; font-weight:700; color:#2D2926;'>Área Administrativa</h2>", unsafe_allow_html=True)

    with col_adm_user:
        st.markdown("""
            <div style="text-align: right; margin-top: 5px;">
                <span style="font-weight: 600; color: #2D2926; font-size: 14px;">Márcia Mendes</span><br>
                <span style="color: #777; font-size: 12px;">Confeiteira</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    if menu_opcao == "📊 Dashboard":
        col_saudacao, col_busca = st.columns([6, 4])
        with col_saudacao:
            st.markdown("### **Bom trabalho, Márcia.**")
            st.caption("Acompanhe a produção e organize as encomendas do dia.")
        with col_busca:
            st.text_input("Buscar por cliente, bolo ou status", placeholder="🔍 Buscar por cliente, bolo ou status...", label_visibility="collapsed")

        st.write("")

        pedidos_novos = len([p for p in st.session_state.lista_pedidos if p['status'] == 'Novos Pedidos'])
        em_producao = len([p for p in st.session_state.lista_pedidos if p['status'] == 'Em Produção'])
        prontos = len([p for p in st.session_state.lista_pedidos if p['status'] == 'Prontos para Retirada'])
        concluidos = len([p for p in st.session_state.lista_pedidos if p['status'] == 'Concluídos'])

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Pedidos Novos</div><div class="metric-value">{pedidos_novos}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Em produção</div><div class="metric-value">{em_producao}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Prontos</div><div class="metric-value">{prontos}</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Total concluído</div><div class="metric-value">{concluidos}</div></div>', unsafe_allow_html=True)

        st.write("")
        st.divider()

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.markdown("#### **Novos Pedidos**")
            items = [p for p in st.session_state.lista_pedidos if p['status'] == 'Novos Pedidos']
            if not items:
                st.caption("Nenhum pedido nesta etapa.")
            for item in items:
                st.markdown(f"""
                    <div class="kanban-card">
                        <strong style="color:#2D2926;">{item['nome']}</strong><br>
                        <span style="font-size:12.5px; color:#555;">{item['detalhes']}</span><br>
                        <span style="font-size:12px; color:#888;">Retirada: {item['retirada']}</span><br>
                        <span class="kanban-tag">Novos Pedidos</span>
                    </div>
                """, unsafe_allow_html=True)

        with k2:
            st.markdown("#### **Em Produção**")
            items = [p for p in st.session_state.lista_pedidos if p['status'] == 'Em Produção']
            if not items:
                st.caption("Nenhum pedido nesta etapa.")

        with k3:
            st.markdown("#### **Prontos para Retirada**")
            items = [p for p in st.session_state.lista_pedidos if p['status'] == 'Prontos para Retirada']
            if not items:
                st.caption("Nenhum pedido nesta etapa.")

        with k4:
            st.markdown("#### **Concluídos**")
            items = [p for p in st.session_state.lista_pedidos if p['status'] == 'Concluídos']
            if not items:
                st.caption("Nenhum pedido nesta etapa.")

    elif menu_opcao == "📦 Pedidos":
        st.markdown("### **Todos os pedidos**")
        st.caption("Gerencie e acompanhe os detalhes de cada etapa.")
        st.divider()
        for item in st.session_state.lista_pedidos:
            st.markdown(f"**{item['nome']}** — {item['detalhes']} ({item['retirada']})")

    elif menu_opcao == "🍰 Catálogo & Sabores":
        st.markdown("### **Catálogo & Sabores**")
        st.caption("Cadastre e acompanhe sabores e insumos.")
        st.divider()
        for cat in st.session_state.catalogo:
            st.write(f"• **{cat['nome']}** ({cat['tipo']}): {cat['qtd']}")

    elif menu_opcao == "📅 Agenda":
        st.markdown("### **Agenda de retiradas**")
        st.divider()
        for item in st.session_state.lista_pedidos:
            st.write(f"🗓️ **{item['retirada']}** — {item['nome']}")

    elif menu_opcao == "⚙️ Configurações":
        st.markdown("### **Configurações**")
        st.divider()
        st.write("Preferências do sistema.")