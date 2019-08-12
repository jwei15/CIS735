import tensorflow as tf

import sys
#import Image
from PIL import Image
import numpy as np
import imageio
import os


train = False

#if sys.argv[1] == 'train':
#    train = True

model_path = "./model/"


namelist = ["fyc", "hy", "ljg", "lqf", "lsl", "ml", "rj", "syj", "wl", "wq", "wyc", "xch", "xxj", "zc","zdx","zjg", "zl", "zyf"]

def nameToint(name):
    return namelist.index(name)

def read_data(data_dir):
    datas =  []
    labels = []
    fpaths = []
    for fname in os.listdir(data_dir):
        print(fname)
        fpath = os.path.join(data_dir, fname)
        fpaths.append(fpath)
        image = imageio.imread(fpath)
        #image = Image.open(fpath)
        data = (np.array(image) / 255.0).reshape(240,100,1)
        label = nameToint((fname.split("_")[0]))
        datas.append(data)
        labels.append(label)

    datas = np.array(datas)
    labels = np.array(labels)

    #print("shape of datas: {}\tshape of labels: {}".format(datas.shape,labels.shape))
    return fpaths, datas, labels

#fpaths, datas, labels = 
fpath, datas, labels = read_data("./cnn_data/")
fpath1, datas1, labels1 = read_data("./cnn_data_test/")

data_placeholder = tf.placeholder(tf.float32, [None,  240, 100, 1])

labels_placeholder = tf.placeholder(tf.int32, [None])

dropout_placeholder = tf.placeholder(tf.float32)

conv0 = tf.layers.conv2d(data_placeholder, 20, 5, activation=tf.nn.relu)

pool0 = tf.layers.max_pooling2d(conv0, [2,2], [2,2])

conv1 = tf.layers.conv2d(pool0, 40, 4, activation = tf.nn.relu)

pool1 = tf.layers.max_pooling2d(conv1, [2,2], [2,2])

flatten = tf.layers.flatten(pool1)

fc = tf.layers.dense(flatten, 400, activation = tf.nn.relu)
print("fc:\t", fc)

dropout_fc = tf.layers.dropout(fc, dropout_placeholder)
print("dropout:\t", dropout_fc)

logits = tf.layers.dense(dropout_fc, len(namelist))
print("Logics\t", logits)

predicted_labels = tf.argmax(logits, 1)
print("predicted_labels:\t",predicted_labels)

losses = tf.nn.softmax_cross_entropy_with_logits(
        labels=tf.one_hot(labels_placeholder, len(namelist)),
            logits=logits)
print("Losses:\t", losses)

mean_loss = tf.reduce_mean(losses)

optimizer = tf.train.AdamOptimizer(learning_rate = 1e-2).minimize(losses)

saver = tf.train.Saver()


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print("\n\n\n\n\n")
    print(sess.run(losses))
'''
with tf.Session() as sess:
    if train:
        print("Training")
        sess.run(tf.global_variables_initializer())

        train_feed_dict = {
                data_placeholder: datas,
                labels_placeholder: labels,
                dropout_placeholder: 0.05
                }

        for step in range(150):
            _, mean_loss_val = sess.run([optimizer, mean_loss],
                    feed_dict = train_feed_dict)
            if step %10 == 0:
                print("step = {}\t mean loss = {}".format(step, mean_loss_val))
                saver.save(sess, model_path)
    else:
        pass
        print("testing")
        saver.restore(sess, model_path)
        test_feed_dict = {
                data_placeholder:datas1,
                labels_placeholder:labels1,
                dropout_placeholder:0
                } 
        predicted_labels_val = sess.run(predicted_labels,
                feed_dict = test_feed_dict)
        
        acc = 0
        for i in range(len(predicted_labels_val)):
            if predicted_labels_val[i] == labels1[i]:
                acc = acc + 1
        print(float(acc / len(labels1)))
'''

