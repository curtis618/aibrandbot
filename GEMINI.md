# aibrandbot

## 專案簡介

aibrandbot 是一個為品牌（例如：觀光園區）設計的 LINE Bot 整合行銷解決方案。它透過 LINE Liff 技術和 AI 圖像合成，提供互動式的網頁任務，讓使用者在參與行銷活動的同時，獲得獨一無二的個人化紀念照片，藉此提升品牌參與感與社群擴散效益。

## 使用者流程

1.  **加入好友與登入**：使用者將品牌的 LINE 官方帳號加為好友，並完成初次登入。
2.  **接收行銷活動**：使用者會收到品牌推播的行銷活動，例如尋寶遊戲、定點打卡等。
3.  **執行網頁任務**：點擊活動訊息後，透過 LINE Liff 開啟網頁應用。使用者根據任務指示（例如：在園區特定地點），拍攝照片。
4.  **AI 圖像合成**：系統會將使用者剛拍攝的照片與其預先上傳的個人照片進行 AI 合成，創造出獨特的紀念照。
5.  **接收合成照片**：完成後，系統會透過 LINE Bot 將合成好的照片回傳給使用者。

## 核心功能

*   **LINE Bot 互動**：作為使用者與品牌互動的主要入口，發布活動並回傳最終成果。
*   **LINE Liff 網頁任務**：提供豐富的互動介面，引導使用者完成拍照等行銷任務。
*   **AI 圖像合成**：將使用者提供的兩張照片（個人照與場景照）進行智慧合成，是本專案的核心技術亮點。
*   **AI 創意生圖**：整合 Google Gemini 3 Pro Image Preview 模型，讓使用者能透過文字描述生成高品質 AI 圖片。
*   **個人化行銷**：為每位參與者創造獨一無二的紀念品，提升活動吸引力與個人化體驗。
*   **智慧客服助手**：整合 Google Gemini AI，提供 24/7 的自然語言問答服務，能自動查詢活動資訊、介紹工作室，並以圖文並茂的 Flex Message 回覆。

## 技術架構 (Technical Architecture)

*   **後端框架**：Python Django 4.2
*   **AI 模型**：
    *   **對話與邏輯**：Google Gemini Pro (gemini-2.5-flash) - 負責 NLU、意圖識別、Function Calling。
    *   **圖像生成**：Google Gemini 3 Pro Image Preview (gemini-2.0-flash-exp) - 負責 AI 生圖。
*   **訊息平台**：LINE Messaging API
    *   功能：Webhook, Reply Message, Loading Animation, Flex Message (Bubble, Carousel), LIFF
*   **資料庫**：SQLite (開發階段) / 可遷移至 PostgreSQL
*   **部署平台**：支援 Vercel (Serverless) 與 Render
*   **套件管理**：
    *   `django`: Web 框架
    *   `google-genai`: 新版 Gemini SDK (用於生圖)
    *   `google-generativeai`: 舊版 Gemini SDK (用於對話)
    *   `requests`: HTTP 請求處理
    *   `python-dotenv`: 環境變數管理

