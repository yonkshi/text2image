from models import *
from lenet.pretrained import generated_lenet
from dataloader import *
import conf
import tensorflow as tf

def main():

    ###======================== DEFIINE MODEL ===================================###
    t_caption = tf.placeholder('float32', [conf.BATCH_SIZE, conf.CHAR_DEPTH, conf.ALPHA_SIZE], name = 'caption_input')
    # t_wrong_image = tf.placeholder('float32', [batch_size ,image_size, image_size, 3], name = 'wrong_image')
    # t_real_caption = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name='real_caption_input')
    # t_wrong_caption = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name='wrong_caption_input')
    # t_z = tf.placeholder(tf.float32, [batch_size, z_dim], name='z_noise')



    # raw input
    data = DataLoader()
    data.process_data()

    # Setting up Queue
    txt_encoder = build_char_cnn_rnn(t_caption)
    lenet_encoded, lenet_image, lenet_model = generated_lenet()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        for i in range(1000):
            captions, img, txt_seq = data.next_batch()
            encoded_text = sess.run(txt_encoder, feed_dict={t_caption: txt_seq})
            encoded_image = sess.run(lenet_encoded, feed_dict={lenet_image: img})


        coord.request_stop()
        coord.join(threads)

def loss(V, T):

    """
    Inputs come as a minibatch, disjoint classes!
    :param V: Batch of encoded images. n x 1024
    :param T: Batch of encoded texts. n x 1024
    :return: Loss of the batch
    """

    ########## TF vectorized ##########

    score = tf.matmul(V, tf.matrix_transpose(T))
    thresh = tf.nn.relu(score - tf.diag(score) + 1)
    loss = tf.reduce_mean(thresh)

    return loss


# # batch size and dimensionality
# n = 40
# d = 1024
#
# # Define the graph
# V = tf.constant(np.random.normal(0, 1, (n, d)), dtype=tf.float32, shape=(n, d))
# T = tf.constant(np.random.normal(0, 1, (n, d)), dtype=tf.float32, shape=(n, d))
# shape = tf.shape(V)
# l = loss(V, T)
#
# # Execute the graph
# with tf.Session() as sess:
#
#     l_out, V_out, T_out, shape_out = sess.run([l, V, T, shape])
#     a = 0


if __name__ == '__main__':
    main()