How to use it?

After Unzipping the file, puting all the target pictures under folder "testing."
Running testing.py to get it's prediction in target.csv

If you wish to reorganize the target pictures, use face_detect.py and assign input path and output path.
It will detect face areas and make the pictures into 28*28 pixed size.

Finally, assing target path, such as "adult/male/*.jpg," in cnn_v1.py, which will find the optimize parameters and save the model under the folder "./model," and then you are be able to run testing.py for predicting. 
