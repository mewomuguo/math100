// 數學一百格 Service Worker
// 策略: cache-first, 確保離線可用

const CACHE_NAME = 'math100-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.png',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

// 安裝: 預先快取所有資源
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// 啟用: 清掉舊版本快取
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// 抓取: cache-first, 找不到才走網路
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) return cached;
      return fetch(e.request).then((res) => {
        // 順便存進快取 (僅成功的同源回應)
        if (res && res.status === 200 && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
        }
        return res;
      }).catch(() => {
        // 完全離線時, 任何網頁要求都回傳首頁
        if (e.request.mode === 'navigate') return caches.match('./index.html');
      });
    })
  );
});
