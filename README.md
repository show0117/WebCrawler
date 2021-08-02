## WebCrawler
#### 該專案包含雲端使用版(WebCrawler_remote)與地端測試版(WebCrawler_local)，雲端使用版提供使用者每日或每周自動化的爬取標案網站，而地端測試版用來進行除錯測試或者手動指定想要爬取更新的資料日期區間。

### 雲端使用版使用步驟
#### 步驟一、開啟一個新的AWS EC2執行個體(限定Windows作業系統)
<img width="515" alt="1" src="https://user-images.githubusercontent.com/62537043/127834154-be40ba4b-0e37-41a1-a088-ab1049318c46.png">

#### 步驟二、從該EC2的遠端伺服器中下載本WebCrawler_remote資料夾並放在任意位置
<img width="959" alt="2" src="https://user-images.githubusercontent.com/62537043/127840747-fff5e6b5-ed5f-4d26-a6eb-71ac67c3ffb0.png">

#### 步驟三、設定工作排程器每周或每日執行WebCrawler_remote中的open.bat檔案
<img width="453" alt="4" src="https://user-images.githubusercontent.com/62537043/127840817-83cb15a7-f30c-49b5-9472-3e033f9cf303.png">

#### 步驟四、利用AWS的IAM服務創建一個新的Policy（政策)
新增一個新的Policy並且在JSON欄位輸入以下程式碼
<img width="461" alt="5" src="https://user-images.githubusercontent.com/62537043/127840861-6fc91049-3ecd-42ba-b738-0f805a75c290.png">
建立Policy
<img width="457" alt="6" src="https://user-images.githubusercontent.com/62537043/127841139-305efcb8-3afb-4c3c-a696-943061be2a27.png">

#### 步驟五、利用AWS的IAM服務創建一個新的Role（角色)
選擇建立新的Role
<img width="424" alt="7" src="https://user-images.githubusercontent.com/62537043/127841236-ba4efa66-97fd-4936-9ea7-4f8bc40c3a70.png">
選擇剛剛建立的新的Policy
<img width="420" alt="8" src="https://user-images.githubusercontent.com/62537043/127841323-92ff1d9d-28d5-42c0-a7a9-28ac61f79564.png">
建立Role
<img width="423" alt="9" src="https://user-images.githubusercontent.com/62537043/127841377-f5226739-6f03-47ac-9367-9938966b6465.png">

#### 步驟六、創建Lambda函數，執行停止和啟動EC2實例
#### 步驟七、建立CloudWatch Events規則，並觸發Lambda函數

### 地端測試版使用步驟
#### 步驟一、下載本WebCrawler_local資料夾並放在自己電腦的任意位置
#### 步驟二、Windows作業系統可以點擊open.bat檔啟動爬蟲程式，其他系統則須直接執行run_crawler.py檔案


