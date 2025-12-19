# aibrandbot

## 專案簡介 (Project Introduction)

aibrandbot 是一個創新的整合行銷解決方案，旨在運用 LINE Bot、LINE Front-end Framework (LIFF) 網頁應用與人工智慧圖像合成技術，協助品牌（例如：觀光園區）進行互動式推廣。此專案目標是提供一套流程，讓使用者能透過參與品牌活動、完成拍照任務，並獲得個人化 AI 合成照片作為紀念，進而提升品牌參與度與社群分享效益。

## 功能概述 (Feature Overview)

*   **LINE Bot 互動介面**：作為使用者與品牌活動的主要互動渠道，負責活動發布、任務指引及最終成果（AI 合成照片）的回傳。
*   **LINE LIFF 網頁應用**：提供高度客製化的前端介面，支援使用者在 LINE 環境中直接進行拍照、上傳等互動式任務。
*   **AI 圖像合成引擎**：專案核心技術，能夠將使用者拍攝的場景照片與其個人照片進行智慧融合，生成獨特的創意合成照片。
*   **個人化使用者體驗**：透過生成專屬紀念照片，大幅提升使用者參與活動的樂趣和記憶點，鼓勵使用者分享，達成病毒式行銷效果。

## 目前實作功能 (Current Implementation)

本專案目前已完成以下核心模組開發：

### 1. 智慧對話機器人 (AI Chatbot)
*   **整合 Google Gemini Pro**：使用最新的 Gemini 生成式 AI 模型，賦予機器人理解自然語言的能力。
*   **Function Calling (工具呼叫)**：實作 AI 自動判斷並呼叫後端函式的功能。例如：當使用者詢問「最近有什麼活動」時，AI 會自動查詢資料庫並回傳結果，而非僅生成文字。

### 2. LINE Messaging API 整合
*   **Webhook 處理**：完整的簽章驗證 (Signature Verification) 與訊息接收流程。
*   **Flex Message 支援**：
    *   **活動卡片 (Activity Card)**：查詢單一活動時，回傳包含圖片、日期、地點的精美卡片。
    *   **輪播訊息 (Carousel)**：查詢多個活動時，以左右滑動的卡片列表呈現。
    *   **影片預覽**：支援以圖片連結開啟影片的互動模式。
*   **載入動畫 (Loading Animation)**：在 AI 思考運算期間，自動顯示 LINE 的載入中動畫，優化使用者體驗。

### 3. 後端管理系統 (Backend Management)
*   **Django Framework**：使用穩定且強大的 Python Web 框架。
*   **資料庫管理**：
    *   設計 `Activity` 模型儲存活動資訊 (名稱、日期、地點、圖片等)。
    *   整合 Django Admin 後台，方便管理員新增、修改或刪除活動資料。
*   **環境變數管理**：使用 `.env` 檔案安全管理 API Key 與 Secret。

## 安裝與執行 (Installation)

1.  安裝相依套件：
    ```bash
    pip install -r requirements.txt
    ```

2.  設定環境變數 (`.env`)：
    ```env
    LINE_CHANNEL_ACCESS_TOKEN=your_token
    LINE_CHANNEL_SECRET=your_secret
    GEMINI_API_KEY=your_gemini_key
    ```

3.  初始化資料庫：
    ```bash
    python manage.py migrate
    ```

4.  啟動伺服器：
    ```bash
    python manage.py runserver
    ```

