import streamlit as st
import pandas as pd
import sympy as sp
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AEA", layout="wide", initial_sidebar_state="collapsed")

# --- INICIALIZAR ESTADOS (PARCHE ANTI-BUG: DOBLE MEMORIA) ---
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"
if "history" not in st.session_state:
    st.session_state.history = []

def guardar_historial():
    if "matriz_actual" in st.session_state:
        st.session_state.history.append(st.session_state.matriz_actual.copy())
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)

# --- ALGORITMO PASO A PASO ---
def obtener_pasos_gauss_jordan(matriz_inicial):
    pasos = []
    M = matriz_inicial.copy()
    filas, columnas = M.shape
    fila_pivote = 0
    for col in range(columnas):
        if fila_pivote >= filas: break
        pivote_val = M[fila_pivote, col]
        if pivote_val == 0:
            for r in range(fila_pivote + 1, filas):
                if M[r, col] != 0:
                    M.row_swap(fila_pivote, r)
                    pasos.append((rf"F_{{{fila_pivote+1}}} \leftrightarrow F_{{{r+1}}}", M.copy()))
                    pivote_val = M[fila_pivote, col]
                    break
        if pivote_val == 0: continue
        if pivote_val != 1:
            M.row_op(fila_pivote, lambda v, j: sp.simplify(v / pivote_val))
            pasos.append((rf"\frac{{F_{{{fila_pivote+1}}}}}{{{sp.latex(pivote_val)}}} \rightarrow F_{{{fila_pivote+1}}}", M.copy()))
        for r in range(filas):
            if r != fila_pivote:
                factor = M[r, col]
                if factor != 0:
                    M.row_op(r, lambda v, j: sp.simplify(v - factor * M[fila_pivote, j]))
                    if factor < 0:
                        op = rf"F_{{{r+1}}} + {sp.latex(-factor)}F_{{{fila_pivote+1}}} \rightarrow F_{{{r+1}}}"
                    else:
                        op = rf"F_{{{r+1}}} - {sp.latex(factor)}F_{{{fila_pivote+1}}} \rightarrow F_{{{r+1}}}"
                    pasos.append((op, M.copy()))
        fila_pivote += 1
    return M, pasos


