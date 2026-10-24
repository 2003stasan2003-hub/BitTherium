from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests
import random
import os

app = FastAPI(title="BitTherium 1.0 Terminal")

# Підключаємо статику (для логотипа та стилів)
if os.path.exists("logo.png"):
    app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/api/prices")
def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        res = requests.get(url, timeout=5).json()
        btc = res['bitcoin']['usd']
        eth = res['ethereum']['usd']
        sol = res['solana']['usd']
        btc_change = round(res['bitcoin'].get('usd_24h_change', 0.0), 2)
        eth_change = round(res['ethereum'].get('usd_24h_change', 0.0), 2)
        return {
            "success": True,
            "BTC": btc,
            "ETH": eth,
            "SOL": sol,
            "BTC_change": btc_change,
            "ETH_change": eth_change
        }
    except Exception:
        # Резервні дані при відсутності інтернету
        return {
            "success": False,
            "BTC": 67450.0,
            "ETH": 3520.0,
            "SOL": 145.0,
            "BTC_change": 2.4,
            "ETH_change": 1.8
        }

@app.get("/", response_class=HTMLResponse)
def serve_home():
    html_content = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BitTherium 1.0 - Професійний криптотермінал</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { background-color: #0e1117; color: #ffffff; display: flex; height: 100vh; overflow: hidden; }
            
            /* Сайдбар */
            sidebar {
                width: 300px;
                background-color: #161b22;
                border-right: 1px solid #30363d;
                display: flex;
                flex-direction: column;
                padding: 15px;
                overflow-y: auto;
            }
            .brand-container {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
            }
            .brand-logo {
                width: 95px;
                height: 95px;
                object-fit: contain;
                background: transparent;
            }
            .brand-title {
                font-size: 22px;
                font-weight: 800;
                color: #ffffff;
            }
            .brand-subtitle {
                font-size: 10px;
                color: #9ca3af;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 2px;
            }
            
            .section-title { font-size: 14px; font-weight: bold; margin: 15px 0 8px 0; color: #8b949e; }
            .btn {
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                margin-bottom: 8px;
                color: #fff;
            }
            .btn-start { background-color: #238636; }
            .btn-stop { background-color: #da3633; }
            .btn-kill { background-color: #f85149; font-size: 16px; margin-top: 10px; }
            
            /* Основна частина */
            main {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow-y: auto;
                padding: 20px;
            }
            .forecast-container {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .tabs {
                display: flex;
                gap: 10px;
                border-bottom: 1px solid #30363d;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            .tab-btn {
                background: none;
                border: none;
                color: #8b949e;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                padding: 6px 12px;
                border-radius: 4px;
            }
            .tab-btn.active { background: #30363d; color: #fff; }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            .metric-card {
                background: #161b22;
                border: 1px solid #30363d;
                padding: 15px;
                border-radius: 8px;
            }
            .metric-label { font-size: 12px; color: #8b949e; }
            .metric-value { font-size: 20px; font-weight: bold; margin-top: 5px; }
            
            @media(max-width: 768px) {
                body { flex-direction: column; overflow: auto; }
                sidebar { width: 100%; height: auto; }
                .metrics-grid { grid-template-columns: 1fr 1fr; }
            }
        </style>
    </head>
    <body>
        <sidebar>
            <div class="brand-container">
                <img src="/static/logo.png" class="brand-logo" alt="Logo">
                <div>
                    <div class="brand-title">BitTherium</div>
                    <div class="brand-subtitle">Професійний термінал</div>
                </div>
            </div>
            <hr style="border: 0; border-top: 1px solid #30363d; margin-bottom: 15px;">
            <div class="section-title">⚙️ Керування системою</div>
            <div id="conn-status" style="font-size: 13px; margin-bottom: 10px;">Статус: <span style="color:green;">● Онлайн</span></div>
            <button class="btn btn-start" onclick="toggleSystem(true)">▶ Запуск</button>
            <button class="btn btn-stop" onclick="toggleSystem(false)">⏸ Зупинка</button>
            
            <div class="section-title" style="margin-top: 25px;">🚨 Безпека</div>
            <button class="btn btn-kill" onclick="triggerKillSwitch()">KILL SWITCH</button>
        </sidebar>

        <main>
            <!-- Графік прогнозування зверху -->
            <div class="forecast-container">
                <h3 style="font-size: 15px; margin-bottom: 10px;">🔮 Глобальний графік прогнозування ринку (BitTherium AI)</h3>
                <div style="height: 250px;"><canvas id="forecastChart"></canvas></div>
            </div>

            <!-- Вкладки меню -->
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('home')">🏠 Головна</button>
                <button class="tab-btn" onclick="switchTab('analytics')">📈 Аналітика</button>
                <button class="tab-btn" onclick="switchTab('quotes')">💱 Котирування</button>
            </div>

            <div id="tab-home" class="tab-content">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Bitcoin (BTC/USDT)</div>
                        <div class="metric-value" id="btc-val">Завантаження...</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Ethereum (ETH/USDT)</div>
                        <div class="metric-value" id="eth-val">Завантаження...</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Solana (SOL/USDT)</div>
                        <div class="metric-value" id="sol-val">Завантаження...</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Статус ринку</div>
                        <div class="metric-value" style="color: #26a69a;">Бичачий</div>
                    </div>
                </div>
            </div>
        </main>

        <script>
            // Ініціалізація глобального графіка прогнозування
            const ctx = document.getElementById('forecastChart').getContext('2d');
            const forecastChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['-6год', '-5год', '-4год', '-3год', '-2год', '-1год', 'Зараз', '+1год (Прогноз)', '+2год', '+3год', '+4год', '+5год'],
                    datasets: [{
                        label: 'Реальні показники (Історія)',
                        data: [66200, 66500, 66400, 66900, 67200, 67100, 67450, null, null, null, null, null],
                        borderColor: '#26a69a',
                        borderWidth: 3,
                        tension: 0.2
                    }, {
                        label: 'AI Прогноз тренду',
                        data: [null, null, null, null, null, null, 67450, 67800, 68100, 68000, 68500, 69000],
                        borderColor: '#ffa726',
                        borderWidth: 3,
                        borderDash: [5, 5],
                        tension: 0.2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#fff' } } },
                    scales: {
                        x: { ticks: { color: '#8b949e' }, grid: { color: '#30363d' } },
                        y: { ticks: { color: '#8b949e' }, grid: { color: '#30363d' } }
                    }
                }
            });

            // Оновлення цін через API
            async function updatePrices() {
                try {
                    let res = await fetch('/api/prices');
                    let data = await res.json();
                    document.getElementById('btc-val').innerText = `$${data.BTC.toLocaleString()}`;
                    document.getElementById('eth-val').innerText = `$${data.ETH.toLocaleString()}`;
                    document.getElementById('sol-val').innerText = `$${data.SOL.toLocaleString()}`;
                } catch(e) { console.error(e); }
            }
            setInterval(updatePrices, 10000);
            updatePrices();

            function toggleSystem(status) {
                alert(status ? "Термінал запущено!" : "Термінал зупинено!");
            }
            function triggerKillSwitch() {
                alert("УВАГА: Активовано Kill Switch! Торгівлю призупинено.");
            }
            function switchTab(tab) {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                event.target.classList.add('active');
            }
        </script>
    </body>
    </html>
    """
    return html_content