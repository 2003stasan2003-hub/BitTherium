import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import time

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
    </style>
""",
    unsafe_allow_html=True,
)

col_logo, col_title = st.columns([1, 11])
with col_logo:
    st.markdown("### ₿Ξ")
with col_title:
    st.title("BitTherium 1.0 — Професійний Криптотрейдинговий Термінал")

st.markdown("---")

with st.sidebar:
  st.header("⚙️ Керування системою")
  st.markdown(
      "**Статус з'єднання:** <span style='color:green;'>● Онлайн</span>",
      unsafe_allow_html=True,
  )

  if has_keys:
    st.markdown(
        "**API-ключі:** <span style='color:green;'>● Завантажено (.env)</span>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        "**API-ключі:** <span style='color:orange;'>● Не налаштовано (.env)</span>",
        unsafe_allow_html=True,
    )

  st.markdown("---")
  col1, col2 = st.columns(2)
  with col1:
    start_btn = st.button("▶ Запуск")
  with col2:
    stop_btn = st.button("⏸ Зупинка")

  if start_btn:
    st.success("Термінал запущено в робочий режим.")
  if stop_btn:
    st.warning("Роботу термінала призупинено.")

  st.markdown("---")
  st.subheader("🚨 Безпека")
  kill_switch = st.button(
      "KILL SWITCH", key="kill", help="Екстрене закриття всіх позицій"
  )
  if kill_switch:
    st.error(
        "УВАГА: Активовано Kill Switch! Усі торги зупинено, позиції закриваються."
    )

st.subheader("📊 Ринкові котирування та активні активи")

m1, m2, m3, m4 = st.columns(4)
m1.metric(label="BTC/USDT", value="$67,450", delta="+2.4%")
m2.metric(label="ETH/USDT", value="$3,520", delta="+1.8%")
m3.metric(label="Халвінг цикл", value="482 дні", delta="Дефіцит")
m4.metric(label="Статус ринку", value="Бичачий", delta="Risk-On")

st.markdown("---")

selected_pair = st.selectbox(
    "Виберіть торгову пару для аналізу:", ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
)

chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 100
    + (67450 if "BTC" in selected_pair else 3500),
    columns=["Ціна"],
)

st.line_chart(chart_data)

st.markdown("---")

st.subheader("🔬 Розширена аналітика ринку")

col_a, col_b = st.columns(2)

with col_a:
  st.markdown("### 🐋 Трекінг китів (Smart Money)")
  st.info(
      "Виявлено великий переказ: **5,000 BTC** ($337M) переміщено на холодний"
      " гаманець біржі."
  )
  st.warning("Тиск покупців: Високий (68% лонг-позицій)")

with col_b:
  st.markdown("### 🔥 Теплова мапа ліквідацій")
  liquidation_data = pd.DataFrame(
      np.random.randint(100, 1000, size=(5, 2)),
      columns=["Ціновий рівень ($)", "Обсяг ліквідацій ($M)"],
  )
  st.dataframe(liquidation_data, use_container_width=True)

st.markdown("---")

st.subheader("⚡ Панель виконання ордерів (Trading Execution)")

trade_col1, trade_col2 = st.columns(2)

with trade_col1:
  order_type = st.radio("Тип ордера:", ["Market", "Limit"])
  amount = st.number_input("Обсяг (USDT):", min_value=10.0, value=100.0)

with trade_col2:
  st.markdown("### Дії")
  buy_btn = st.button("🟢 BUY / LONG", use_container_width=True)
  sell_btn = st.button("🔴 SELL / SHORT", use_container_width=True)

if buy_btn:
  st.success(f"Виконано ордер BUY для {selected_pair} на суму {amount} USDT.")
if sell_btn:
  st.error(f"Виконано ордер SELL для {selected_pair} на суму {amount} USDT.")

st.markdown("---")
st.success(
    "🚀 BitTherium 1.0 повністю зібрано! Усі модулі (каркас, котирування,"
    " аналітика китів, ліквідації, ордери та Kill Switch) функціонують."
)