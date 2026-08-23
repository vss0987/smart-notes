const TOKEN_URL = "/api/token/";
const REFRESH_URL = "/api/token/refresh/";
const REGISTER_URL = "/api/users/register/";
const SUMMARIZE_URL = "/api/ai/summarize/";
const HISTORY_URL = "/api/ai/history/";

const loginPanel = document.getElementById("loginPanel");
const registerPanel = document.getElementById("registerPanel");
const workspaceView = document.getElementById("workspaceView");
const historyView = document.getElementById("historyView");
const logoutBtn = document.getElementById("logoutBtn");
const historyBtn = document.getElementById("historyBtn");

const loginBtn = document.getElementById("loginBtn");
const loginError = document.getElementById("loginError");
const loginEmailEl = document.getElementById("loginEmail");
const loginPasswordEl = document.getElementById("loginPassword");

const registerBtn = document.getElementById("registerBtn");
const registerError = document.getElementById("registerError");
const registerEmailEl = document.getElementById("registerEmail");
const registerPasswordEl = document.getElementById("registerPassword");

const textEl = document.getElementById("text");
const charCountEl = document.getElementById("charCount");
const statusEl = document.getElementById("status");
const resultPanel = document.getElementById("resultPanel");
const resultContent = document.getElementById("result-content");
const summarizeBtn = document.getElementById("summarizeBtn");
const historyList = document.getElementById("historyList");
const historyEmpty = document.getElementById("historyEmpty");

const PLACEHOLDER_TEXT = "Здесь появится результат";

function setStatus(text) {
    statusEl.textContent = `status: ${text}`;
}

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}

function setTokens({ access, refresh }) {
    if (access) localStorage.setItem("access_token", access);
    if (refresh) localStorage.setItem("refresh_token", refresh);
}

function clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

/* --- Переключение экранов --- */

function showApp() {
    loginPanel.hidden = true;
    registerPanel.hidden = true;
    logoutBtn.hidden = false;
    historyBtn.hidden = false;
    showWorkspace();
}

function showLoginForm() {
    loginPanel.hidden = false;
    registerPanel.hidden = true;
    workspaceView.hidden = true;
    historyView.hidden = true;
    logoutBtn.hidden = true;
    historyBtn.hidden = true;
}

function showRegisterForm() {
    loginPanel.hidden = true;
    registerPanel.hidden = false;
    workspaceView.hidden = true;
    historyView.hidden = true;
    logoutBtn.hidden = true;
    historyBtn.hidden = true;
}

function showWorkspace() {
    workspaceView.hidden = false;
    historyView.hidden = true;
    historyBtn.textContent = "История";
    historyBtn.classList.remove("is-active");
    setStatus("ожидание");
}

function showHistoryView() {
    workspaceView.hidden = true;
    historyView.hidden = false;
    historyBtn.textContent = "Назад";
    historyBtn.classList.add("is-active");
    loadHistory();
}

function toggleHistoryView() {
    if (historyView.hidden) {
        showHistoryView();
    } else {
        showWorkspace();
    }
}

/**
 * Пытается получить новый access-токен через refresh.
 * Возвращает true, если удалось — иначе разлогинивает.
 */
async function tryRefreshToken() {
    const refresh = getRefreshToken();
    if (!refresh) return false;

    try {
        const response = await fetch(REFRESH_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });

        if (!response.ok) return false;

        const data = await response.json();
        setTokens({ access: data.access, refresh: data.refresh });
        return true;

    } catch (err) {
        return false;
    }
}

/**
 * fetch с автоматической подстановкой токена и одной попыткой
 * обновить его через refresh, если сервер ответил 401.
 */
async function authFetch(url, options = {}) {
    const makeRequest = () => fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            "Authorization": `Bearer ${getAccessToken()}`,
        },
    });

    let response = await makeRequest();

    if (response.status === 401) {
        const refreshed = await tryRefreshToken();
        if (refreshed) {
            response = await makeRequest();
        } else {
            clearTokens();
            showLoginForm();
            throw new Error("Сессия истекла, войдите снова");
        }
    }

    return response;
}

async function authenticateAndEnter(email, password) {
    const response = await fetch(TOKEN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        throw new Error("Неверный email или пароль");
    }

    const data = await response.json();
    setTokens({ access: data.access, refresh: data.refresh });
    showApp();
}

async function login() {
    const email = loginEmailEl.value.trim();
    const password = loginPasswordEl.value;

    loginError.hidden = true;
    loginBtn.disabled = true;

    if (!email || !password) {
        loginError.textContent = "Введите email и пароль";
        loginError.hidden = false;
        loginBtn.disabled = false;
        return;
    }

    try {
        await authenticateAndEnter(email, password);
        loginPasswordEl.value = "";
    } catch (err) {
        loginError.textContent = err.message || "Не удалось подключиться к серверу";
        loginError.hidden = false;
    } finally {
        loginBtn.disabled = false;
    }
}

