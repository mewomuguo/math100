# 第 1 批: PWA 化 - 部署說明

這一批做完後,你的網頁就升級成 PWA (漸進式網頁應用程式),
- 可在手機/桌面「加入主畫面」變成 App
- 完全離線可用
- 是後續第 2 批 Capacitor 打包成 Android App 的基礎


## 檔案清單

```
math100-app/
├── index.html              主程式 (從 math100.html 改名)
├── manifest.json           PWA 設定 (App 名稱、圖示、主題色)
├── sw.js                   Service Worker (離線快取)
├── favicon.png             瀏覽器分頁圖示 (64x64)
├── icon-192.png            App 圖示 (192x192)
├── icon-512.png            App 圖示 (512x512)
├── icon-maskable-512.png   Adaptive icon (Android 用, 512x512)
└── make_icons.py           圖示產生器 (可以重跑換樣式)
```


## 步驟

### 1. 部署到 GitHub Pages (建議,免費)

PWA **必須走 HTTPS** 才能啟用 Service Worker。GitHub Pages 自帶 HTTPS。

```bash
# 在你的 GitHub 上建立新 repo: math100 (或任何名字)
git init
git add .
git commit -m "PWA v1"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/math100.git
git push -u origin main
```

然後在 repo Settings → Pages → Source 選 `main` branch / root,
等 1-2 分鐘後網址會是: `https://YOUR_NAME.github.io/math100/`


### 2. 驗證 PWA 是否正確

在電腦版 Chrome 打開部署網址,F12 開啟 DevTools:

- **Application → Manifest** → 應該看到 App 名稱、圖示
- **Application → Service Workers** → 應該看到 sw.js 已啟用 (status: activated)
- 網址列右邊會出現「安裝 App」icon (像個 + 號的螢幕)


### 3. 在手機上「裝」起來

開 Android Chrome 進入網址 →
選單 (右上 ⋮) → **加到主畫面** → 按裝
桌面就會出現「數學一百格」App 圖示, 點開全螢幕執行 (沒有網址列)。


### 4. 測試離線

- 進入 App → 開飛航模式 → 重新打開 App → 應該還能玩
- 第一次進入網頁時會自動快取所有檔案, 之後完全離線可用


## 已知限制

- **iOS Safari** 對 PWA 支援沒 Android 完整, 部分功能 (例如全螢幕)
  可能略有差異, 但核心遊戲功能 OK。
- 修改 index.html 後重新部署, **使用者要等 sw.js 自動更新** (重開 App 兩次或清快取)。如果改版很頻繁, 可以把 manifest.json 裡的 `"name"` 後面加版本號, 或調整 sw.js 裡的 `CACHE_NAME = 'math100-v2'`。


## 接下來

- 驗證 PWA 沒問題後 → 進入第 2 批: Capacitor 包成 Android App
- 上架前要準備的法務文件 → 第 3 批: 隱私權政策、Play Console 設定
