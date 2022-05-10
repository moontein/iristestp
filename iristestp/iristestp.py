
# -*- coding: UTF-8 -*-
# �����β�����ݼ���ʵ��ǰ�򴫲������򴫲������ӻ�loss����

# ��������ģ��
import tensorflow as tf
from sklearn import datasets
from matplotlib import pyplot as plt
import numpy as np

# �������ݣ��ֱ�Ϊ���������ͱ�ǩ
x_data = datasets.load_iris().data
y_data = datasets.load_iris().target

# ����������ݣ���Ϊԭʼ������˳��ģ�˳�򲻴��һ�Ӱ��׼ȷ�ʣ�
# seed: ��������ӣ���һ��������������֮��ÿ�����ɵ��������һ����Ϊ�����ѧ���Ա�ÿλͬѧ���һ�£�
np.random.seed(116)  # ʹ����ͬ��seed����֤���������ͱ�ǩһһ��Ӧ
np.random.shuffle(x_data)
np.random.seed(116)
np.random.shuffle(y_data)
tf.random.set_seed(116)

# �����Һ�����ݼ��ָ�Ϊѵ�����Ͳ��Լ���ѵ����Ϊǰ120�У����Լ�Ϊ��30��
x_train = x_data[:-30]
y_train = y_data[:-30]
x_test = x_data[-30:]
y_test = y_data[-30:]

# ת��x���������ͣ��������������ʱ�����������Ͳ�һ�±���
x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# from_tensor_slices����ʹ���������ͱ�ǩֵһһ��Ӧ���������ݼ������Σ�ÿ������batch�����ݣ�
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(32)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

# ����������Ĳ�����4�����������ʣ������Ϊ4������ڵ㣻��Ϊ3���࣬�������Ϊ3����Ԫ
# ��tf.Variable()��ǲ�����ѵ��
# ʹ��seedʹÿ�����ɵ��������ͬ�������ѧ��ʹ��ҽ����һ�£�����ʵʹ��ʱ��дseed��
w1 = tf.Variable(tf.random.truncated_normal([4, 3], stddev=0.1, seed=1))
b1 = tf.Variable(tf.random.truncated_normal([3], stddev=0.1, seed=1))

lr = 0.1  # ѧϰ��Ϊ0.1
train_loss_results = []  # ��ÿ�ֵ�loss��¼�ڴ��б��У�Ϊ������loss�����ṩ����
test_acc = []  # ��ÿ�ֵ�acc��¼�ڴ��б��У�Ϊ������acc�����ṩ����
epoch = 500  # ѭ��500��
loss_all = 0  # ÿ�ַ�4��step��loss_all��¼�ĸ�step���ɵ�4��loss�ĺ�

# ѵ������
for epoch in range(epoch):  #���ݼ������ѭ����ÿ��epochѭ��һ�����ݼ�
    for step, (x_train, y_train) in enumerate(train_db):  #batch�����ѭ�� ��ÿ��stepѭ��һ��batch
        with tf.GradientTape() as tape:  # with�ṹ��¼�ݶ���Ϣ
            y = tf.matmul(x_train, w1) + b1  # ������˼�����
            y = tf.nn.softmax(y)  # ʹ���y���ϸ��ʷֲ����˲������������ͬ�������������loss��
            y_ = tf.one_hot(y_train, depth=3)  # ����ǩֵת��Ϊ�������ʽ���������loss��accuracy
            loss = tf.reduce_mean(tf.square(y_ - y))  # ���þ��������ʧ����mse = mean(sum(y-out)^2)
            loss_all += loss.numpy()  # ��ÿ��step�������loss�ۼӣ�Ϊ������lossƽ��ֵ�ṩ���ݣ����������loss��׼ȷ
        # ����loss�Ը����������ݶ�
        grads = tape.gradient(loss, [w1, b1])

        # ʵ���ݶȸ��� w1 = w1 - lr * w1_grad    b = b - lr * b_grad
        w1.assign_sub(lr * grads[0])  # ����w1�Ը���
        b1.assign_sub(lr * grads[1])  # ����b�Ը���

    # ÿ��epoch����ӡloss��Ϣ
    print("Epoch {}, loss: {}".format(epoch, loss_all/4))
    train_loss_results.append(loss_all / 4)  # ��4��step��loss��ƽ����¼�ڴ˱�����
    loss_all = 0  # loss_all���㣬Ϊ��¼��һ��epoch��loss��׼��

    # ���Բ���
    # total_correctΪԤ��Ե���������, total_numberΪ���Ե���������������������������ʼ��Ϊ0
    total_correct, total_number = 0, 0
    for x_test, y_test in test_db:
        # ʹ�ø��º�Ĳ�������Ԥ��
        y = tf.matmul(x_test, w1) + b1
        y = tf.nn.softmax(y)
        pred = tf.argmax(y, axis=1)  # ����y�����ֵ����������Ԥ��ķ���
        # ��predת��Ϊy_test����������
        pred = tf.cast(pred, dtype=y_test.dtype)
        # ��������ȷ����correct=1������Ϊ0����bool�͵Ľ��ת��Ϊint��
        correct = tf.cast(tf.equal(pred, y_test), dtype=tf.int32)
        # ��ÿ��batch��correct��������
        correct = tf.reduce_sum(correct)
        # ������batch�е�correct��������
        total_correct += int(correct)
        # total_numberΪ���Ե�����������Ҳ����x_test��������shape[0]���ر���������
        total_number += x_test.shape[0]
    # �ܵ�׼ȷ�ʵ���total_correct/total_number
    acc = total_correct / total_number
    test_acc.append(acc)
    print("Test_acc:", acc)
    print("--------------------------")

# ���� loss ����
plt.title('Loss Function Curve')  # ͼƬ����
plt.xlabel('Epoch')  # x���������
plt.ylabel('Loss')  # y���������
plt.plot(train_loss_results, label="$Loss$")  # ��㻭��trian_loss_resultsֵ�����ߣ�����ͼ����Loss
plt.legend()  # ��������ͼ��
plt.show()  # ����ͼ��

# ���� Accuracy ����
plt.title('Acc Curve')  # ͼƬ����
plt.xlabel('Epoch')  # x���������
plt.ylabel('Acc')  # y���������
plt.plot(test_acc, label="$Accuracy$")  # ��㻭��test_accֵ�����ߣ�����ͼ����Accuracy
plt.legend()
plt.show()
