io.imread("檔名")
io.imsave("檔名"內容)

若要降噪，則將 main() 裡的 reduceNoise() 那行的 comment 弄掉

若要做亮度均衡，
    則將 main() 裡的 HistogramEqualization() 那行的 comment 弄掉
	並可以隨意調整第二個參數的值，其為對cdf的次方調整

若要增加高頻訊號，則將sharpening()的comment弄掉

若要調整飽和度，則將 saturation()的comment弄掉，
    並調整第二個參數內容，其意義為對全部飽和度做scaling