# ==========================================
# PANTALLA 1: INICIO (LA SORPRESA)
# ==========================================
if st.session_state.pantalla == "inicio":
    
    st.markdown("""
    <style>
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    footer {visibility: hidden;}
    
    /* --- AQUÍ ESTÁ LA MAGIA PARA OCULTAR LOS LINKS EN EL INICIO TAMBIÉN --- */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a, a.header-anchor {
        display: none !important;
    }
    
    .anim-container {
        text-align: center; font-family: "Arial Black", sans-serif; font-size: 6rem;
        font-weight: bold; cursor: pointer; position: relative; height: 180px;
        display: flex; justify-content: center; align-items: center; margin-bottom: 10px;
    }
    .aea-text { position: absolute; transition: opacity 0.3s ease-out, transform 0.3s ease-out; }
    .algebra-wrapper {
        position: absolute; opacity: 0; width: 600px; display: flex; justify-content: flex-start;
    }
    .algebra-text {
        letter-spacing: 10px; overflow: hidden; white-space: nowrap;
        border-right: 6px solid transparent; padding-right: 15px; width: 0;
    }
    .anim-container:hover .aea-text { opacity: 0; transform: scale(1.1); }
    .anim-container:hover .algebra-wrapper { opacity: 1; }
    .anim-container:hover .algebra-text {
        animation: typing 0.7s steps(7, end) forwards, blinkCursor 0.8s infinite;
    }
    @keyframes typing { from { width: 0; } to { width: 100%; } }
    @keyframes blinkCursor { 0%, 100% { border-right-color: transparent; } 50% { border-right-color: #2680C2; } }
    
    .stButton>button {
        background-color: transparent !important;
        border: 2px solid transparent !important;
        color: #555555 !important;
        font-family: "Arial", sans-serif;
        font-size: 1rem;
        letter-spacing: 5px;
        transition: all 0.5s ease;
    }
    .stButton>button:hover {
        border: 2px solid #74BCA1 !important;
        color: #74BCA1 !important;
        box-shadow: 0 0 15px rgba(116, 188, 161, 0.4);
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("<br><br><br><br><br>", unsafe_allow_html=True)
    
    html_logo = """
    <div class="anim-container">
        <div class="aea-text">
            <span style='color: #C0DAE5;'>A</span><span style='color: #2680C2;'>E</span><span style='color: #74BCA1;'>A</span>
        </div>
        <div class="algebra-wrapper">
            <div class="algebra-text">
                <span style='color: #C0DAE5;'>Á</span><span style='color: #2680C2;'>L</span><span style='color: #2680C2;'>G</span><span style='color: #2680C2;'>E</span><span style='color: #2680C2;'>B</span><span style='color: #2680C2;'>R</span><span style='color: #74BCA1;'>A</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html_logo, unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #444; letter-spacing: 3px;'>PROYECTO FINAL - ÁLGEBRA LINEAL</h4>", unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    
    col_izq, col_centro, col_der = st.columns([2, 2, 2])
    with col_centro:
        if st.button("PLAY", use_container_width=True):
            st.session_state.pantalla = "motor"
            st.rerun()

# ==========================================
# PANTALLA 2: MOTOR ALGEBRAICO (CON TELÓN)
# ==========================================
elif st.session_state.pantalla == "motor":
    
    st.markdown("""
    <style>
    /* Efecto Telón */
    .curtain {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 999999; display: flex;
    }
    .curtain-half {
        width: 50%; height: 100%; background: #0e1117;
        animation: openCurtain 1.5s cubic-bezier(0.77, 0, 0.175, 1) forwards;
    }
    .curtain-half.left { transform-origin: left; border-right: 1px solid #2680C2; }
    .curtain-half.right { transform-origin: right; border-left: 1px solid #74BCA1; }
    
    @keyframes openCurtain {
        0% { transform: scaleX(1); }
        100% { transform: scaleX(0); }
    }
    
    [data-testid="collapsedControl"] {display: block;}
    
    /* Ocultar links de títulos en el Motor */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a, a.header-anchor {
        display: none !important;
    }
    
    .mini-logo {
        text-align: left; font-family: "Arial Black", sans-serif; font-size: 2.5rem;
        font-weight: bold; margin-bottom: 20px;
    }
    </style>
    
    <div class="curtain">
        <div class="curtain-half left"></div>
        <div class="curtain-half right"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- LOGO ANIMADO PARA LA PANTALLA DEL MOTOR ---
    st.markdown("""
    <style>
    .anim-container-motor {
        text-align: left; font-family: "Arial Black", sans-serif; font-size: 2.5rem;
        font-weight: bold; cursor: pointer; position: relative; height: 60px;
        display: flex; justify-content: flex-start; align-items: center; margin-bottom: 20px;
    }
    .aea-text-motor { 
        position: absolute; transition: opacity 0.3s ease-out; display: flex; align-items: center; 
    }
    .algebra-wrapper-motor {
        position: absolute; opacity: 0; display: flex; align-items: center;
    }
    .algebra-text-motor {
        letter-spacing: 6px; overflow: hidden; white-space: nowrap;
        border-right: 4px solid transparent; padding-right: 8px; width: 0;
    }
    .anim-container-motor:hover .aea-text-motor { opacity: 0; }
    .anim-container-motor:hover .algebra-wrapper-motor { opacity: 1; }
    .anim-container-motor:hover .algebra-text-motor {
        animation: typing-m 0.6s steps(7, end) forwards, blink-m 0.8s infinite;
    }
    @keyframes typing-m { from { width: 0; } to { width: 260px; } }
    @keyframes blink-m { 0%, 100% { border-right-color: transparent; } 50% { border-right-color: #2680C2; } }
    .suffix-motor {
        color: white; font-size: 1.5rem; font-weight: normal; margin-left: 10px; font-family: "Arial", sans-serif; white-space: nowrap;
    }
    </style>
    
    <div class="anim-container-motor">
        <div class="aea-text-motor">
            <span style='color: #C0DAE5;'>A</span><span style='color: #2680C2;'>E</span><span style='color: #74BCA1;'>A</span>
            <span class="suffix-motor"></span>
        </div>
        <div class="algebra-wrapper-motor">
            <div class="algebra-text-motor">
                <span style='color: #C0DAE5;'>Á</span><span style='color: #2680C2;'>L</span><span style='color: #2680C2;'>G</span><span style='color: #2680C2;'>E</span><span style='color: #2680C2;'>B</span><span style='color: #2680C2;'>R</span><span style='color: #74BCA1;'>A</span>
            </div>
            <span class="suffix-motor"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("Regresar al Inicio", use_container_width=True):
        st.session_state.pantalla = "inicio"
        st.rerun()
    
    st.sidebar.markdown("---")

    # --- PANEL LATERAL ---
    st.sidebar.header("⚙️ Parámetros")
    operacion = st.sidebar.selectbox("📖 Tema a resolver:", [
        "Espacios Nulos", "Conjuntos de Bases", "Sistemas de Coordenadas", "Diagonalización"
    ])

    col1, col2 = st.sidebar.columns(2)
    filas = col1.number_input("Filas", min_value=1, max_value=8, value=3)
    cols = col2.number_input("Columnas", min_value=1, max_value=8, value=4)

    # --- LÓGICA DE DIMENSIONES (DOBLE MEMORIA) ---
    if "df_matriz" not in st.session_state:
        df_ini = pd.DataFrame([["0"] * cols for _ in range(filas)])
        st.session_state.df_matriz = df_ini
        st.session_state.matriz_actual = df_ini.copy()
    else:
        old_df = st.session_state.matriz_actual
        old_f, old_c = old_df.shape
        if old_f != filas or old_c != cols:
            new_df = pd.DataFrame([["0"] * cols for _ in range(filas)])
            min_f, min_c = min(old_f, filas), min(old_c, cols)
            for i in range(min_f):
                for j in range(min_c):
                    new_df.iat[i, j] = old_df.iat[i, j]
            st.session_state.df_matriz = new_df
            st.session_state.matriz_actual = new_df.copy()

    # --- ÁREA CENTRAL ---
    st.write("### 📝 Editor de Matriz")

    t1, t2, t3, t4 = st.columns(4)
    if t1.button("🧹 Limpiar Todo", use_container_width=True):
        guardar_historial()
        new_df = pd.DataFrame([["0"] * cols for _ in range(filas)])
        st.session_state.df_matriz = new_df
        st.session_state.matriz_actual = new_df.copy()
        st.rerun()
    if t2.button("🎲 Aleatorio", use_container_width=True):
        guardar_historial()
        new_df = pd.DataFrame([[str(random.randint(-9, 9)) for _ in range(cols)] for _ in range(filas)])
        st.session_state.df_matriz = new_df
        st.session_state.matriz_actual = new_df.copy()
        st.rerun()
    if t3.button("ℹ️ Identidad", use_container_width=True):
        guardar_historial()
        new_df = pd.DataFrame([["0"] * cols for _ in range(filas)])
        for i in range(min(filas, cols)):
            new_df.iat[i, i] = "1"
        st.session_state.df_matriz = new_df
        st.session_state.matriz_actual = new_df.copy()
        st.rerun()
    if t4.button("↩️ Retroceder", use_container_width=True):
        if st.session_state.history:
            prev_df = st.session_state.history.pop()
            st.session_state.df_matriz = prev_df
            st.session_state.matriz_actual = prev_df.copy()
            st.rerun()
        else:
            st.toast("No hay más acciones para deshacer 🛑")

    df_editado = st.data_editor(st.session_state.df_matriz, use_container_width=True)
    
    st.session_state.matriz_actual = df_editado.copy()

    # --- MOTOR DE CÁLCULO ---
    col_calc1, col_calc2 = st.columns([1.5, 4])
    with col_calc1:
        btn_calcular = st.button("🚀 CALCULAR RESULTADO", type="primary", use_container_width=True)

    if btn_calcular:
        try:
            M = sp.Matrix(df_editado.values.tolist())
            M_rref, pivotes = M.rref()

            st.markdown("---")
            st.subheader("🎯 Resultado Principal")

            if operacion == "Espacios Nulos":
                base_nul = M.nullspace()
                col_a, col_b = st.columns(2)
                with col_a:
                    st.latex(r"\text{Matriz Escalonada Reducida:}")
                    st.latex(sp.latex(M_rref))
                with col_b:
                    if not base_nul:
                        st.latex(r"\text{Nul } A = \{\mathbf{0}\}")
                    else:
                        st.latex(r"\text{Base Nul A:}")
                        for vec in base_nul: st.latex(sp.latex(vec))

            elif operacion == "Conjuntos de Bases":
                col_a, col_b = st.columns(2)
                with col_a:
                    st.latex(r"\text{Matriz Escalonada Reducida:}")
                    st.latex(sp.latex(M_rref))
                with col_b:
                    indices_base = [i + 1 for i in pivotes]
                    st.latex(rf"\text{{Columnas que forman la Base (Col A): }} {indices_base}")

            elif operacion == "Sistemas de Coordenadas":
                vector_coord = M_rref[:, -1]
                col_a, col_b = st.columns(2)
                with col_a:
                    st.latex(r"\text{Matriz Aumentada Reducida:}")
                    st.latex(sp.latex(M_rref))
                with col_b:
                    st.latex(r"[\mathbf{x}]_{\mathcal{B}} = " + sp.latex(vector_coord))

            elif operacion == "Diagonalización":
                if M.rows != M.cols: st.error("Debe ser cuadrada para Diagonalizar.")
                elif not M.is_diagonalizable(): st.warning("La matriz NO es diagonalizable.")
                else:
                    P, D = M.diagonalize()
                    P_inv = P.inv()
                    c1, c2, c3 = st.columns(3)
                    c1.latex(r"P = " + sp.latex(P))
                    c2.latex(r"D = " + sp.latex(D))
                    c3.latex(r"P^{-1} = " + sp.latex(P_inv))

            # --- DESARROLLO PASO A PASO ---
            with st.expander("🔍 Ver Desarrollo Paso a Paso (Gauss-Jordan)"):
                if operacion in ["Espacios Nulos", "Conjuntos de Bases", "Sistemas de Coordenadas"]:
                    st.latex(r"\text{Matriz Inicial: } " + sp.latex(M))
                    _, pasos = obtener_pasos_gauss_jordan(M)
                    for op, matriz_paso in pasos:
                        st.latex(op)
                        st.latex(sp.latex(matriz_paso))
                elif operacion == "Diagonalización":
                    st.latex(r"\text{Cálculo de Valores y Vectores Propios:}")
                    for val, mult, vects in M.eigenvects():
                        st.latex(rf"\lambda = {sp.latex(val)}")
                        for i, v in enumerate(vects): st.latex(sp.latex(v))

        except Exception as e:
            st.error(f"Error en los datos. Revisa los valores ingresados. Detalle: {e}")