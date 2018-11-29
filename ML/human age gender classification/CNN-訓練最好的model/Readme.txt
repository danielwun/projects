將程式解壓縮完 將所要預測的圖片覆蓋到testing資料夾底下
運行 testing.py即可輸出其預測並存檔至target.csv

重新架構模型請使用face_detect.py指定檔案路徑與存檔路徑
會將圖片抓出臉之後縮放到28*28的大小

在使用cnn_v1.py裡面指定圖檔路徑 預設如adult/male/*.jpg
會自動找出最佳值並將模型存檔 存檔路徑預設跟目錄底下
將模型覆蓋至./model底下 在使用testing.py預測即可