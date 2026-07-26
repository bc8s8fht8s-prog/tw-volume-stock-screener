const pageSize = 50;

let data = {};
let currentPage = 1;

// 所有股票
let allStocks = [];

// 搜尋後股票
let filteredStocks = [];

// 排序方式
let sortMode = "code";

// 成交量倍數篩選（預設 1.5 倍）
let volumeFilter = 1.5;

function sortStocks() {

    if (sortMode === "code") {

        filteredStocks.sort((a, b) =>
            Number(a.code) - Number(b.code)
        );

    } else if (sortMode === "change") {

        filteredStocks.sort((a, b) =>
            Number(b.change_percent || 0) -
            Number(a.change_percent || 0)
        );

    }

}

function applyFilters() {

    const keyword = document
        .getElementById("search")
        .value
        .trim()
        .toLowerCase();

    filteredStocks = allStocks.filter(stock => {

        const matchKeyword =
            keyword === "" ||
            String(stock.code).toLowerCase().includes(keyword) ||
            String(stock.name).toLowerCase().includes(keyword);

        const ratio =
            Number(stock.volume_ratio || 0);

        const matchVolume =
            ratio >= volumeFilter;

        return matchKeyword && matchVolume;

    });

    sortStocks();

    // 更新符合條件檔數
    document.getElementById("count").textContent =
        filteredStocks.length + " 檔";

    renderPage(1);

}

function changeVolumeFilter() {

    volumeFilter = Number(
        document.getElementById("volumeFilter").value
    );

    applyFilters();

}

async function loadData() {

    const response = await fetch("data/result.json");

    data = await response.json();

    allStocks = data.stocks;

    document.getElementById("update_time").textContent = data.update_time;
    document.getElementById("scan_count").textContent = data.scan_count;

    applyFilters();

}

function renderPage(page) {

    currentPage = page;

    const stockList = document.getElementById("stock-list");

    stockList.innerHTML = "";

    const start = (page - 1) * pageSize;
    const end = start + pageSize;

    const stocks = filteredStocks.slice(start, end);

    if (stocks.length === 0) {

        stockList.innerHTML = `
            <div class="no-result">
                🔍 找不到符合條件的股票
            </div>
        `;

        document.getElementById("pagination").innerHTML = "";

        return;

    }

    stocks.forEach(stock => {

        const close = Number(stock.close).toFixed(2);
        const high = Number(stock.high).toFixed(2);

        const change =
            stock.change_percent != null
                ? Number(stock.change_percent).toFixed(2)
                : "--";

        const osc =
            stock.osc != null
                ? Number(stock.osc).toFixed(3)
                : "--";

        const oscClass =
            stock.osc >= 0 ? "osc-up" : "osc-down";

        const volumeRatio =
            stock.volume_ratio != null
                ? Number(stock.volume_ratio).toFixed(2)
                : "--";

        stockList.innerHTML += `

            <div class="stock-card">

                <h3>${stock.code} ${stock.name}</h3>

                <p>
                    本日收盤：
                    <strong>${close}</strong>
                </p>

                <p>
                    昨日最高：
                    <strong>${high}</strong>
                </p>

                <p>
                    本日漲幅：
                    <span class="change-up">${change}%</span>
                </p>

                <p>
                    OSC：
                    <span class="${oscClass}">
                        ${osc}
                    </span>
                </p>

                <p>
                    📈 量比：
                    <strong>${volumeRatio} 倍</strong>
                </p>

            </div>

        `;

    });

    renderPagination();

}

function renderPagination() {

    const totalPages = Math.ceil(filteredStocks.length / pageSize);

    let html = "";

    if (currentPage > 1) {

        html += `
            <button class="page-btn"
                onclick="renderPage(${currentPage - 1})">
                ◀
            </button>
        `;

    }

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    if (currentPage <= 3) {
        endPage = Math.min(5, totalPages);
    }

    if (currentPage >= totalPages - 2) {
        startPage = Math.max(1, totalPages - 4);
    }

    for (let i = startPage; i <= endPage; i++) {

        if (i === currentPage) {

            html += `
                <button class="page-btn active">
                    ${i}
                </button>
            `;

        } else {

            html += `
                <button
                    class="page-btn"
                    onclick="renderPage(${i})">
                    ${i}
                </button>
            `;

        }

    }

    if (currentPage < totalPages) {

        html += `
            <button class="page-btn"
                onclick="renderPage(${currentPage + 1})">
                ▶
            </button>
        `;

    }

    document.getElementById("pagination").innerHTML = `
        <div class="pagination">
            ${html}
        </div>
    `;

}

function searchStocks() {

    applyFilters();

}

function changeSort() {

    sortMode =
        document.getElementById("sortSelect").value;

    applyFilters();

}

loadData();