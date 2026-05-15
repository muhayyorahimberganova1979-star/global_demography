"""
Global Demografiya Tahlili - Frontend (Streamlit)
=================================================
Interaktiv demografik tahlil interfeysi
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  SOZLAMALAR
# ─────────────────────────────────────────────
import os
API_URL = os.environ.get("API_URL", "http://localhost:5000")

st.set_page_config(
    page_title="🌍 Global Demografiya Tahlili",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a73e8;
        border-bottom: 3px solid #1a73e8;
        padding-bottom: 0.4rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

RANG_XARITA = {
    'Asia': '#FF2D55',
    'Europe': '#007AFF',
    'Africa': '#FFCC00',
    'North America': '#34C759',
    'South America': '#AF52DE',
    'Oceania': '#5856D6'
}

# ─────────────────────────────────────────────
#  PREMIUM DARK MODE CSS (Glassmorphism 2.0)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {
        --bg-dark: #0f172a;
        --sidebar-bg: rgba(30, 41, 59, 0.4);
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --text-main: #f8fafc;
        --text-dim: #94a3b8;
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }
    
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%);
    }
    
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        background: linear-gradient(to right, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 3rem 0;
        filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.3));
    }
    
    .stMetric {
        background: rgba(30, 41, 59, 0.5) !important;
        backdrop-filter: blur(10px);
        padding: 1.5rem !important;
        border-radius: 24px !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        border-color: var(--accent-blue);
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--glass-border);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .info-card {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
    }
    
    .info-card small {
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    
    .info-card b, .info-card h3, .info-card p {
        color: #f8fafc !important;
    }

    /* Metric label & value visibility */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }
    [data-testid="stMetricDelta"] {
        opacity: 0.85;
    }

    /* Ensure all text elements visible on dark bg */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1,
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
        color: #f8fafc !important;
    }

    .stCaption, .stCaption p {
        color: #94a3b8 !important;
    }

    /* Selectbox, multiselect, slider text */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stTextInput label, .stRadio label {
        color: #f8fafc !important;
    }

    /* Dataframe header */
    [data-testid="stDataFrame"] {
        color: #f8fafc;
    }
    
    /* Better Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(30, 41, 59, 0.3);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: var(--text-dim) !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
        color: white !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  API FUNKSIYALAR
# ─────────────────────────────────────────────

@st.cache_data(ttl=300)
def api_so_rov(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_URL}{endpoint}", params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except:
        return None


def api_bor_mi() -> bool:
    try:
        return requests.get(API_URL, timeout=3).status_code == 200
    except:
        return False


# ─────────────────────────────────────────────
#  GRAFIKLAR
# ─────────────────────────────────────────────

def aholi_xarita(davlatlar):
    df = pd.DataFrame(davlatlar)
    fig = px.choropleth(
        df, locations='kod', color='aholi', hover_name='davlat',
        hover_data={'kod': False, 'qita': True, 'aholi': ':,'},
        color_continuous_scale='Magma',
        title='🌍 Jahon aholisi zichligi xaritasi',
        labels={'aholi': 'Aholi'}
    )
    fig.update_layout(
        height=600, margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showframe=False, 
            bgcolor='rgba(0,0,0,0)',
            showcoastlines=True, coastlinecolor="#334155",
            showland=True, landcolor="#1e293b",
            showocean=True, oceancolor="#0f172a"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc")
    )
    return fig


def qita_doira(qitalar):
    df = pd.DataFrame(qitalar)
    fig = px.pie(df, values='jami_aholi', names='qita',
                 title="Qit'alar bo'yicha aholi taqsimoti",
                 color='qita', color_discrete_map=RANG_XARITA, hole=0.6)
    fig.update_traces(textposition='outside', textinfo='label+percent',
                      marker=dict(line=dict(color='#0f172a', width=3)))
    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc"),
        showlegend=False
    )
    return fig


def qita_taqqos(qitalar):
    df = pd.DataFrame(qitalar)
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("O'rtacha umr", "O'rtacha AHM (USD)",
                                        "Fertillik darajasi", "Shaharlik %"),
                        vertical_spacing=0.2)
    ranglar = [RANG_XARITA.get(q, '#888') for q in df['qita']]
    pairs = [('urtacha_umr', 1, 1), ('urtacha_gdp', 1, 2),
             ('urtacha_fertillik', 2, 1), ('urtacha_shaharlik', 2, 2)]
    for col_name, row, col in pairs:
        fig.add_trace(go.Bar(
            x=df['qita'], y=df[col_name],
            marker_color=ranglar,
            marker_line_width=0,
            showlegend=False,
            text=[f"{v:.1f}" for v in df[col_name]],
            textposition='outside',
        ), row=row, col=col)
    fig.update_layout(
        height=700, 
        title_text="Qit'alar bo'yicha tahlil paneli",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc"),
        margin=dict(t=100)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def top_gorizontal(davlatlar, ustun, sarlavha, rang='Viridis'):
    df = pd.DataFrame(davlatlar).iloc[::-1]
    fig = px.bar(df, x=ustun, y='davlat', orientation='h',
                 color=ustun, color_continuous_scale=rang,
                 text=ustun, title=sarlavha)
    fig.update_traces(texttemplate='%{text:,.1f}', textposition='outside',
                      marker=dict(line_width=0))
    fig.update_layout(
        height=500, coloraxis_showscale=False,
        margin=dict(l=130, r=60, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc")
    )
    return fig


def radar_taqqos(taqqos):
    kategoriyalar = ["Umr", "GDP/10k", "Shaharlik %", "Savodxonlik",
                     "100-Fertillik*10", "100-Tug'ilish"]
    fig = go.Figure()
    for d in taqqos:
        qiymatlar = [
            d['umr_davomiyligi'],
            d['gdp_per_capita'] / 10000,
            d['shaharlik'],
            d['savodxonlik'],
            100 - d['fertillik'] * 10,
            100 - d['tug_ilish']
        ]
        fig.add_trace(go.Scatterpolar(
            r=qiymatlar, theta=kategoriyalar,
            fill='toself', name=d['davlat'], opacity=0.6,
            line=dict(width=3)
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            bgcolor="rgba(30,41,59,0.2)"
        ),
        showlegend=True, title="Radar tahlil matritsasi", height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc")
    )
    return fig


def scatter_gdp_umr(scatter_data, qita=None):
    df = pd.DataFrame(scatter_data)
    fig = px.scatter(
        df, x='gdp', y='umr', color='qita',
        size='aholi', hover_name='davlat',
        size_max=60,
        title="Boylik va umr davomiyligi bog'liqligi",
        labels={'gdp': 'AHM (USD)', 'umr': 'Umr davomiyligi', 'qita': "Qit'a"},
        color_discrete_map=RANG_XARITA, log_x=True
    )
    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.02)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor="rgba(255,255,255,0.1)")
    )
    return fig


def korrelatsiya_xarita(matritsa, ustunlar):
    df = pd.DataFrame(matritsa)
    qisqa = {
        'gdp_per_capita': 'AHM', 'life_expectancy': 'Umr',
        'birth_rate': "Tug'ilish", 'death_rate': "O'lim",
        'fertility_rate': 'Fertillik', 'median_age': 'Yosh',
        'urban_population_pct': 'Shaharlik', 'literacy_rate': 'Savodxonlik'
    }
    df.index = [qisqa.get(u, u) for u in ustunlar]
    df.columns = [qisqa.get(u, u) for u in ustunlar]
    fig = px.imshow(df, text_auto='.2f', color_continuous_scale='Magma',
                    zmin=-1, zmax=1,
                    title="Demografik o'zgaruvchilar korrelyatsiya matritsasi",
                    aspect='auto')
    fig.update_layout(
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f8fafc")
    )
    return fig


# ─────────────────────────────────────────────
#  SAHIFALAR
# ─────────────────────────────────────────────

def sahifa_bosh(stat, davlatlar, qitalar):
    st.markdown('<div class="main-header">🌍 GLOBAL DEMOGRAFIYA TAHLILI</div>', unsafe_allow_html=True)
    
    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🌍 DAVLATLAR", stat.get('jami_davlatlar', '-'))
    c2.metric("👥 JAMI AHOLI", f"{stat.get('jami_aholi', 0) / 1e9:.2f} mlrd")
    c3.metric("⏳ UMRI", f"{stat.get('global_urtacha_umr', '-')} yil")
    c4.metric("💰 O'RT. AHM", f"${stat.get('global_urtacha_gdp', 0):,.0f}")
    c5.metric("👶 FERTILLIK", stat.get('global_urtacha_fertillik', '-'))
    
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        if davlatlar:
            st.plotly_chart(aholi_xarita(davlatlar), use_container_width=True)
    with col_b:
        if qitalar:
            st.plotly_chart(qita_doira(qitalar), use_container_width=True)

    st.markdown('<div class="section-header">🏆 Global ko\'rsatkichlar</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    eng_kop = stat.get('eng_kop_aholi', {})
    eng_umr = stat.get('eng_yuqori_umr', {})
    past_umr = stat.get('eng_past_umr', {})
    eng_gdp = stat.get('eng_yuqori_gdp', {})
    
    r1.markdown(f"""<div class="info-card"><small style="color:var(--accent-blue)">ENG KO'P AHOLI</small><br><b>{eng_kop.get('davlat')}</b><br><h3 style="margin:0; color:#fff;">{eng_kop.get('aholi', 0):,}</h3></div>""", unsafe_allow_html=True)
    r2.markdown(f"""<div class="info-card"><small style="color:var(--accent-purple)">UMR DAVOMIYLIGI</small><br><b>{eng_umr.get('davlat')}</b><br><h3 style="margin:0; color:#fff;">{eng_umr.get('yil')} yil</h3></div>""", unsafe_allow_html=True)
    r3.markdown(f"""<div class="info-card"><small style="color:var(--accent-pink)">ENG PAST UMR</small><br><b>{past_umr.get('davlat')}</b><br><h3 style="margin:0; color:#fff;">{past_umr.get('yil')} yil</h3></div>""", unsafe_allow_html=True)
    r4.markdown(f"""<div class="info-card"><small style="color:var(--accent-blue)">ENG YUQORI AHM</small><br><b>{eng_gdp.get('davlat')}</b><br><h3 style="margin:0; color:#fff;">${eng_gdp.get('usd', 0):,.0f}</h3></div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Ko\'p o\'lchovli tahlil</div>', unsafe_allow_html=True)
    if qitalar:
        st.plotly_chart(qita_taqqos(qitalar), use_container_width=True)


def sahifa_top():
    st.markdown('<div class="section-header">🏅 Top davlatlar reytingi</div>', unsafe_allow_html=True)
    
    col_n1, col_n2 = st.columns([2, 1])
    with col_n1:
        n = st.select_slider("Oraliqni tanlang", options=[5, 10, 15, 20, 25, 30], value=10)
    
    tab1, tab2, tab3 = st.tabs(["👥 Aholi", "⏳ Umr davomiyligi", "💰 Iqtisodiyot"])

    with tab1:
        data = api_so_rov('/api/top-aholi', {'n': n})
        if data:
            lst = [{'davlat': d['davlat'], 'qita': d['qita'],
                    'population': d['population'] / 1e6} for d in data['davlatlar']]
            st.plotly_chart(top_gorizontal(lst, 'population',
                                           f"Aholi bo'yicha Top {n} davlat (Millionlarda)", 'Viridis'),
                            use_container_width=True)
            
            df = pd.DataFrame(data['davlatlar'])
            st.markdown("##### Batafsil reyting")
            st.dataframe(df[["o'rin", 'davlat', 'qita', 'population']].rename(
                columns={"o'rin": "O'rin", 'davlat': 'Davlat', 'qita': "Qit'a", 'population': 'Aholi'}
            ), use_container_width=True, hide_index=True)

    with tab2:
        data = api_so_rov('/api/top-umr', {'n': n})
        if data:
            lst = [{'davlat': d['davlat'], 'qita': d['qita'],
                    'life_expectancy': d['life_expectancy']} for d in data['davlatlar']]
            st.plotly_chart(top_gorizontal(lst, 'life_expectancy',
                                           f"Umr davomiyligi bo'yicha Top {n} davlat (Yillarda)", 'Cividis'),
                            use_container_width=True)

    with tab3:
        data = api_so_rov('/api/top-gdp', {'n': n})
        if data:
            lst = [{'davlat': d['davlat'], 'qita': d['qita'],
                    'gdp_per_capita': d['gdp_per_capita']} for d in data['davlatlar']]
            st.plotly_chart(top_gorizontal(lst, 'gdp_per_capita',
                                           f"AHM bo'yicha Top {n} davlat (USD)", 'Plasma'),
                            use_container_width=True)


def sahifa_davlat():
    st.markdown('<div class="section-header">🔍 Davlat Tahlili</div>', unsafe_allow_html=True)
    
    with st.spinner("Davlatlar ro'yxati yuklanmoqda..."):
        davlatlar_data = api_so_rov('/api/davlatlar')
        
    if not davlatlar_data:
        st.error("Ma'lumot yuklanmadi")
        return

    nom_kod = {d['davlat']: d['kod'] for d in davlatlar_data['davlatlar']}
    nomlar = sorted(nom_kod.keys())

    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        tanlangan = st.selectbox("Davlatni tanlang:", nomlar, index=nomlar.index('Uzbekistan') if 'Uzbekistan' in nomlar else 0)
    with col_s2:
        qid = st.text_input("🔎 Tezkor qidiruv:", placeholder="Masalan: Germany")
        if qid and len(qid) >= 2:
            res = api_so_rov('/api/qidirish', {'q': qid})
            if res and res.get('natijalar'):
                tanlangan = res['natijalar'][0]['davlat']

    kod = nom_kod.get(tanlangan, '')
    data = api_so_rov(f'/api/davlat/{kod}')
    if not data:
        st.error("Ma'lumot topilmadi")
        return

    # Davlat kartasi
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.6); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem; backdrop-filter: blur(10px);">
        <h2 style="margin:0; color:#60a5fa;">🏳 {data['davlat']} ({data['kod']})</h2>
        <p style="font-size:1.2rem; color:#94a3b8;"><b style='color:#f8fafc;'>Qit'a:</b> {data['qita']} | <b style='color:#f8fafc;'>Tavsif:</b> {data['tavsif']}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Aholi", f"{data['aholi']:,}", delta=f"Reyting: {data['aholi_reyting']}")
    c2.metric("💰 AHM", f"${data['gdp_per_capita']:,.0f}", delta=f"Reyting: {data['gdp_reyting']}")
    c3.metric("⏳ Umr", f"{data['umr_davomiyligi']} yil", delta=f"Reyting: {data['umr_reyting']}")
    c4.metric("📚 Savodxonlik", f"{data['savodxonlik']}%")

    st.markdown("---")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("👶 Fertillik", data['fertillik_darajasi'])
    d2.metric("🏙 Shaharlik", f"{data['shahar_aholi_ulushi']}%")
    d3.metric("🎂 O'rt. yosh", f"{data['urtacha_yosh']} yil")
    d4.metric("📈 Tug'ilish", f"{data['tug_ilish_darajasi']}‰")

    st.markdown("#### 📊 Demografik ko'rsatkichlar (Gauges)")
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'indicator'}] * 3])
    
    gauges = [
        (data['umr_davomiyligi'], "Umr davomiyligi", [40, 95], "#2ecc71"),
        (data['savodxonlik'], "Savodxonlik (%)", [0, 100], "#3498db"),
        (data['shahar_aholi_ulushi'], "Shaharlik (%)", [0, 100], "#9b59b6")
    ]
    
    for i, (val, title, rng, color) in enumerate(gauges, 1):
        fig.add_trace(go.Indicator(
            mode="gauge+number", value=val,
            title={'text': title, 'font': {'size': 18}},
            gauge={
                'axis': {'range': rng, 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [rng[0], (rng[0]+rng[1])/2], 'color': 'rgba(0,0,0,0.05)'}
                ],
            }
        ), row=1, col=i)
        
    fig.update_layout(
        height=350, 
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)


def sahifa_taqqoslash():
    st.markdown('<div class="section-header">⚖️ Kengaytirilgan taqqoslash tahlili</div>', unsafe_allow_html=True)
    
    with st.spinner("Ma'lumotlar yuklanmoqda..."):
        davlatlar_data = api_so_rov('/api/davlatlar')
        
    if not davlatlar_data:
        st.error("Ma'lumot yuklanmadi")
        return

    nom_kod = {d['davlat']: d['kod'] for d in davlatlar_data['davlatlar']}
    nomlar = sorted(nom_kod.keys())
    default = [x for x in ['Uzbekistan', 'China', 'Germany', 'United States', 'India'] if x in nomlar]

    tanlangan = st.multiselect("Davlatlarni tanlang (2-8):", nomlar, default=default or nomlar[:5])
    if len(tanlangan) < 2:
        st.warning("Taqqoslash uchun kamida 2 ta davlat tanlang.")
        return

    kodlar = ",".join([nom_kod[n] for n in tanlangan[:8]])
    data = api_so_rov('/api/taqqoslash', {'kodlar': kodlar})
    if not data or not data.get('taqqoslash'):
        st.error("Ma'lumotlarni yuklashda xatolik.")
        return

    t = data['taqqoslash']
    df = pd.DataFrame(t)

    st.markdown("##### Taqqoslash jadvali")
    st.dataframe(df.rename(columns={
        'davlat': 'Davlat', 'qita': "Qit'a", 'aholi': 'Aholi',
        'gdp_per_capita': 'AHM', 'umr_davomiyligi': 'Umr',
        'tug_ilish': "Tug'ilish", 'shaharlik': 'Shaharlik %',
        'fertillik': 'Fertillik', 'urtacha_yosh': "O'rt. yosh",
        'savodxonlik': 'Savodxonlik'
    }).drop(columns=['kod', 'olim'], errors='ignore'),
                 use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_taqqos(t), use_container_width=True)
    with col2:
        fig = px.bar(df, x='davlat', y='aholi', color='qita',
                     title="Aholi hajmi tahlili", color_discrete_map=RANG_XARITA,
                     text='aholi')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans", color="#fff"))
        st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x='gdp_per_capita', y='umr_davomiyligi',
                      color='davlat', size='aholi', size_max=50, text='davlat',
                      title="Iqtisodiyot va umr davomiyligi",
                      labels={'gdp_per_capita': 'AHM (USD)', 'umr_davomiyligi': 'Umr (Yillar)'})
    fig2.update_traces(textposition='top center')
    fig2.update_layout(height=480, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)', font=dict(family="Plus Jakarta Sans", color="#fff"))
    st.plotly_chart(fig2, use_container_width=True)


def sahifa_korrelyatsiya():
    st.markdown('<div class="section-header">📈 Ko\'p o\'zgaruvchili korrelyatsiya tahlili</div>', unsafe_allow_html=True)

    qita_list = ['Global', 'Asia', 'Europe', 'Africa',
                 'North America', 'South America', 'Oceania']
    
    col1_f, col2_f = st.columns([1, 2])
    with col1_f:
        qita = st.selectbox("Hudud filtri:", qita_list)
    
    params = {} if qita == 'Global' else {'qita': qita}
    sc_data = api_so_rov('/api/aholi-tahlili', params)

    if sc_data:
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("AHM–UMR KORRELYATSIYASI", sc_data['gdp_umr_korrelyatsiya'])
        col2.metric("AHM–FERTILLIK KORRELYATSIYASI", sc_data['gdp_fertillik_korrelyatsiya'])
        st.plotly_chart(scatter_gdp_umr(sc_data['scatter_data']), use_container_width=True)

    corr = api_so_rov('/api/korrelatsiya')
    if corr:
        st.plotly_chart(
            korrelatsiya_xarita(corr['matritsa'], corr['ustunlar']),
            use_container_width=True
        )
        kuchli = corr.get('kuchli_korrelyatsiyalar', [])
        if kuchli:
            st.markdown("#### 🔗 Muhim aloqalar")
            df_k = pd.DataFrame(kuchli)
            df_k['korrelyatsiya'] = df_k['korrelyatsiya'].apply(lambda x: f"{x:+.3f}")
            st.dataframe(df_k.rename(columns={'ko_rsatkich_1': "Ko'rsatkich 1", 'ko_rsatkich_2': "Ko'rsatkich 2", 'korrelyatsiya': 'Indeks'}), 
                         use_container_width=True, hide_index=True)


def sahifa_tasnif():
    st.markdown('<div class="section-header">🏷 Demografik tasnif</div>', unsafe_allow_html=True)
    
    with st.spinner("Segmentlar tahlil qilinmoqda..."):
        data = api_so_rov('/api/demografik-tasnif')
        
    if not data:
        st.error("❌ Ma'lumotlarni yuklashda xatolik.")
        return

    tab1, tab2, tab3 = st.tabs(["💰 Boylik guruhlari", "⏳ Umr guruhlari", "👶 Fertillik guruhlari"])

    with tab1:
        if 'gdp_guruhlar' in data:
            df = pd.DataFrame(data['gdp_guruhlar'])
            if not df.empty:
                st.markdown("#### Jahon AHM taqsimoti")
                c1, c2 = st.columns(2)
                with c1:
                    fig = px.pie(df, values='soni', names='gdp_per_capita',
                                 title="Davlatlar soni", hole=0.5,
                                 color_discrete_sequence=px.colors.qualitative.Prism)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans", color="#fff"))
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    fig2 = px.bar(df, x='gdp_per_capita', y='jami_aholi',
                                  color='gdp_per_capita', title="Boylik guruhi bo'yicha aholi",
                                  color_discrete_sequence=px.colors.qualitative.Prism)
                    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans", color="#fff"))
                    st.plotly_chart(fig2, use_container_width=True)
                
                st.dataframe(df.rename(columns={
                    'gdp_per_capita': 'Boylik guruhi', 'soni': 'Davlatlar',
                    'jami_aholi': 'Aholi', 'urtacha_umr': "O'rt. umr"
                }), use_container_width=True, hide_index=True)

    with tab2:
        if 'umr_guruhlar' in data:
            df2 = pd.DataFrame(data['umr_guruhlar'])
            if not df2.empty:
                st.markdown("#### Umr davomiyligi segmentlari")
                fig = px.bar(df2, x='life_expectancy', y='soni', color='life_expectancy',
                             title="Umr guruhi bo'yicha davlatlar",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans", color="#fff"))
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df2.rename(columns={
                    'life_expectancy': 'Umr guruhi', 'soni': 'Davlatlar',
                    'jami_aholi': 'Aholi'
                }), use_container_width=True, hide_index=True)

    with tab3:
        if 'fertillik_guruhlar' in data:
            df3 = pd.DataFrame(data['fertillik_guruhlar'])
            if not df3.empty:
                st.markdown("#### Fertillik dinamikasi")
                fig = px.bar(df3, x='fertility_rate', y='soni', color='fertility_rate',
                             title="Fertillik guruhi bo'yicha davlatlar",
                             color_discrete_sequence=px.colors.qualitative.Safe)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans", color="#fff"))
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df3.rename(columns={
                    'fertility_rate': 'Fertillik guruhi', 'soni': 'Davlatlar',
                    'jami_aholi': 'Aholi'
                }), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  ASOSIY
# ─────────────────────────────────────────────

def main():
    if not api_bor_mi():
        st.error("⚠️ Backend API ishlamayapti!")
        st.info("""
**Iltimos avval backendni ishga tushiring:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Keyin bu sahifani yangilang (F5).
        """)
        st.stop()

    stat = api_so_rov('/api/umumiy-statistika') or {}
    davlatlar_data = api_so_rov('/api/davlatlar')
    davlatlar = davlatlar_data.get('davlatlar', []) if davlatlar_data else []
    qitalar_data = api_so_rov('/api/qitalar')
    qitalar = qitalar_data if isinstance(qitalar_data, list) else []

    with st.sidebar:
        st.markdown("### 🌍 Global Demografiya")
        st.markdown("---")
        sahifa = st.radio("📋 Bo'limlar:", [
            "🏠 Asosiy sahifa",
            "🏅 Top davlatlar",
            "🔍 Davlat tahlili",
            "⚖️ Taqqoslash",
            "📈 Korrelyatsiya",
            "🏷 Demografik tasnif"
        ])
        st.markdown("---")
        if stat:
            st.markdown(f"**Davlatlar:** {stat.get('jami_davlatlar', '-')}")
            st.markdown(f"**Jahon aholisi:** {stat.get('jami_aholi', 0) / 1e9:.2f} mlrd")
        st.markdown("---")
        st.caption("© 2024 Global Demografiya\nFlask | Streamlit | Plotly | Pandas")

    if "Asosiy" in sahifa:
        sahifa_bosh(stat, davlatlar, qitalar)
    elif "Top" in sahifa:
        sahifa_top()
    elif "Davlat" in sahifa:
        sahifa_davlat()
    elif "Taqqoslash" in sahifa:
        sahifa_taqqoslash()
    elif "Korrelyatsiya" in sahifa:
        sahifa_korrelyatsiya()
    elif "Tasnif" in sahifa.lower() or "tasnif" in sahifa.lower():
        sahifa_tasnif()


if __name__ == '__main__':
    main()
