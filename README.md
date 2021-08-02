## WebCrawler
#### 該專案包含雲端使用版(WebCrawler_remote)與地端測試版(WebCrawler_local)，雲端使用版提供使用者每日或每周自動化的爬取標案網站，而地端測試版用來進行除錯測試或者手動指定想要爬取更新的資料日期區間。

### 雲端使用版使用步驟
#### 步驟一、開啟一個新的AWS EC2執行個體(限定Windows作業系統)
<img width="515" alt="1" src="https://user-images.githubusercontent.com/62537043/127834154-be40ba4b-0e37-41a1-a088-ab1049318c46.png">

#### 步驟二、設定新環境

1. 下載Python

2. 從該EC2的遠端伺服器中下載本WebCrawler_remote資料夾並放在任意位置

<img width="959" alt="2" src="https://user-images.githubusercontent.com/62537043/127840747-fff5e6b5-ed5f-4d26-a6eb-71ac67c3ffb0.png">

3. 用CMD.exe命令行窗口輸入 chcp 65001 解決中文無法顯示的問題

#### 步驟三、設定工作排程器每周或每日的某個固定時間執行WebCrawler_remote中的open.bat檔案，並且設定執行權限

先設定每周或每日固定重啟的時間

<img width="453" alt="4" src="https://user-images.githubusercontent.com/62537043/127840817-83cb15a7-f30c-49b5-9472-3e033f9cf303.png">

從工作排程器程式庫中選擇剛剛建立的排程，右鍵點選內容，然後將執行權限設定為「不弄使用者是否登入均執行」並且以最高權限執行

<img width="471" alt="19" src="https://user-images.githubusercontent.com/62537043/127849584-15cd40fa-83e8-42f8-8fb2-56194f499785.png">

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

#### 步驟六、創建用來啟動與停止EC2的Lambda函數

首先我們先建立能夠啟動EC2的函式。開啟Lambda主控台並創建新的Function(函式)，選擇從頭開始撰寫、輸入函式名稱、選擇語言、以及選取剛剛新建的Role，然後按下建立函式

<img width="867" alt="12" src="https://user-images.githubusercontent.com/62537043/127843721-bda8d6f5-3f69-4869-8382-42935452cf65.png">

<img width="868" alt="11" src="https://user-images.githubusercontent.com/62537043/127843748-e83e4596-bacb-4597-aa2c-0b82fd722de0.png">

在該函式的Lambda Function中輸入下列程式碼便完成了啟動EC2的函式的創建。

<img width="416" alt="13" src="https://user-images.githubusercontent.com/62537043/127844757-92b5aa2a-04f8-4a70-94be-fa73d87c4806.png">

而停止EC2的Lambda函數也同樣如法炮製，並且在Lambda Function中輸入下列程式碼:

<img width="842" alt="14" src="https://user-images.githubusercontent.com/62537043/127845084-ad4fdae4-6102-4838-bb45-86751854c784.png">

最後，利用測試功能測試函式能否正常運作，若測試結果出現成功便大功告成。

<img width="855" alt="16" src="https://user-images.githubusercontent.com/62537043/127846733-09efab6b-dd6e-40f9-ba18-97ac4c93eb37.png">

#### 步驟七、利用CloudWatch的Events功能管理Lambda函數的啟動時間
選擇Events然後建立新規則，用Cron表達式設定想要停止與啟動EC2的時間，建議關閉與啟動間隔設定半小時以上。此外，該時段不可以涵蓋爬蟲程式正在執行的時段，因此最好是把重啟的時間設定為距離啟動爬蟲程式的時間間隔愈遠愈好。

<img width="378" alt="18" src="https://user-images.githubusercontent.com/62537043/127848580-29423026-a5c6-4fbf-ab44-7a9bd5ca69d0.png">

全部都設定完成之後，該EC2便會每天固定重新啟動取得新的公有IP，並且在上面運行爬蟲程式。

### 地端測試版使用步驟
#### 步驟一、下載本WebCrawler_local資料夾並放在自己電腦的任意位置
#### 步驟二、Windows作業系統可以點擊open.bat檔啟動爬蟲程式，其他系統則須直接執行run_crawler.py檔案


