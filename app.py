import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")
has_keys = bool(api_key and secret_key and api_key != "ваш_api_ключ_тут")

st.set_page_config(
    page_title="BitTherium 1.0", page_icon="⚡", layout="wide", initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #161b22;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        font-weight: bold;
    }
    .kill-switch {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    
    /* ЗНИЩЕННЯ СТАНДАРТНИХ ВІДСТУПІВ САЙДБАРА STREAMLIT */
    section[data-testid="stSidebar"] {
        top: 0px !important;
    }
    section[data-testid="stSidebar"] div.stBlock {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:first-child {
        padding-top: 0px !important;
        margin-top: -30px !important;
    }

    /* БЕЗШОВНИЙ ІДЕАЛЬНИЙ БЛОК БРЕНДУ У САМОМУ ВЕРХНЬОМУ КУТКУ */
    .absolute-hero-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        width: 100%;
    }
    .absolute-hero-logo {
        width: 85px !important; /* Великий об'ємний кругий логотип (~2 см) */
        height: 85px !important;
        object-fit: contain;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .absolute-hero-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
        line-height: 1.1;
        white-space: nowrap;
    }
    .absolute-hero-subtitle {
        font-size: 10px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 3px;
    }
    
    @media (max-width: 768px) {
        .stMetric {
            margin-bottom: 10px;
        }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Підключення до стабільного публічного API CoinGecko
@st.cache_data(ttl=15)
def get_live_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        eth_price = data['ethereum']['usd']
        sol_price = data['solana']['usd']
        
        btc_change = data['bitcoin'].get('usd_24h_change', 0.0)
        eth_change = data['ethereum'].get('usd_24h_change', 0.0)
        
        return {
            'success': True,
            'BTC': btc_price,
            'ETH': eth_price,
            'SOL': sol_price,
            'BTC_change': round(btc_change, 2),
            'ETH_change': round(eth_change, 2),
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'BTC': 67450.0,
            'ETH': 3520.0,
            'SOL': 145.0,
            'BTC_change': 2.4,
            'ETH_change': 1.8,
            'error': str(e)
        }

live_data = get_live_prices()

# Ініціалізація сесійної пам'яті
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

if 'system_active' not in st.session_state:
    st.session_state.system_active = True

if 'price_alerts' not in st.session_state:
    st.session_state.price_alerts = []

# САЙДБАР: Повністю безшовне розташування нового логотипа та назви в кутку
with st.sidebar:
    import base64
    
    logo_html = ""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{encoded}" class="absolute-hero-logo">'
    else:
        logo_html = '<span style="font-size: 45px;">₿Ξ</span>'

    st.markdown(
        f"""
        <div class="absolute-hero-brand">
            {logo_html}
            <div>
                <span class="absolute-hero-title">BitTherium</span><br>
                <span class="absolute-hero-subtitle">Професійний термінал</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.header("⚙️ Керування системою")
    if live_data['success']:
        st.markdown("**Статус з'єднання:** <span style='color:green;'>● Онлайн (Живі дані)</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Статус з'єднання:** <span style='color:orange;'>● Офлайн (Резерв)</span>", unsafe_allow_html=True)

    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        start_btn = st.button("▶ Запуск")
    with col_s2:
        stop_btn = st.button("⏸ Зупинка")

    if start_btn:
        st.session_state.system_active = True
        st.success("Термінал запущено.")
    if stop_btn:
        st.session_state.system_active = False
        st.warning("Термінал призупинено.")

    st.markdown("---")
    st.subheader("🚨 Безпека")
    if st.button("KILL SWITCH", key="kill", help="Екстрене закриття позицій"):
        st.session_state.system_active = False
        st.session_state.trade_history = []
        st.error("УВАГА: Активовано Kill Switch!")

# ГОЛОВНИЙ ЕКРАН: Горизонтальне меню вкладок
tab_home, tab_market_mgmt, tab_analytics, tab_macro, tab_params, tab_quotes, tab_history = st.tabs([
    "🏠 Головна", 
    "📊 Ринк-Менеджмент", 
    "📈 Аналітика", 
    "📰 Макропоказники", 
    "⚙️ Параметри", 
    "💱 Котирування", 
    "📜 Історія / Сесуг"
])

with tab_home:
    st.subheader("📊 Ринкові котирування в реальному часі")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Bitcoin (BTC/USDT)", value=f"${live_data['BTC']:,.2f}", delta=f"{live_data['BTC_change']}%")
    m2.metric(label="Ethereum (ETH/USDT)", value=f"${live_data['ETH']:,.2f}", delta=f"{live_data['ETH_change']}%")
    m3.metric(label="Solana (SOL/USDT)", value=f"${live_data['SOL']:,.2f}", delta="Live")
    m4.metric(label="Статус ринку", value="Бичачий", delta="Risk-On")

    st.markdown("---")
    selected_pair = st.selectbox("Виберіть торгову пару для графіка:", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
    base_price = live_data['BTC'] if "BTC" in selected_pair else (live_data['ETH'] if "ETH" in selected_pair else live_data['SOL'])

    # Інтерактивний графік свічок (Plotly)
    np.random.seed(42)
    dates = [pd.Timestamp.now() - pd.Timedelta(hours=i) for i in range(30)][::-1]
    opens = base_price + np.random.randn(30).cumsum() * (base_price * 0.001)
    closes = opens + np.random.randn(30) * (base_price * 0.0005)
    highs = np.maximum(opens, closes) + np.abs(np.random.randn(30)) * (base_price * 0.0003)
    lows = np.minimum(opens, closes) - np.abs(np.random.randn(30)) * (base_price * 0.0003)

    fig = go.Figure(data=[go.Candlestick(
        x=dates, open=opens, high=highs, low=lows, close=closes,
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True
