import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Agencia P2P", layout="wide")
st.title("🤖 Agencia IA - Buscador de Brechas P2P")
st.markdown("---")

# Inicializar Memoria
if 'spread_anterior' not in st.session_state:
    st.session_state.spread_anterior = 0.0
if 'historial_spreads' not in st.session_state:
    st.session_state.historial_spreads = []

st.subheader("⚙️ Parámetros de Operación")
col1, col2, col3, col4 = st.columns(4)

with col1:
    capital_usdt = st.number_input("Monto a operar (USDT)", value=1000.0, step=100.0)
with col2:
    banco_defecto = st.text_input("Pago principal", value="Banesco")
with col3:
    banco_secundario = st.text_input("Pago secundario", value="PagoMovil")
with col4:
    nivel_comerciante = st.selectbox("Nivel de Comerciante", ["No Verificado", "Bronce", "Plata", "Oro"])

comisiones = {"No Verificado": 0.0025, "Bronce": 0.0020, "Plata": 0.00175, "Oro": 0.00125}
f_maker = comisiones[nivel_comerciante]

def buscar_anuncios(tipo_comercio, banco=None, monto_ves=None, tipo_merchant="No Verificado"):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "fiat": "VES", "page": 1, "rows": 8, 
        "tradeType": tipo_comercio, "asset": "USDT"
    }
    
    if tipo_merchant == "No Verificado":
        payload["publisherType"] = None
    else:
        payload["publisherType"] = "merchant"
        
    if banco:
        payload["payTypes"] = [banco]
    else:
        payload["payTypes"] = []
        
    if monto_ves:
        payload["transAmount"] = str(monto_ves) 
        
    try:
        response = requests.post(url, json=payload)
        datos = response.json()
        if datos['code'] == '000000' and datos['data']:
            anuncios = []
            for anuncio in datos['data']:
                anuncios.append({
                    "Anunciante": anuncio['advertiser']['nickName'],
                    "Precio": float(anuncio['adv']['price']),
                    "Disponible (USDT)": float(anuncio['adv']['surplusAmount']),
                    "Límite (VES)": f"{float(anuncio['adv']['minSingleTransAmount']):.0f} - {float(anuncio['adv']['dynamicMaxSingleTransAmount']):.0f}"
                })
            return pd.DataFrame(anuncios).head(5)
    except Exception as e:
        pass
    return pd.DataFrame([{"Anunciante": "Sin datos", "Precio": 0.0, "Disponible (USDT)": 0.0, "Límite (VES)": "0"}])

col_auto, _ = st.columns([1, 3])
with col_auto:
    auto_refresh = st.toggle("🔄 Activar Escáner Automático (5s)")

