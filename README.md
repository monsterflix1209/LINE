# LINE Rich Menu 分頁工具

這個專案用 GitHub Actions 建立 LINE Rich Menu，之後可延伸成 A ⇄ B ⇄ C 分頁。

## 使用方式

1. 到 GitHub Repository → Settings → Secrets and variables → Actions。
2. 建立 Repository secret：`LINE_CHANNEL_ACCESS_TOKEN`
3. Secret 的值貼上你的 LINE Channel Access Token（不要寫進程式碼）。
4. 到 Actions → `Create LINE Rich Menu A` → `Run workflow`。
5. Workflow 成功後會在日誌中顯示 `richMenuId`。

第一版先建立 Rich Menu A；下一步再加入圖片上傳與 `richmenuswitch` 分頁。
