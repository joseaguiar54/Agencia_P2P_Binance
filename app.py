import streamlit as st
import requests
import pandas as pd
import time
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Crear carpeta para capturas si no existe
if not os.path.exists("capturas_p2p"):
    os.makedirs("capturas_p2p")

# Cargar variables secretas
load_dotenv()

st.set_page_config(page_title="Agencia P2P | Skalix UI", layout="wide", page_icon="⚡")

# --- INYECCIÓN DE CSS (ESTILO SKALIX) ---
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #94a3b8; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    [data-testid="stMetric"] { background-color: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); transition: transform 0.2s ease-in-out; }
    [data-testid="stMetric"]:hover { transform: translateY(-2px); }
    [data-testid="stMetricValue"] { color: #f8fafc; font-weight: 700; font-size: 1.8rem; }
    [data-testid="stMetricDelta"] { font-weight: 600; }
    [data-testid="baseButton-primary"] { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 8px; font-weight: 600; letter-spacing: 0.5px; padding: 0.6rem 1.2rem; transition: all 0.3s ease; }
    [data-testid="baseButton-primary"]:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }
    h1, h2, h3 { color: #f1f5f9 !important; font-weight: 700; }
    hr { border-color: #1e293b; margin-top: 2rem; margin-bottom: 2rem; }
    .stAlert { border-radius: 10px !important; border: 1px solid #1e293b !important; }
    [data-testid="stDataFrame"] { border-radius: 10px; border: 1px solid #1e293b; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { background-color: #121826 !important; border: 1px solid #334155 !important; color: #f8fafc !important; border-radius: 8px; }
    [data-testid="stSidebar"] { background-color: #121826 !important; border-right: 1px solid #1e293b; }
</style>
""", unsafe_allow_html=True)

# --- WHITE PAPER INSTITUCIONAL ---
@st.dialog("📚 White Paper Institucional - Agencia P2P")
def mostrar_whitepaper():
    st.markdown("""
    ### 🧠 Filosofía del Motor Cuantitativo
    El Terminal Quant no busca adivinar el mercado, sino medir la fricción. La rentabilidad se calcula descontando las comisiones exactas de tu nivel de comerciante en Binance. Si el Spread Neto cubre la fricción y arroja verde, el bot autoriza la ejecución.

    ---

    ### 🛡️ 1. Modo Rentabilidad Pura (Default)
    *   **Cuándo usar:** Mercados volátiles o con baja competencia donde las brechas son amplias.
    *   **Objetivo:** Extraer ganancias tangibles para el fondo de capitalización.
    *   **Regla del Bot:** Exige un spread neto mínimo del 0.10%. Sugiere precios competitivos pero que garanticen un margen real.

    ### 🚀 2. Modo Volumen (Break-Even)
    *   **Cuándo usar:** Días lentos o con alta competencia donde los márgenes son inferiores a 0.10%.
    *   **Objetivo:** Adquirir volumen gratuito para alcanzar la meta de Verificado (2 BTC y 1000 órdenes en 30 días).
    *   **Regla del Bot:** Baja la exigencia a 0.00%. Sugiere precios hiper-agresivos (Top 1 en Binance) para rotar capital velozmente cubriendo solo el 0.50% de las comisiones (Maker) sin que tu bolsillo sufra.

    ### 🗜️ 3. La Estrategia de la Pinza (Límites Asimétricos)
    *   **Venta (Entregar USDT):** Configuras en Binance límites de **$10 a $20**. Captas clientes minoristas que asumen precios un poco peores. Dispara rápidamente tu métrica de *Número de Órdenes*.
    *   **Recompra (Recibir USDT):** Configuras en Binance límites de **$200 a Máximo**. Entras al territorio de los mayoristas con el precio agresivo que te calculó el radar para montos bajos, quedando siempre de absoluto #1. Dispara tu métrica de *Volumen Acumulado*.
    
    ### ⚡ 4. Arbitraje Flash (Radar Taker)
    *   **Cuándo usar:** Picos súbitos de volatilidad alcista en VES (notificados con alerta naranja 🔥).
    *   **Objetivo:** Hacer un "Flash Loan" usando la ventana de pago de Binance.
    *   **Ejecución:**
        1. Abres 4 anuncios de Compra Maker escalonando el precio en +0.001 (ej. 40.001, 40.002) con duración de 30 a 45 minutos. Atrapas minoristas.
        2. Liquidarás tu saldo inicial de USDT vendiéndolo directamente a otro anuncio (Taker).
        3. Con el capital líquido obtenido de la venta Taker, pagas las órdenes de los minoristas retenidos antes de que expire el tiempo.
    *   **Seguridad:** El radar asegura que el precio de venta Taker (menos 0.06%) sea matemáticamente superior a tu costo de adquisición Maker (más 0.50%).

    ### 🌎 5. Ecosistema Zinli vs Banca VES
    *   **Zinli (USD):** Ideal para rotar volumen veloz. Permite límites bajos (ej. $10) con una frecuencia altísima gracias al perfil del usuario (freelancers, gamers). Menor fricción bancaria.
    *   **VES (Banca Nacional):** Ideal para márgenes amplios y arbitraje flash, pero requiere cautela con el escáner bancario. Utilizar Banesco o PagoMovil espaciando operaciones.
    """)

with st.sidebar:
    st.markdown("### 🏛️ Control Central")
    if st.button("📚 Ver White Paper", use_container_width=True):
        mostrar_whitepaper()
    st.markdown("---")
    st.info("El archivo maestro con tus tácticas de mercado, siempre a un clic de distancia para alinear operaciones antes del combate.")

st.title("⚡ Terminal Quant - Agencia P2P")
st.markdown("---")

# --- DATOS BANCARIOS (KYC MAKER) ---
BANCOS_INFO = {
    "Banesco": """Banesco Banco Universal\nTipo: Cuenta Corriente (VES)\nNro: 01340438174381036374\nCI: V-18.322.554\nTitular: JOSE RAFAEL AGUIAR CONTRERAS""",
    "Mercantil": """Mercantil, C.A, Banco Universal\nTipo: Cuenta de Ahorro (VES)\nNro: 01050101610101414609\nCI: V-18.322.554\nTitular: JOSE RAFAEL AGUIAR CONTRERAS""",
    "Zinli": """Billetera Zinli (USD)\nCorreo: tucorreo@gmail.com\nTitular: JOSE RAFAEL AGUIAR CONTRERAS"""
}

# --- BASES DE DATOS LOCALES ---
CICLOS_FILE = "ciclos_p2p.csv"
OPERACIONES_FILE = "operaciones_p2p.csv"

cols_ciclos = ["ID_Ciclo", "Fecha", "Capital (USDT)", "P. Venta", "P. Recompra (Principal)", "P. Recompra (NV)", "P. Recompra (Media)", "P. Recompra (Alta)", "Ganancia Neta (USDT)"]
cols_operaciones = ["ID_Orden", "ID_Ciclo", "Fecha", "Plataforma", "Tipo", "Zona", "Monto_USDT", "Monto_Fiat", "Metodo", "Cliente", "CI", "Cuenta", "KYC", "Captura_Local", "Captura_URL"]

def cargar_df(archivo, columnas):
    if os.path.exists(archivo): 
        df = pd.read_csv(archivo)
        if "Monto_VES" in df.columns:
            df.rename(columns={"Monto_VES": "Monto_Fiat"}, inplace=True)
            df.to_csv(archivo, index=False)
        for c in columnas:
            if c not in df.columns: df[c] = None
        return df
    return pd.DataFrame(columns=columnas)

def guardar_df(df, archivo): df.to_csv(archivo, index=False)

# --- INICIALIZAR MEMORIA ---
if 'estrategia' not in st.session_state: st.session_state.estrategia = "🇻🇪 Nacional (VES)"
if 'ciclos_df' not in st.session_state: st.session_state.ciclos_df = cargar_df(CICLOS_FILE, cols_ciclos)
if 'operaciones_df' not in st.session_state: st.session_state.operaciones_df = cargar_df(OPERACIONES_FILE, cols_operaciones)
if 'historial_spreads' not in st.session_state: st.session_state.historial_spreads = []
if 'ultimo_envio_telegram' not in st.session_state: st.session_state.ultimo_envio_telegram = 0.0
if 'ultimo_nivel_enviado' not in st.session_state: st.session_state.ultimo_nivel_enviado = ""
if 'kyc_nombre_temporal' not in st.session_state: st.session_state.kyc_nombre_temporal = ""
if 'ultimo_spread_sonoro' not in st.session_state: st.session_state.ultimo_spread_sonoro = 0.0

if 'auto_pv' not in st.session_state: st.session_state.auto_pv = 0.0
if 'auto_pc_prin' not in st.session_state: st.session_state.auto_pc_prin = 0.0
if 'auto_pc_nv' not in st.session_state: st.session_state.auto_pc_nv = 0.0
if 'auto_pc_med' not in st.session_state: st.session_state.auto_pc_med = 0.0
if 'auto_pc_alt' not in st.session_state: st.session_state.auto_pc_alt = 0.0

# --- FUNCIONES DE API ---
def enviar_telegram(mensaje, captura_local=None, captura_url=None):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return False, "Faltan credenciales"
    try:
        if captura_local:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(captura_local, "rb") as f:
                res = requests.post(url, data={"chat_id": chat_id, "caption": mensaje, "parse_mode": "HTML", "show_caption_above_media": True}, files={"photo": f})
            if res.status_code != 200:
                with open(captura_local, "rb") as f:
                    res = requests.post(url, data={"chat_id": chat_id, "caption": mensaje, "show_caption_above_media": True}, files={"photo": f})
        elif captura_url and captura_url.startswith("http"):
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            res = requests.post(url, data={"chat_id": chat_id, "caption": mensaje, "parse_mode": "HTML", "photo": captura_url, "show_caption_above_media": True})
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            res = requests.post(url, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "HTML"})
            if res.status_code != 200:
                res = requests.post(url, json={"chat_id": chat_id, "text": mensaje})
                
        return (True, "Enviado") if res.status_code == 200 else (False, res.text)
    except Exception as e: return False, str(e)

def obtener_precio_btc():
    try: return float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=3).json()["price"])
    except: return 60000.0

def buscar_anuncios(tipo_comercio, fiat_sym="VES", banco=None, monto_fiat=None, tipo_merchant="No Verificado"):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {"fiat": fiat_sym, "page": 1, "rows": 8, "tradeType": tipo_comercio, "asset": "USDT", "publisherType": None if tipo_merchant == "No Verificado" else "merchant", "payTypes": [banco] if banco else []}
    if monto_fiat: payload["transAmount"] = str(monto_fiat) 
    try:
        datos = requests.post(url, json=payload).json()
        if datos['code'] == '000000' and datos['data']:
            return pd.DataFrame([{"Anunciante": a['advertiser']['nickName'], "Precio": float(a['adv']['price']), "Disponible": float(a['adv']['surplusAmount']), f"Límites ({fiat_sym})": f"{float(a['adv']['minSingleTransAmount']):.0f} - {float(a['adv']['dynamicMaxSingleTransAmount']):.0f}"} for a in datos['data']]).head(5)
    except: pass
    return pd.DataFrame([{"Anunciante": "Sin datos", "Precio": 0.0, "Disponible": 0.0, f"Límites ({fiat_sym})": "0"}])

# --- MODALES DE OPERACIÓN ---
@st.dialog("➕ Apertura de Nuevo Ciclo Macro")
def modal_nuevo_ciclo(f_maker, fiat_sym):
    st.info(f"Almacena tus precios estratégicos para todas las zonas de ataque ({fiat_sym}).")
    c1, c2 = st.columns(2)
    reg_cap = c1.number_input("Capital Operado (USDT)", value=float(capital_usdt), step=50.0)
    reg_venta = c2.number_input("Precio Venta (Salida)", value=float(st.session_state.auto_pv), format="%.3f")
    
    st.markdown("**Zonas de Recompra Guardadas:**")
    c3, c4, c5, c6 = st.columns(4)
    r_prin = c3.number_input("Principal", value=float(st.session_state.auto_pc_prin), format="%.3f")
    r_nv = c4.number_input("Zona NV", value=float(st.session_state.auto_pc_nv), format="%.3f")
    r_med = c5.number_input("Media", value=float(st.session_state.auto_pc_med), format="%.3f")
    r_alt = c6.number_input("Alta", value=float(st.session_state.auto_pc_alt), format="%.3f")
    
    if st.button("💾 Crear Ciclo Raíz", type="primary", use_container_width=True):
        if reg_venta > 0 and r_prin > 0:
            ganancia_usdt_real = (((reg_venta / (1 + f_maker)) - (r_prin / (1 - f_maker))) * reg_cap) / (reg_venta / (1 + f_maker))
            nuevo_ciclo = {
                "ID_Ciclo": str(uuid.uuid4())[:8], "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Capital (USDT)": reg_cap, "P. Venta": reg_venta, "P. Recompra (Principal)": r_prin,
                "P. Recompra (NV)": r_nv, "P. Recompra (Media)": r_med, "P. Recompra (Alta)": r_alt,
                "Ganancia Neta (USDT)": round(ganancia_usdt_real, 2)
            }
            st.session_state.ciclos_df = pd.concat([pd.DataFrame([nuevo_ciclo]), st.session_state.ciclos_df], ignore_index=True)
            guardar_df(st.session_state.ciclos_df, CICLOS_FILE)
            st.rerun()

@st.dialog("➕ Agregar Operación (Cliente)")
def modal_operacion(id_ciclo_actual, fiat_sym):
    ciclo_base = st.session_state.ciclos_df[st.session_state.ciclos_df["ID_Ciclo"] == id_ciclo_actual].iloc[0]
    st.markdown(f"**Registrando micro-operación | Ciclo:** `{id_ciclo_actual}`")
    
    op_id_orden = st.text_input("ID de la Orden (Binance) ⚠️", placeholder="Ej: 20394857392038")
    
    col_op1, col_op2 = st.columns(2)
    op_plataforma = col_op1.selectbox("Plataforma", ["Binance", "Bybit", "Bitget", "Zinli Directo"])
    op_tipo = col_op2.selectbox("Tipo de Orden", ["Venta (Entregas USDT)", "Compra (Recibes USDT)", "Venta TAKER (Descarga)"])
    
    precio_aplicado = ciclo_base["P. Venta"]
    zona_sel = "Salida (Venta)"
    
    if "Compra" in op_tipo:
        zona_sel = st.selectbox("🎯 Zona de Recompra Ejecutada", ["Principal", "Zona NV", "Media", "Alta"])
        if zona_sel == "Principal": precio_aplicado = ciclo_base["P. Recompra (Principal)"]
        elif zona_sel == "Zona NV": precio_aplicado = ciclo_base["P. Recompra (NV)"]
        elif zona_sel == "Media": precio_aplicado = ciclo_base["P. Recompra (Media)"]
        elif zona_sel == "Alta": precio_aplicado = ciclo_base["P. Recompra (Alta)"]
    elif "TAKER" in op_tipo:
        zona_sel = "Arbitraje Flash"
        
    st.caption(f"Precio base sugerido para cálculo: **{precio_aplicado:.3f} {fiat_sym}** (Puedes editar el Fiat abajo)")
    st.markdown("---")
    
    col_op3, col_op4 = st.columns(2)
    op_usdt = col_op3.number_input("Monto USDT", min_value=0.0, format="%.2f", step=10.0)
    op_fiat = col_op4.number_input(f"Monto Fiat ({fiat_sym})", value=float(op_usdt * precio_aplicado), format="%.2f", step=10.0 if fiat_sym=="USD" else 100.0)
    
    col_op5, col_op6 = st.columns(2)
    op_metodo = col_op5.selectbox("Método de Pago", ["Zinli", "Banesco", "Mercantil", "PagoMovil", "BDV", "Otro"] if fiat_sym=="USD" else ["Banesco", "Mercantil", "PagoMovil", "BDV", "Zinli", "Otro"])
    if op_metodo in BANCOS_INFO: col_op5.info(f"**TUS DATOS (Copiar):**\n\n{BANCOS_INFO[op_metodo]}")
        
    col_ci1, col_ci2 = st.columns([1, 1])
    with col_ci1:
        op_ci = st.text_input("C.I. / Doc. Contraparte", placeholder="V-12345678 o Correo")
        if st.button("🔍 Verificar KYC"):
            ci_limpia = "".join(filter(str.isdigit, op_ci))
            nacionalidad = 'E' if op_ci.upper().startswith('E') else 'V'
            if ci_limpia:
                try:
                    r = requests.get(f"https://api.cedula.com.ve/api/v1?app_id=9365&token=a1b4b16de2f74b40c86558a079934d16&nacionalidad={nacionalidad}&cedula={ci_limpia}", timeout=5).json()
                    if "data" in r and r["data"]:
                        st.session_state.kyc_nombre_temporal = " ".join([n for n in [r["data"].get("primer_nombre",""), r["data"].get("segundo_nombre",""), r["data"].get("primer_apellido",""), r["data"].get("segundo_apellido","")] if n]).strip()
                        st.success(f"✅ KYC Verificado: {st.session_state.kyc_nombre_temporal}")
                except: st.error("❌ Error API Cédula.")
    
    with col_ci2: op_cliente = st.text_input("Cliente (Alias / Nombre)", value=st.session_state.kyc_nombre_temporal)
        
    op_cuenta = st.text_input("Cuenta Bancaria / Email (Contraparte)")
    op_kyc = st.checkbox("✅ KYC Validado (La cuenta coincide con la Cédula/Binance)")
    
    st.markdown("**Comprobante de Pago**")
    capt_col1, capt_col2 = st.columns(2)
    op_captura_url = capt_col1.text_input("URL Captura (Opcional)")
    op_captura_file = capt_col2.file_uploader("O subir Imagen Local", type=['png', 'jpg', 'jpeg'])
    
    if st.button("💾 Guardar y Avisar a Telegram", type="primary", use_container_width=True):
        if op_usdt > 0 and op_id_orden:
            captura_local = ""
            if op_captura_file is not None:
                file_path = os.path.join("capturas_p2p", f"{op_id_orden}_{op_captura_file.name}")
                with open(file_path, "wb") as f: f.write(op_captura_file.getbuffer())
                captura_local = file_path 
                
            nueva_op = {
                "ID_Orden": op_id_orden, "ID_Ciclo": id_ciclo_actual, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Plataforma": op_plataforma, "Tipo": op_tipo, "Zona": zona_sel, "Monto_USDT": op_usdt, "Monto_Fiat": op_fiat,
                "Metodo": op_metodo, "Cliente": op_cliente, "CI": op_ci, "Cuenta": op_cuenta,
                "KYC": "Sí" if op_kyc else "No", "Captura_Local": captura_local, "Captura_URL": op_captura_url
            }
            st.session_state.operaciones_df = pd.concat([pd.DataFrame([nueva_op]), st.session_state.operaciones_df], ignore_index=True)
            guardar_df(st.session_state.operaciones_df, OPERACIONES_FILE)
            
            enlace_html = f'<a href="{op_captura_url}">Enlace de Pago</a>' if (op_captura_url and len(op_captura_url)>5) else "No adjuntada"
            
            mensaje_telegram = f"""
🧾 <b>OPERACIÓN REGISTRADA</b> 🧾

🔹 <b>ID Orden:</b> <code>{op_id_orden}</code>
🔹 <b>Ciclo:</b> <code>{id_ciclo_actual}</code>
🔄 <b>Tipo:</b> {op_tipo}
🎯 <b>Zona Ejecutada:</b> {zona_sel}

💰 <b>Monto USDT:</b> {op_usdt:.2f} USDT
💱 <b>Monto Fiat:</b> {op_fiat:,.2f} {fiat_sym}
🏦 <b>Método:</b> {op_metodo}

👤 <b>Cliente:</b> {op_cliente}
💳 <b>Doc:</b> {op_ci}
📧 <b>Cuenta/Correo:</b> {op_cuenta}
✅ <b>KYC Validado:</b> {"Sí" if op_kyc else "No"}
🌐 <b>Plataforma:</b> {op_plataforma}

📎 <b>Captura Local:</b> {"Guardada ✅" if captura_local else "No adjuntada"}
🔗 <b>Captura URL:</b> {enlace_html}
            """
            exito, msj_err = enviar_telegram(mensaje_telegram, captura_local=captura_local, captura_url=op_captura_url)
            
            if exito: st.toast("✅ Operación enviada a Telegram.")
            else: st.warning(f"⚠️ Guardado localmente, falló Telegram: {msj_err}")
                
            st.session_state.kyc_nombre_temporal = "" 
            st.rerun()
        else: st.error("Monto USDT e ID obligatorios.")

# --- PARÁMETROS PRINCIPALES ---
st.subheader("⚙️ Configuración del Terminal")
col0, col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 1, 1])

with col0: 
    idx_est = 0 if "VES" in st.session_state.estrategia else 1
    estrategia_sel = st.selectbox("Estrategia", ["🇻🇪 Nacional (VES)", "🌎 Internacional (Zinli - USD)"], index=idx_est)
    st.session_state.estrategia = estrategia_sel

# Variables Dinámicas por Estrategia
is_ves = "VES" in st.session_state.estrategia
fiat_sym = "VES" if is_ves else "USD"
def_banco = "Banesco" if is_ves else "Zinli"
def_sec = "PagoMovil" if is_ves else "Zinli"
def_nv = 20000.0 if is_ves else 50.0
step_nv = 1000.0 if is_ves else 10.0

with col1: capital_usdt = st.number_input("Capital (USDT)", value=1000.0, step=100.0)
with col2: banco_defecto = st.text_input("Banco Principal", value=def_banco)
with col3: banco_secundario = st.text_input("Banco Secundario", value=def_sec)
with col4: nivel_comerciante = st.selectbox("Nivel Binance", ["No Verificado", "Bronce", "Plata", "Oro"])
with col5: monto_no_verificado = st.number_input(f"Ataque NV ({fiat_sym})", value=def_nv, step=step_nv)

comisiones = {"No Verificado": 0.0025, "Bronce": 0.0020, "Plata": 0.00175, "Oro": 0.00125}
f_maker = comisiones[nivel_comerciante]
f_taker = 0.0006 # Comisión Fija Taker 0.06% 

# --- 🏆 TRACKER MERCHANT ---
st.markdown("### 📈 Verificación Merchant P2P")
precio_btc_actual = obtener_precio_btc()

volumen_acumulado = st.session_state.operaciones_df["Monto_USDT"].sum() if not st.session_state.operaciones_df.empty else 0.0
ordenes_acumuladas = len(st.session_state.operaciones_df)
ganancias_acumuladas = st.session_state.ciclos_df["Ganancia Neta (USDT)"].sum() if not st.session_state.ciclos_df.empty else 0.0
equiv_btc_actual = volumen_acumulado / precio_btc_actual if precio_btc_actual > 0 else 0
usdt_restantes = max(0.0, 2.0 - equiv_btc_actual) * precio_btc_actual

m1, m2, m3, m4 = st.columns(4)
m1.metric("Volumen (USDT)", f"{volumen_acumulado:,.2f}", f"- {usdt_restantes:,.2f} restantes", delta_color="inverse")
m2.metric("Equivalencia BTC", f"{equiv_btc_actual:.4f} ₿", f"- {max(0.0, 2.0 - equiv_btc_actual):.4f} restantes", delta_color="inverse")
m3.metric("Órdenes", f"{ordenes_acumuladas} / 1000", f"- {max(0, 1000 - ordenes_acumuladas)} restantes", delta_color="inverse")
m4.metric("Fondo de Ganancias", f"{ganancias_acumuladas:,.2f} USDT", "Meta: 800 USDT")

st.markdown("---")
col_auto1, col_auto2, col_auto3 = st.columns([1, 1, 1.5])
with col_auto1: auto_refresh = st.toggle("🔄 Escáner Auto (5s)", value=True)
with col_auto2: sonido_activado = st.toggle("🔊 Alertas Sonoras", value=True)
with col_auto3: modo_volumen = st.toggle("🚀 Modo Volumen (Break-Even)", value=False)

# --- ESCÁNER LOGIC ---
def logica_escaner(cap_usdt, fiat_symbol, b_def, b_sec, n_com, m_nv, f_m, alerta_activa, m_volumen, f_tak):
    df_t1 = buscar_anuncios("BUY", fiat_symbol, tipo_merchant=n_com) 
    df_t2 = buscar_anuncios("BUY", fiat_symbol, b_def, tipo_merchant=n_com) 
    p_venta_ref = df_t2.iloc[0]['Precio'] if not df_t2.empty and df_t2.iloc[0]['Precio'] > 0 else (40.0 if fiat_symbol=="VES" else 1.0)
    
    cap_fiat = cap_usdt * p_venta_ref
    z_at = int(cap_fiat / 30); z_med = int(z_at * 1.6666); z_alt = int(z_at * 3)
    
    st.markdown(f"### 🎯 Plan de Ataque (Liquidez: **{cap_fiat:,.2f} {fiat_symbol}**)")
    st.caption(f"Zona Alta: **{z_alt:,}** | Zona Media: **{z_med:,}** | Ataque: **{z_at:,}** | NV: **{m_nv:,.0f}**")
    
    df_t3 = buscar_anuncios("SELL", fiat_symbol, b_def, z_alt, tipo_merchant=n_com) 
    df_t4 = buscar_anuncios("SELL", fiat_symbol, b_def, z_med, tipo_merchant=n_com) 
    df_t5 = buscar_anuncios("SELL", fiat_symbol, b_def, z_at, tipo_merchant=n_com) 
    df_t6 = buscar_anuncios("SELL", fiat_symbol, b_sec, z_at, tipo_merchant=n_com) 
    df_t_nv = buscar_anuncios("SELL", fiat_symbol, b_def, m_nv, tipo_merchant=n_com)
    
    t1, t2, t3, t4 = st.columns(4)
    with t1: st.dataframe(df_t1, hide_index=True)
    with t2: st.dataframe(df_t2, hide_index=True)
    with t3: st.dataframe(df_t3, hide_index=True)
    with t4: st.dataframe(df_t4, hide_index=True)
        
    st.markdown("---")
    t5, t6, t_nv_col, t7 = st.columns([1, 1, 1, 3.5]) 
    with t5: st.markdown("##### 5. Principal"); st.dataframe(df_t5, hide_index=True)
    with t6: st.markdown("##### 6. Secundario"); st.dataframe(df_t6, hide_index=True)
    with t_nv_col: st.markdown("##### 7. Zona NV"); st.dataframe(df_t_nv, hide_index=True)
        
    rentabilidad_neta = -100.0 
    rent_flash = -100.0
    
    with t7:
        st.markdown("##### 8. Análisis Cuantitativo y Arbitraje Flash")
        try:
            df_v_reales = df_t2[df_t2['Disponible'] >= (50.0 if fiat_symbol=="VES" else 10.0)]
            df_c_reales = df_t5[df_t5['Disponible'] >= (50.0 if fiat_symbol=="VES" else 10.0)]
            
            p_venta = df_v_reales.iloc[0]['Precio'] if not df_v_reales.empty else df_t2.iloc[0]['Precio']
            p_compra = df_c_reales.iloc[0]['Precio'] if not df_c_reales.empty else df_t5.iloc[0]['Precio']
            
            # --- CÁLCULO MAKER-MAKER ---
            friccion_pct = (f_m * 2) * 100 
            spread_bruto = p_venta - p_compra
            rent_bruta = (spread_bruto / p_compra) * 100
            
            p_venta_efectivo = p_venta / (1 + f_m)
            p_compra_efectivo = p_compra / (1 - f_m)
            spread_neto = p_venta_efectivo - p_compra_efectivo
            rentabilidad_neta = (spread_neto / p_compra_efectivo) * 100
            
            # --- CÁLCULO RADAR TAKER (Arbitraje Flash) ---
            p_venta_taker_efectivo = p_venta * (1 - f_tak)
            spread_flash = p_venta_taker_efectivo - p_compra_efectivo
            rent_flash = (spread_flash / p_compra_efectivo) * 100
            
            st.session_state.historial_spreads.append(spread_neto)
            if len(st.session_state.historial_spreads) > 180: st.session_state.historial_spreads.pop(0)
                
            tendencia = "Estático"
            if len(st.session_state.historial_spreads) >= 36: 
                mitad = len(st.session_state.historial_spreads) // 2
                m_reciente = sum(st.session_state.historial_spreads[mitad:]) / len(st.session_state.historial_spreads[mitad:])
                m_antigua = sum(st.session_state.historial_spreads[:mitad]) / mitad
                if m_reciente > m_antigua + 0.015: tendencia = "Expandiendo"
                elif m_reciente < m_antigua - 0.015: tendencia = "Contrayendo"
            
            st.info(f"⚖️ **Fricción Maker:** Spread Bruto: **{spread_bruto:.4f} ({rent_bruta:.2f}%)** ➖ Fees: **{friccion_pct:.2f}%** 🟰 Rent. Neta: **{rentabilidad_neta:.3f}%**")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(f"Spread Neto ({fiat_symbol})", f"{spread_neto:.4f}", delta=tendencia)
            c2.metric("Rent. Maker", f"{rentabilidad_neta:.3f}%")
            c3.metric("Límite Breakeven", f"{p_venta * ((1 - f_m) / (1 + f_m)):.2f}")
            c4.metric("Rent. Flash Taker", f"{rent_flash:.3f}%", delta="🔥" if rent_flash > 0 else "")
            
            limite_rentabilidad = 0.0 if m_volumen else 0.1
            
            if rent_flash > 0:
                p_base = df_t5.iloc[0]['Precio'] + 0.001 if not df_t5.empty else 0
                st.warning(f"🔥 **VENTANA DE ARBITRAJE FLASH ABIERTA:** Rentabilidad Taker Positiva ({rent_flash:.3f}%). Sugerencia: Abre 4 anuncios Maker escalonados (`{p_base:.3f}`, `{p_base + 0.001:.3f}`, `{p_base + 0.002:.3f}`, `{p_base + 0.003:.3f}`) a 30-45 min y liquida tu stock actual como Taker a `{p_venta:.3f}`.")
            elif rentabilidad_neta < limite_rentabilidad: 
                st.error("🔴 **NO OPERAR:** Margen insuficiente.")
                st.session_state.ultimo_spread_sonoro = 0.0 
            else:
                if m_volumen:
                    st.warning("🟡 **MODO VOLUMEN ACTIVO:** Operando en Break-Even estratégico.")
                else:
                    st.success("🟢 **MERCADO EXCELENTE:** Brecha favorable.")
                    
            if alerta_activa and (rent_flash > 0 or spread_neto > st.session_state.ultimo_spread_sonoro + 0.01):
                if rentabilidad_neta >= limite_rentabilidad or rent_flash > 0:
                    st.markdown("""<audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>""", unsafe_allow_html=True)
                    st.session_state.ultimo_spread_sonoro = spread_neto
            
            st.session_state.auto_pv = p_venta - 0.001
            st.session_state.auto_pc_prin = df_t5.iloc[0]['Precio'] + 0.001 if not df_t5.empty else 0
            st.session_state.auto_pc_nv = df_t_nv.iloc[0]['Precio'] + 0.001 if not df_t_nv.empty else 0
            st.session_state.auto_pc_med = df_t4.iloc[0]['Precio'] + 0.001 if not df_t4.empty else 0
            st.session_state.auto_pc_alt = df_t3.iloc[0]['Precio'] + 0.001 if not df_t3.empty else 0
            
        except Exception as e: st.warning("Evaluando liquidez...")

    st.markdown("---")
    st.markdown("### 📋 Señales de Operación")
    if rentabilidad_neta >= (0.0 if m_volumen else 0.1) or rent_flash > 0:
        try:
            col_v, col_c = st.columns(2)
            with col_v:
                st.info("📤 **ANUNCIOS DE VENTA (Entregas USDT)**")
                st.markdown(f"🔹 **Precio Sugerido Maker:** `{st.session_state.auto_pv:.3f} {fiat_symbol}`")
                st.markdown(f"🔹 **Lim. Mínimo:** `{cap_fiat/3:,.2f} {fiat_symbol}`")
                st.markdown(f"🔹 **Lim. Máximo:** `{cap_fiat:,.2f} {fiat_symbol}`")
            with col_c:
                st.success("📥 **ANUNCIOS DE RECOMPRA (Recibes USDT)**")
                st.markdown(f"🔸 **Z. Principal:** `{st.session_state.auto_pc_prin:.3f} {fiat_symbol}`")
                st.markdown(f"🔸 **Z. NV ({m_nv:,.0f}):** `{st.session_state.auto_pc_nv:.3f} {fiat_symbol}`")
                st.markdown(f"🔸 **Z. Media:** `{st.session_state.auto_pc_med:.3f} {fiat_symbol}`")
                st.markdown(f"🔸 **Z. Alta:** `{st.session_state.auto_pc_alt:.3f} {fiat_symbol}`")
            
            t_actual = time.time()
            if (t_actual - st.session_state.ultimo_envio_telegram > 300) or (st.session_state.ultimo_nivel_enviado != n_com):
                mensaje_telegram = f"""
🚨 <b>NUEVA BRECHA DETECTADA ({fiat_symbol})</b> 🚨

⚙️ <b>Configuración del Agente:</b>
• Nivel Comercial: <b>{n_com}</b>
• Método de Pago: <b>{b_def}</b>
• Capital Base: {cap_usdt} USDT
• Modo Volumen: {"Activado 🚀" if m_volumen else "Desactivado"}

📊 <b>Análisis de Mercado:</b>
• Tendencia: {tendencia}
• Rent. Neta Maker: {rentabilidad_neta:.3f}%
• Spread Neto: {spread_neto:.4f} {fiat_symbol}
"""
                if rent_flash > 0:
                    mensaje_telegram += f"🔥 <b>ARBITRAJE FLASH:</b> {rent_flash:.3f}% (Salida Taker)\n"

                mensaje_telegram += f"""
📤 <b>TUS ANUNCIOS DE VENTA</b>
• Precio Sugerido: {st.session_state.auto_pv:.3f} {fiat_symbol}
• Lim. Mínimo: {cap_fiat/3:,.2f} {fiat_symbol}
• Lim. Máximo: {cap_fiat:,.2f} {fiat_symbol}

📥 <b>TUS ANUNCIOS DE RECOMPRA</b>
• Z. Ataque Principal: {st.session_state.auto_pc_prin:.3f} {fiat_symbol}
• Z. Ataque NV ({m_nv:,.0f}): {st.session_state.auto_pc_nv:.3f} {fiat_symbol}
• Z. Media: {st.session_state.auto_pc_med:.3f} {fiat_symbol}
• Z. Alta: {st.session_state.auto_pc_alt:.3f} {fiat_symbol}
                """
                enviar_telegram(mensaje_telegram)
                st.session_state.ultimo_envio_telegram = t_actual
                st.session_state.ultimo_nivel_enviado = n_com
        except: pass

@st.fragment(run_every=5)
def escaner_automatico(c_usdt, fiat_symbol, b_def, b_sec, n_com, m_nv, f_m, alerta_activa, m_volumen, f_tak): logica_escaner(c_usdt, fiat_symbol, b_def, b_sec, n_com, m_nv, f_m, alerta_activa, m_volumen, f_tak)

@st.fragment
def escaner_manual(c_usdt, fiat_symbol, b_def, b_sec, n_com, m_nv, f_m, alerta_activa, m_volumen, f_tak): logica_escaner(c_usdt, fiat_symbol, b_def, b_sec, n_com, m_nv, f_m, alerta_activa, m_volumen, f_tak)

if auto_refresh: escaner_automatico(capital_usdt, fiat_sym, banco_defecto, banco_secundario, nivel_comerciante, monto_no_verificado, f_maker, sonido_activado, modo_volumen, f_taker)
else:
    if st.button("🚀 Escanear Mercado", type="primary", use_container_width=True): escaner_manual(capital_usdt, fiat_sym, banco_defecto, banco_secundario, nivel_comerciante, monto_no_verificado, f_maker, sonido_activado, modo_volumen, f_taker)

# --- SECCIÓN INFERIOR: GESTIÓN DE BITÁCORA ---
st.markdown("---")
st.header("📔 Base de Datos Operativa")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ Crear Ciclo Macro", use_container_width=True): modal_nuevo_ciclo(f_maker, fiat_sym)

with col_btn2:
    if not st.session_state.ciclos_df.empty:
        opciones = st.session_state.ciclos_df.apply(lambda r: f"Ciclo {r['ID_Ciclo']} - {r['Fecha']} ({r['Capital (USDT)']} USDT)", axis=1).tolist()
        ciclo_sel = st.selectbox("Selecciona un ciclo activo:", opciones, label_visibility="collapsed")
        id_ciclo_objetivo = st.session_state.ciclos_df.iloc[opciones.index(ciclo_sel)]["ID_Ciclo"]
        if st.button("➕ Registrar Micro-Operación", type="primary", use_container_width=True): modal_operacion(id_ciclo_objetivo, fiat_sym)

tab1, tab2 = st.tabs(["📝 Panel de Clientes", "📦 Ciclos Maestros"])
with tab1:
    for c in cols_operaciones:
        if c not in st.session_state.operaciones_df.columns: st.session_state.operaciones_df[c] = None
    edited_ops_df = st.data_editor(st.session_state.operaciones_df[cols_operaciones], num_rows="dynamic", hide_index=True, use_container_width=True)
    if not edited_ops_df.equals(st.session_state.operaciones_df[cols_operaciones]):
        st.session_state.operaciones_df = edited_ops_df
        guardar_df(edited_ops_df, OPERACIONES_FILE)
        st.rerun()

with tab2:
    edited_ciclos_df = st.data_editor(st.session_state.ciclos_df, num_rows="dynamic", hide_index=True, use_container_width=True)
    if not edited_ciclos_df.equals(st.session_state.ciclos_df):
        st.session_state.ciclos_df = edited_ciclos_df
        guardar_df(edited_ciclos_df, CICLOS_FILE)
        st.rerun()