if auto_refresh or st.button("🚀 Escanear Mercado", type="primary"):
    with st.spinner('Procesando análisis cuantitativo y generando anuncios...'):
        
        df_t1 = buscar_anuncios("BUY", tipo_merchant=nivel_comerciante) 
        df_t2 = buscar_anuncios("BUY", banco_defecto, tipo_merchant=nivel_comerciante) 
        
        precio_venta_ref = df_t2.iloc[0]['Precio'] if not df_t2.empty and df_t2.iloc[0]['Precio'] > 0 else 40.0
        
        capital_ves = capital_usdt * precio_venta_ref
        zona_ataque = int(capital_ves / 30)
        zona_media = int(zona_ataque * 1.6666)
        zona_alta = int(zona_ataque * 3)
        
        st.markdown(f"### 🎯 Zonas Calculadas (Capital Total: **{capital_ves:,.2f} VES**)")
        st.caption(f"Salida Alta: **{zona_alta:,} VES** | Salida Media: **{zona_media:,} VES** | Zona Ataque: **{zona_ataque:,} VES**")
        
        df_t3 = buscar_anuncios("SELL", banco_defecto, zona_alta, tipo_merchant=nivel_comerciante) 
        df_t4 = buscar_anuncios("SELL", banco_defecto, zona_media, tipo_merchant=nivel_comerciante) 
        df_t5 = buscar_anuncios("SELL", banco_defecto, zona_ataque, tipo_merchant=nivel_comerciante) 
        df_t6 = buscar_anuncios("SELL", banco_secundario, zona_ataque, tipo_merchant=nivel_comerciante) 
        
        st.subheader("📊 Monitoreo del Mercado Maker")
        
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            st.markdown("### 1. Ventas Gral")
            st.dataframe(df_t1, hide_index=True)
        with t2:
            st.markdown(f"### 2. Ventas {banco_defecto}")
            st.dataframe(df_t2, hide_index=True)
        with t3:
            st.markdown("### 3. Recompra Alta")
            st.dataframe(df_t3, hide_index=True)
        with t4:
            st.markdown("### 4. Recompra Media")
            st.dataframe(df_t4, hide_index=True)
            
        st.markdown("---")
        
        t5, t6, t7 = st.columns([1, 1, 2]) 
        with t5:
            st.markdown(f"### 5. Ataque {banco_defecto}")
            st.dataframe(df_t5, hide_index=True)
        with t6:
            st.markdown(f"### 6. Ataque {banco_secundario}")
            st.dataframe(df_t6, hide_index=True)
            
        # Variable global de rentabilidad para el Kill-Switch
        rentabilidad_neta = -100.0 
        
        # --- TABLA 7: ANÁLISIS CUANTITATIVO ESTRATÉGICO ---
        with t7:
            st.markdown("### 7. Análisis Cuantitativo Estratégico")
            try:
                # FILTRO ANTI-FANTASMAS (Mínimo 50 USDT)
                df_ventas_reales = df_t2[df_t2['Disponible (USDT)'] >= 50.0]
                df_compras_reales = df_t5[df_t5['Disponible (USDT)'] >= 50.0]
                
                precio_venta = df_ventas_reales.iloc[0]['Precio'] if not df_ventas_reales.empty else df_t2.iloc[0]['Precio']
                precio_compra = df_compras_reales.iloc[0]['Precio'] if not df_compras_reales.empty else df_t5.iloc[0]['Precio']
                
                ingreso_neto = precio_venta * (1 - f_maker)
                costo_neto = precio_compra * (1 + f_maker)
                spread_neto = ingreso_neto - costo_neto
                rentabilidad_neta = (spread_neto / costo_neto) * 100
                
                # MEMORIA DE MERCADO (15 MIN)
                st.session_state.historial_spreads.append(spread_neto)
                if len(st.session_state.historial_spreads) > 180:
                    st.session_state.historial_spreads.pop(0)
                    
                tendencia = "⚪ Calculando..."
                if len(st.session_state.historial_spreads) >= 36: 
                    mitad = len(st.session_state.historial_spreads) // 2
                    media_antigua = sum(st.session_state.historial_spreads[:mitad]) / mitad
                    media_reciente = sum(st.session_state.historial_spreads[mitad:]) / len(st.session_state.historial_spreads[mitad:])
                    
                    if media_reciente > media_antigua + 0.015:
                        tendencia = "🟢 Expandiendo"
                    elif media_reciente < media_antigua - 0.015:
                        tendencia = "🔴 Contrayendo"
                    else:
                        tendencia = "⚪ Estático"
                
                precio_breakeven = (precio_venta * (1 - f_maker)) / (1 + f_maker)
                ganancia_ves = spread_neto * capital_usdt
                ganancia_usdt = ganancia_ves / precio_venta
                
                c1, c2, c3 = st.columns(3)
                c1.metric(label="Spread Neto (VES)", value=f"{spread_neto:.4f}", delta=tendencia)
                c2.metric(label="Rentabilidad Neta", value=f"{rentabilidad_neta:.3f}%")
                c3.metric(label="Límite Breakeven", value=f"{precio_breakeven:.2f}")
                
                st.markdown(f"**Proyección del Ciclo ({capital_usdt} USDT):** 💵 Ganancia Neta: **{ganancia_ves:,.2f} VES** (~{ganancia_usdt:.2f} USDT)")
                
                if rentabilidad_neta <= 0.1:
                    st.error("🔴 **NO OPERAR:** Margen de maniobra insuficiente. Riesgo inminente de pérdida o breakeven.")
                elif rentabilidad_neta <= 0.3:
                    st.warning("🟡 **MERCADO REGULAR:** Brecha ajustada. Operar con cautela y vigilar la salida de emergencia de 50k.")
                else:
                    st.success("🟢 **MERCADO EXCELENTE:** Brecha amplia y favorable. Ideal para atacar la zona principal.")
                    
            except Exception as e:
                st.warning("Evaluando profundidad de mercado...")

        # --- NUEVA SECCIÓN: GENERADOR DE ANUNCIOS MAKER ---
        st.markdown("---")
        st.markdown("### 📋 Generador de Anuncios (Señales de Operación)")
        
        # KILL-SWITCH DE SEGURIDAD
        if rentabilidad_neta <= 0.1:
            st.error("🔒 **SEÑALES BLOQUEADAS POR SEGURIDAD:** El Agente Quant ha ocultado los parámetros de los anuncios porque ejecutar operaciones con el mercado actual resultaría en pérdidas matemáticas debido a las comisiones. Por favor, espera a que el mercado se expanda.")
        else:
            try:
                col_vende, col_compra = st.columns(2)
                
                with col_vende:
                    st.info("📤 **TUS ANUNCIOS DE VENTA (Vender tus USDT por VES)**")
                    precio_sugerido_venta = precio_venta - 0.01
                    
                    # Lógica de salida rápida: Límite mínimo = 1/3 del capital
                    limite_minimo_venta = capital_ves / 3
                    limite_maximo_venta = capital_ves
                    
                    st.markdown(f"🔹 **Precio Sugerido:** `{precio_sugerido_venta:.3f} VES`")
                    st.markdown(f"🔹 **Límites (Mín - Máx):** `{limite_minimo_venta:,.2f} - {limite_maximo_venta:,.2f} VES`")
                    st.caption(f"Estrategia: Eres el #1 absoluto. Tu límite mínimo obliga a los compradores a llevarse grandes cantidades para liquidar en máximo 3 operaciones.")

                with col_compra:
                    st.success("📥 **TUS ANUNCIOS DE RECOMPRA (Recuperar tus USDT)**")
                    precio_sugerido_ataque = df_t5.iloc[0]['Precio'] + 0.01 if not df_t5.empty else 0
                    precio_sugerido_media = df_t4.iloc[0]['Precio'] + 0.01 if not df_t4.empty else 0
                    precio_sugerido_alta = df_t3.iloc[0]['Precio'] + 0.01 if not df_t3.empty else 0
                    
                    st.markdown(f"🔸 **Zona Ataque Directo:** Precio: `{precio_sugerido_ataque:.3f} VES` | Límite Mín: `{zona_ataque:,.2f} VES`")
                    st.markdown(f"🔸 **Zona Media (Emergencia):** Precio: `{precio_sugerido_media:.3f} VES` | Límite Mín: `{zona_media:,.2f} VES`")
                    st.markdown(f"🔸 **Zona Alta (Emergencia):** Precio: `{precio_sugerido_alta:.3f} VES` | Límite Mín: `{zona_alta:,.2f} VES`")
                    st.caption("Estrategia: Posicionarte 0.01 VES por encima del competidor #1, respetando estrictamente la zona de liquidez analizada.")
            except Exception as e:
                st.warning("Faltan datos para generar las señales precisas de los anuncios.")

    if auto_refresh:
        time.sleep(5)
        st.rerun()