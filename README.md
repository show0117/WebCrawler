## WebCrawler
#### 該專案包含雲端使用版(WebCrawler_remote)與地端測試版(WebCrawler_local)，雲端使用版提供使用者每日或每周自動化的爬取標案網站，而地端測試版用來進行除錯測試或者手動指定想要爬取更新的資料日期區間。

### 雲端使用版使用步驟
#### 步驟一、開啟一個新的AWS EC2執行個體(限定Windows作業系統)
<img width="515" alt="1" src="https://user-images.githubusercontent.com/62537043/127834154-be40ba4b-0e37-41a1-a088-ab1049318c46.png">
#### 步驟二、從該EC2的遠端伺服器中下載本WebCrawler_remote資料夾並放在任意位置
![image](https://user-images.githubusercontent.com/62537043/127833755-dd57f166-b60f-44a8-92cf-035d2505876e.png)
#### 步驟三、設定工作排程器

#### 步驟四、為Lambda函數創建IAM中Polic（政策)和Roles（角色)
#### 步驟五、創建Lambda函數，執行停止和啟動EC2實例
#### 步驟六、建立CloudWatch Events規則，並觸發Lambda函數

### 地端測試版使用步驟
#### 步驟一、下載本WebCrawler_local資料夾並放在自己電腦的任意位置
#### 步驟二、執行run_webcrawler.py檔案並輸入起始日期