async function register() {
    const email = registerEmailEl.value.trim();
    const password = registerPasswordEl.value;

    registerError.hidden = true;
    registerBtn.disabled = true;

    if (!email || !password) {
        registerError.textContent = "Введите email и пароль";
        registerError.hidden = false;
        registerBtn.disabled = false;
        return;
    }

    try {
        const response = await fetch(REGISTER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            const firstError = Object.values(data)[0];
            registerError.textContent = Array.isArray(firstError)
                ? firstError[0]
                : "Не удалось зарегистрироваться. Проверьте email и пароль.";
            registerError.hidden = false;
            return;
        }

        // После успешной регистрации сразу входим тем же email/паролем —
        // пользователю не нужно вводить их повторно на другой форме.
        await authenticateAndEnter(email, password);
        registerPasswordEl.value = "";

    } catch (err) {
        registerError.textContent = "Не удалось подключиться к серверу";
        registerError.hidden = false;
    } finally {
        registerBtn.disabled = false;
    }
}

function logout() {
    clearTokens();
    showLoginForm();
}

function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function renderHistoryItem(entry) {
    const item = document.createElement("div");
    item.className = "history-item";
    item.innerHTML = `
        <div class="history-item-date">${formatDate(entry.created_at)}</div>
        <div class="history-block">
            <span class="history-block-label">Исходный текст</span>
            <div class="history-item-input is-clamped">${entry.input_text}</div>
            <button type="button" class="history-toggle" hidden>Показать полностью</button>
        </div>
        <div class="history-block history-block-result">
            <span class="history-block-label">Результат</span>
            <div class="history-item-summary">${entry.summary}</div>
        </div>
    `;

    const inputEl = item.querySelector(".history-item-input");
    const toggleBtn = item.querySelector(".history-toggle");

    // Кнопку показываем, только если текст реально обрезан
    // (иначе она будет висеть даже у коротких сообщений в два слова).
    requestAnimationFrame(() => {
        if (inputEl.scrollHeight > inputEl.clientHeight + 1) {
            toggleBtn.hidden = false;
        }
    });

    toggleBtn.addEventListener("click", () => {
        const isClamped = inputEl.classList.toggle("is-clamped");
        toggleBtn.textContent = isClamped ? "Показать полностью" : "Свернуть";
    });

    return item;
}

async function loadHistory() {
    try {
        const response = await authFetch(HISTORY_URL);
        if (!response.ok) return;

        const items = await response.json();

        historyList.querySelectorAll(".history-item").forEach(el => el.remove());

        if (items.length === 0) {
            historyEmpty.hidden = false;
            return;
        }

        historyEmpty.hidden = true;
        items.forEach(entry => historyList.appendChild(renderHistoryItem(entry)));

    } catch (err) {
        // Тихо игнорируем — история не критична для основного сценария
    }
}

textEl.addEventListener("input", () => {
    charCountEl.textContent = `${textEl.value.length} симв.`;
});

logoutBtn.addEventListener("click", logout);
historyBtn.addEventListener("click", toggleHistoryView);

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

/**
 * Обычная замена текста без анимации — для плейсхолдера,
 * статуса "Обрабатывается…" и сообщений об ошибке.
 */
function setPlainResult(text, isPlaceholder) {
    resultContent.textContent = text;
    resultContent.classList.toggle("is-placeholder", Boolean(isPlaceholder));
}

/**
 * Показывает финальный результат так, будто слова проступают
 * из размытия одно за другим. Задержка растёт со словом, но
 * не бесконечно — после 40-го слова все стартуют одновременно,
 * иначе длинная суммаризация "проявлялась" бы по полминуты.
 */
function revealResult(text) {
    resultContent.classList.remove("is-placeholder");
    resultContent.innerHTML = text
        .split(/(\s+)/)
        .map((token, index) => {
            if (/^\s*$/.test(token)) return token;
            const delay = Math.min(index, 40) * 18;
            return `<span class="reveal-word" style="animation-delay: ${delay}ms">${escapeHtml(token)}</span>`;
        })
        .join("");
}

async function summarize() {
    const text = textEl.value.trim();

    if (!text) {
        setStatus("введите текст");
        return;
    }

    resultPanel.classList.remove("is-error");
    setPlainResult("Обрабатывается…", true);
    summarizeBtn.disabled = true;
    setStatus("обработка");

    try {
        const response = await authFetch(SUMMARIZE_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const data = await response.json();
        revealResult(data || "Пустой ответ от сервера");
        setStatus("готово");

    } catch (err) {
        resultPanel.classList.add("is-error");
        setPlainResult(err.message || "Не удалось получить ответ. Попробуйте позже.", false);
        setStatus("ошибка");
    } finally {
        summarizeBtn.disabled = false;
    }
}

// При загрузке страницы — сразу показать нужную панель
if (getAccessToken()) {
    showApp();
} else {
    showLoginForm();
}
