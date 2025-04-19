<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Инвестиционное приложение</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Подключаем Telegram WebApp скрипт -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <div id="app">
        <div id="content">
            <!-- Здесь будет основной контент страницы -->
            <div id="marketPage" class="page active">
                <h2>Рынок</h2>
                <div class="chart-container">
                    <canvas id="candleChart"></canvas>
                </div>
                <div class="stock-list">
                    <h3>Популярные акции</h3>
                    <div class="stock-item" onclick="showStockDetails('AAPL')">
                        <div class="stock-icon">AAPL</div>
                        <div class="stock-info">
                            <div class="stock-name">Apple Inc.</div>
                            <div class="stock-price">$173.45</div>
                        </div>
                        <div class="stock-change positive">+2.3%</div>
                    </div>
                    <div class="stock-item" onclick="showStockDetails('GOOGL')">
                        <div class="stock-icon">GOOGL</div>
                        <div class="stock-info">
                            <div class="stock-name">Alphabet Inc.</div>
                            <div class="stock-price">$133.82</div>
                        </div>
                        <div class="stock-change negative">-0.7%</div>
                    </div>
                    <div class="stock-item" onclick="showStockDetails('MSFT')">
                        <div class="stock-icon">MSFT</div>
                        <div class="stock-info">
                            <div class="stock-name">Microsoft Corp.</div>
                            <div class="stock-price">$344.29</div>
                        </div>
                        <div class="stock-change positive">+1.5%</div>
                    </div>
                    <div class="stock-item" onclick="showStockDetails('AMZN')">
                        <div class="stock-icon">AMZN</div>
                        <div class="stock-info">
                            <div class="stock-name">Amazon.com Inc.</div>
                            <div class="stock-price">$127.12</div>
                        </div>
                        <div class="stock-change positive">+0.6%</div>
                    </div>
                </div>
            </div>

            <div id="portfolioPage" class="page">
                <h2>Портфель</h2>
                <div class="portfolio-summary">
                    <div class="portfolio-value">
                        <h3>Общая стоимость</h3>
                        <div class="value">$10,245.67</div>
                        <div class="change positive">+$124.56 (+1.23%)</div>
                    </div>
                </div>

                <div class="portfolio-assets">
                    <h3>Ваши активы</h3>
                    <div class="asset-item">
                        <div class="asset-icon">AAPL</div>
                        <div class="asset-info">
                            <div class="asset-name">Apple Inc.</div>
                            <div class="asset-shares">3 акции</div>
                        </div>
                        <div class="asset-value">
                            <div class="value">$520.35</div>
                            <div class="change positive">+2.3%</div>
                        </div>
                    </div>
                    <div class="asset-item">
                        <div class="asset-icon">MSFT</div>
                        <div class="asset-info">
                            <div class="asset-name">Microsoft Corp.</div>
                            <div class="asset-shares">2 акции</div>
                        </div>
                        <div class="asset-value">
                            <div class="value">$688.58</div>
                            <div class="change positive">+1.5%</div>
                        </div>
                    </div>
                </div>

                <div class="portfolio-actions">
                    <button class="action-button">Купить</button>
                    <button class="action-button">Продать</button>
                </div>
            </div>
        </div>

        <!-- Нижняя навигационная панель -->
        <div class="nav-bar">
            <button id="marketBtn" class="nav-button active">
                <svg viewBox="0 0 24 24" class="nav-icon">
                    <path d="M1,9h3v10h-3v-10zm6-5h3v15h-3v-15zm6,7h3v8h-3v-8zm6-7h3v15h-3v-15z"/>
                </svg>
                <span>Рынок</span>
            </button>
            <button id="portfolioBtn" class="nav-button">
                <svg viewBox="0 0 24 24" class="nav-icon">
                    <path d="M21,6h-4V3c0-0.55-0.45-1-1-1H8C7.45,2,7,2.45,7,3v3H3C1.9,6,1,6.9,1,8v12c0,1.1,0.9,2,2,2h18c1.1,0,2-0.9,2-2V8C23,6.9,22.1,6,21,6z M9,4h6v2H9V4z M21,20H3V8h4h10h4V20z"/>
                </svg>
                <span>Портфель</span>
            </button>
        </div>
    </div>

    <!-- Подключаем Chart.js для графиков -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="app.js"></script>
</body>
</html>

:root {
    --tg-theme-bg-color: #ffffff;
    --tg-theme-text-color: #000000;
    --tg-theme-hint-color: #999999;
    --tg-theme-link-color: #2481cc;
    --tg-theme-button-color: #2481cc;
    --tg-theme-button-text-color: #ffffff;
    --tg-theme-secondary-bg-color: #f0f0f0;

    /* Дополнительные переменные для нашей темы */
    --nav-bg-color: rgba(240, 240, 240, 0.8);
    --nav-active-color: #2481cc;
    --nav-inactive-color: #999999;
    --border-color: #e0e0e0;
    --positive-color: #4caf50;
    --negative-color: #f44336;
}

/* Автоматически подстраиваемся под тему Telegram */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: var(--tg-theme-bg-color);
    color: var(--tg-theme-text-color);
    margin: 0;
    padding: 0;
    min-height: 100vh;
    font-size: 16px;
}

#app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

#content {
    flex-grow: 1;
    overflow-y: auto;
    padding: 16px;
    padding-bottom: 80px; /* добавляем отступ снизу для навигационной панели */
}

.page {
    display: none;
}

.page.active {
    display: block;
}

h2 {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 24px;
    font-weight: 600;
}

h3 {
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 12px;
}

/* Навигационная панель */
.nav-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-around;
    background-color: var(--nav-bg-color);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid var(--border-color);
    padding: 8px 16px;
    box-sizing: border-box;
    z-index: 100;
}

.nav-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 8px 16px;
    outline: none;
    color: var(--nav-inactive-color);
    cursor: pointer;
}

.nav-button.active {
    color: var(--nav-active-color);
}

.nav-icon {
    width: 24px;
    height: 24px;
    fill: currentColor;
    margin-bottom: 4px;
}

/* График */
.chart-container {
    height: 240px;
    margin-bottom: 16px;
    background-color: var(--tg-theme-secondary-bg-color);
    border-radius: 12px;
    overflow: hidden;
    padding: 16px;
}

/* Списки акций */
.stock-list, .portfolio-assets {
    margin-bottom: 24px;
}

.stock-item, .asset-item {
    display: flex;
    align-items: center;
    padding: 12px;
    margin-bottom: 8px;
    background-color: var(--tg-theme-secondary-bg-color);
    border-radius: 12px;
    cursor: pointer;
}

.stock-icon, .asset-icon {
    font-weight: bold;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: var(--tg-theme-button-color);
    color: var(--tg-theme-button-text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
}

.stock-info, .asset-info {
    flex-grow: 1;
}

.stock-name, .asset-name {
    font-weight: 500;
    margin-bottom: 4px;
}

.stock-price, .asset-shares {
    font-size: 14px;
    color: var(--tg-theme-hint-color);
}

.stock-change, .change {
    font-weight: 500;
}

.positive {
    color: var(--positive-color);
}

.negative {
    color: var(--negative-color);
}

/* Портфель */
.portfolio-summary {
    background-color: var(--tg-theme-secondary-bg-color);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
}

.portfolio-value .value {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 4px;
}

.portfolio-actions {
    display: flex;
    justify-content: space-around;
}

.action-button {
    background-color: var(--tg-theme-button-color);
    color: var(--tg-theme-button-text-color);
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
}

@media (prefers-color-scheme: dark) {
    :root {
        --t
