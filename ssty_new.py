import tensorflow as tf

import numpy as np
import IPython.display as display
import os

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))




def image_example(image_string, label):
  image_shape = tf.image.decode_jpeg(image_string).shape

  feature = {
      'height': _int64_feature(image_shape[0]),
      'width': _int64_feature(image_shape[1]),
      'depth': _int64_feature(image_shape[2]),
      'label': _int64_feature(label),
      'image_raw': _bytes_feature(image_string),
  }

  return tf.train.Example(features=tf.train.Features(feature=feature))

def create_tf(cwd, record_path):
    classes=['daisy',
         'dandelion',
         'roses',
         'sunflowers',
         'tulips']
    for index, name in enumerate(classes):
        record_file = record_path + name+'.tfrecords'
        class_path=os.path.join(cwd,name)
        with tf.io.TFRecordWriter(record_file) as writer:
            for img_name in os.listdir(class_path):
                file_name = class_path + '/' + img_name
                image_string = open(file_name, 'rb').read()
                tf_example = image_example(image_string, index)
                writer.write(tf_example.SerializeToString())
    return




cwd = 'flowers_ss' 
record_path = 'tfss/'

ret = create_tf(cwd, record_path)


