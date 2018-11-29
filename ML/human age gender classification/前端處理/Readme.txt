將 haarcascade.xml 跟 .py放在同一個資料夾下
改變 filepath 的路徑，指向檔案所在的資料夾

For final.py:
	若想要輸出有 sobel filter 較凸顯邊緣的圖片，則將 sobelFilter()那行的# 刪掉
	改變輸出圖片大小則將resize(,(x,y)) 中的x y大小改掉
	圖片就會在.py檔下的資料夾產生。

For dataAugmentation.py:
	在dataAugmentation 的 function 裡面，
	改變迴圈條件中 save_to_dir="資料夾名"
	改變增加大小則改變迴圈中 if > 數量：
	
