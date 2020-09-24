# 104人力銀行--使用關鍵字搜尋職缺爬取職務資訊
 
# 程式執行:
   1. 讀取設定檔 104job.conf
   2. 讀取設定檔 keyword、city、updatetime 內容
   3. city 帶入get_city_code函數取得地區編號 city_code
   4. 執行 get_pageNumber(keyword, city_code) 取得所搜尋職缺總頁數
   5. 執行 get_page 函數，爬取每筆職缺資料，存入資料庫
   
# 存取方式:
   1. 使用 sqlite3 資料庫
   2. 資料庫存取: 以 job_id 欄位判定某筆資料是否存在，如存在(if info)就更新這筆資料，\
      如不存在(else) 就新增資料。
