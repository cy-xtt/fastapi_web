import glob
import os

from keras_preprocessing.image import ImageDataGenerator
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
import numpy as np
from keras import losses,models,layers,metrics,optimizers
import matplotlib.pyplot as plt
from skimage import io,transform
from sklearn.model_selection import train_test_split

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
# 数据预处理
# 对训练集进行处理
# I:\阿里天池\facial age_datasets\face_age\*
total_face_img = []
total_label = []
for dir_path in glob.glob(r"G:\面部年龄\facial age_datasets\face_age\face_age\*"):
    img_label = dir_path.split('/')[-1]
    label = dir_path[-3:]
    for img_path in glob.glob(os.path.join(dir_path, "*.png")):
        total_face_img.append(img_path)
        total_label.append(label)


total_image_img_list = []
for i in total_face_img:
    img = io.imread(i)
    img = transform.resize(img, (100, 100))
    img = img/255.0
    img = img.astype('float16')
    total_image_img_list.append(img)

total_face_img = np.hstack(total_face_img)
total_label = np.hstack(total_label)
temp = np.array([total_face_img, total_label])
temp = temp.transpose()
np.random.shuffle(temp)
total_face_img = list(temp[:, 0])
total_label = list(temp[:, 1])

print(total_label)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(total_label)
y = to_categorical(y,50)
#y = np.array(total_label)
x = np.array(total_image_img_list)
#print(y)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.15,shuffle=True,random_state=0)

# # 数据增强器
# augs_gen = ImageDataGenerator(
#  featurewise_center=False,
#  samplewise_center=False,
#  featurewise_std_normalization=False,
#  samplewise_std_normalization=False,
#  zca_whitening=False,
#  rotation_range=10,
#  zoom_range = 0.1,
#  width_shift_range=0.2,
#  height_shift_range=0.2,
#  horizontal_flip=True,
#  vertical_flip=False)
# augs_gen.fit(x_train)

cnn = models.Sequential()
cnn.add(layers.Conv2D(32,(4,4),activation='relu',input_shape=(100,100,3)))
cnn.add(layers.BatchNormalization())
cnn.add(layers.Dropout(0.25))
cnn.add(layers.MaxPooling2D((2,2)))
cnn.add(layers.Conv2D(64,(3,3),activation='relu'))
cnn.add(layers.BatchNormalization())
cnn.add(layers.Dropout(0.25))
cnn.add(layers.MaxPooling2D((2,2)))
cnn.add(layers.Conv2D(55,(3,3),activation='relu'))
cnn.add(layers.BatchNormalization())
cnn.add(layers.Dropout(0.25))
cnn.add(layers.MaxPooling2D((2,2)))
cnn.add(layers.Flatten())
cnn.add(layers.Dense(50,activation='softmax'))
cnn.compile(loss='binary_crossentropy',
 optimizer=optimizers.Adam(lr=0.0005),
 metrics=['accuracy'])

history = cnn.fit(x_train,y_train,batch_size=200,validation_data=(x_test,y_test),epochs=2,verbose=1)

# def show_history(history): #显示训练过程学习曲线
#     loss = history.history['loss']
#     val_loss = history.history['val_loss']
#     epochs = range(1, len(loss) +1)
#     plt.figure(figsize=(12,4))
#     plt.subplot(1, 2, 1)
#     plt.plot(epochs, loss, 'bo', label='训练损失')
#     plt.plot(epochs, val_loss, 'b', label='验证损失')
#     plt.title('Training and validation loss')
#     plt.xlabel('Epochs')
#     plt.ylabel('Loss')
#     plt.legend()
#     acc = history.history['accuracy']
#     val_acc = history.history['val_accuracy']
#     plt.subplot(1, 2, 2)
#     plt.plot(epochs, acc, 'bo', label='训练正确精度')
#     plt.plot(epochs, val_acc, 'b', label='验证正确精度')
#     plt.title('Training and validation accuracy')
#     plt.xlabel('Epochs')
#     plt.ylabel('Accuracy')
#     plt.legend()
#     plt.show()
# show_history(history)
import joblib
joblib.dump(cnn, './model_save/cnn_face_3.pkl')
img_1 = io.imread(r'C:\Users\DTE_ccc\Desktop\1111.jpg')
image = transform.resize(img_1,(100,100))
image = image / 255.0
image = image.astype('float16')
image = image.reshape(1,100,100,3)
predict = cnn.predict(image)
print(predict)
predict_1 = np.argmax(predict)
print(predict_1)