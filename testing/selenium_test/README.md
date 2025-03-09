# 寫測試
1. 一人寫五個(5*4=20 除了 HAYU 負責環境建置)，先搶先贏
2. 寫之前先去 [文件](https://docs.google.com/document/d/1BQbdZ0Hl2nKw4Se_ETXLVtGOhzc81aNe50NYg_2iZWU/edit?tab=t.0) 寫表格，避免寫到同個測試
3. 開自己的 branch
3. 每個測試開一個檔案
4. 寫一個 function，成功回傳 true，失敗回傳 false
5. 去 main.py 裡面加上指令執行你的測試
6. 確認 github action 你的測試跑成功
7. 發 pull request 並回去 main branch

# 修 Bug
1. 發 issue 詳細敘述
1. 要修的人開個 branch
1. 自己或找人修網頁的 Bug ，也寫過程到該 issue
2. 發 pull request 合併回去 main branch
1. 關閉 issue

P.S. 本機測試的時候用 ubuntu 可能跑不起來，我是用 miniconda 在 Windows 跑，如果需要在 ubuntu 跑再說

# 優先做的 (剩下的可以自己想，例如 failed test 之類的)
- [X] 順利載入首頁
- [X] 按下註冊按鈕有出現註冊畫面
- [X] 按下登入按鈕有出現登入畫面
- [X] 可以正常註冊
- [X] 註冊後可以正常登入
- [X] 註冊後登入後可以正常登出
- [ ] 登入後首頁歡迎回來有顯示使用者名字
- [ ] 可以創造短網址
- [ ] 短網址可以正常轉址
- [ ] 登入後的首頁下方有紀錄表格
- [ ] 紀錄表格的刪除有正常運作
- [ ] other 自己加

