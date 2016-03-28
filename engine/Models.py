import tensorflow as tf
import math

def conv(inputs, diameter, Nin, Nout, name):
    fan_in = diameter * diameter * Nin
    stddev = math.sqrt(2.0 / fan_in)
    kernel = tf.Variable(tf.truncated_normal([diameter, diameter, Nin, Nout], stddev=stddev), name=name+'_kernel')
    return tf.nn.conv2d(inputs, kernel, [1, 1, 1, 1], padding='SAME')

def conv_uniform_bias(inputs, diameter, Nin, Nout, name):
    bias = tf.Variable(tf.constant(0.0, shape=[Nout]), name=name+'_bias')
    return conv(inputs, diameter, Nin, Nout, name) + bias

def conv_pos_dep_bias(inputs, diameter, Nin, Nout, N, name):
    bias = tf.Variable(tf.constant(0.0, shape=[N, N, Nout]), name=name+'_bias')
    return conv(inputs, diameter, Nin, Nout, name) + bias

def relu_conv_uniform_bias(inputs, diameter, Nin, Nout, name):
    return tf.nn.relu(conv_uniform_bias(inputs, diameter, Nin, Nout, name))

def relu_conv_pos_dep_bias(inputs, diameter, Nin, Nout, N, name):
    return tf.nn.relu(conv_pos_dep_bias(inputs, diameter, Nin, Nout, N, name))

def ELU_conv_pos_dep_bias(inputs, diameter, Nin, Nout, N, name):
    return tf.nn.elu(conv_pos_dep_bias(inputs, diameter, Nin, Nout, N, name))

def linear_layer(inputs, Nin, Nout):
    stddev = math.sqrt(2.0 / Nin)
    print "linear layer using stddev =", stddev
    weights = tf.Variable(tf.truncated_normal([Nin, Nout], stddev=0.1))
    bias = tf.Variable(tf.constant(0.1, shape=[Nout]))
    out = tf.matmul(inputs, weights) + bias
    return out

def fully_connected_layer(inputs, Nin, Nout):
    return tf.nn.relu(linear_layer(inputs, Nin, Nout))


class Linear:
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_linear_N%d_mb%d_fe_%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
    def inference(self, feature_planes, N, Nfeat):
        flat_features = tf.reshape(feature_planes, [-1, N*N*Nfeat])
        logits = linear_layer(flat_features, N*N*Nfeat, N*N)
        return logits



class SingleFull: # recommend 9x9, mbs=1000, adam, lr=0.003
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_single_full_N%d_mb%d_fe_%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
    def inference(self, feature_planes, N, Nfeat):
        Nhidden = 1024
        flat_features = tf.reshape(feature_planes, [-1, N*N*Nfeat])
        hidden = fully_connected_layer(flat_features, N*N*Nfeat, Nhidden)
        logits = linear_layer(hidden, Nhidden, N*N)
        return logits

class Conv3Full: # recommend 9x9, mbs=1000, adam, lr=0.003
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_conv3_full_N%d_mb%d_fe_%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
    def inference(self, feature_planes, N, Nfeat):
        NK = 32
        Nhidden = 1024
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK)
        conv2 = conv_layer(conv1, 3, NK, NK)
        conv3 = conv_layer(conv2, 3, NK, NK)
        conv3_flat = tf.reshape(conv3, [-1, N*N*NK])
        hidden4 = fully_connected_layer(conv3_flat, N*N*NK, Nhidden)
        logits = linear_layer(hidden4, Nhidden, N*N)
        return logits

class Conv4Full: 
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_conv4_full_N%d_mb%d_fe_%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
    def inference(self, feature_planes, N, Nfeat):
        NK = 64
        Nhidden = 1024
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK, stddev=0.01)
        conv2 = conv_layer(conv1, 3, NK, NK, stddev=0.01)
        conv3 = conv_layer(conv2, 3, NK, NK, stddev=0.01)
        conv4 = conv_layer(conv3, 3, NK, NK, stddev=0.01)
        conv4_flat = tf.reshape(conv4, [-1, N*N*NK])
        hidden5 = fully_connected_layer(conv4_flat, N*N*NK, Nhidden)
        logits = linear_layer(hidden5, Nhidden, N*N)
        return logits

class Conv5Full: 
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_conv5_full_N%d_mb%d_fe_%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
    def inference(self, feature_planes, N, Nfeat):
        NK = 128
        Nhidden = 1024
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK, stddev=0.01)
        conv2 = conv_layer(conv1, 3, NK, NK, stddev=0.01)
        conv3 = conv_layer(conv2, 3, NK, NK, stddev=0.01)
        conv4 = conv_layer(conv3, 3, NK, NK, stddev=0.01)
        conv5 = conv_layer(conv4, 3, NK, NK, stddev=0.01)
        conv5_flat = tf.reshape(conv5, [-1, N*N*NK])
        hidden6 = fully_connected_layer(conv5_flat, N*N*NK, Nhidden)
        logits = linear_layer(hidden6, Nhidden, N*N)
        return logits

class Conv8: 
    def __init__(self, N, Nfeat, minibatch_size=1000, learning_rate=0.0003):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_conv8_N%d_mb%d_fe%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 128
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK, stddev=0.01)
        conv2 = conv_layer(conv1, 3, NK, NK, stddev=0.01)
        conv3 = conv_layer(conv2, 3, NK, NK, stddev=0.01)
        conv4 = conv_layer(conv3, 3, NK, NK, stddev=0.01)
        conv5 = conv_layer(conv4, 3, NK, NK, stddev=0.01)
        conv6 = conv_layer(conv5, 3, NK, NK, stddev=0.01)
        conv7 = conv_layer(conv6, 3, NK, NK, stddev=0.01)
        conv8 = conv_layer(conv7, 1, NK, 1, stddev=0.01) # todo: switch to no_relu
        conv8_flat = tf.reshape(conv8, [-1, N*N])        
        bias = tf.Variable(tf.constant(0, shape=[N*N], dtype=tf.float32)) # position-dependent bias
        logits = conv8_flat + bias
        return logits

class Conv8Full: 
    def __init__(self, N, Nfeat, minibatch_size, learning_rate):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/ckpts_conv8_full_N%d_mb%d_fe%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 128
        Nhidden = 1024
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK)
        conv2 = conv_layer(conv1, 3, NK, NK)
        conv3 = conv_layer(conv2, 3, NK, NK)
        conv4 = conv_layer(conv3, 3, NK, NK)
        conv5 = conv_layer(conv4, 3, NK, NK)
        conv6 = conv_layer(conv5, 3, NK, NK)
        conv7 = conv_layer(conv6, 3, NK, NK)
        conv8 = conv_layer(conv7, 3, NK, NK)
        conv8_flat = tf.reshape(conv8, [-1, N*N*NK])        
        hidden9 = fully_connected_layer(conv8_flat, N*N*NK, Nhidden)
        logits = linear_layer(hidden9, Nhidden, N*N)
        return logits

# didn't get higher than ~33% on KGS :(
class Conv12: # AlphaGo architecture
    def __init__(self, N, Nfeat, minibatch_size=1000, learning_rate=0.0003):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/ckpts_conv12_N%d_mb%d_fe%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 128
        conv1 = conv_layer(feature_planes, 5, Nfeat, NK)
        conv2 = conv_layer(conv1, 3, NK, NK)
        conv3 = conv_layer(conv2, 3, NK, NK)
        conv4 = conv_layer(conv3, 3, NK, NK)
        conv5 = conv_layer(conv4, 3, NK, NK)
        conv6 = conv_layer(conv5, 3, NK, NK)
        conv7 = conv_layer(conv6, 3, NK, NK)
        conv8 = conv_layer(conv7, 3, NK, NK)
        conv9 = conv_layer(conv8, 3, NK, NK)
        conv10 = conv_layer(conv9, 3, NK, NK)
        conv11 = conv_layer(conv10, 3, NK, NK)
        conv12 = conv_layer_no_relu(conv11, 1, NK, 1)
        conv12_flat = tf.reshape(conv12, [-1, N*N])        
        bias = tf.Variable(tf.constant(0, shape=[N*N], dtype=tf.float32)) # position-dependent bias
        logits = conv12_flat + bias
        return logits

# smallest network described in Maddison et al. paper
# They claim 37.5% accuracy on KGS
# One difference is that they have two output planes, one for each color
class MaddisonMinimal: 
    def __init__(self, N, Nfeat, minibatch_size=1000, learning_rate=0.0003):
        self.checkpoint_dir = "/home/greg/coding/ML/go/NN/engine/checkpoints/maddison_minimal_N%d_mb%d_fe%d" % (N, minibatch_size, Nfeat)
        self.learning_rate = learning_rate
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 16
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NK, self.N)
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NK, NK, self.N)
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, self.N)
        conv4 = conv_pos_dep_bias(conv3, 1, NK, 1, self.N)
        logits = tf.reshape(conv4, [-1, N*N])
        return logits

class Conv6PosDep: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/conv6posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 128
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NK, N, 'conv1')
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NK, NK, N, 'conv2')
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = relu_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = relu_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = conv_pos_dep_bias(conv5, 3, NK, 1, N, 'conv6') 
        logits = tf.reshape(conv6, [-1, N*N])        
        return logits

# Got to ~46.7% on KGS after 58K minibatches of 256 (~12 hours of training), NK=192, learning_rate=0.03
class Conv8PosDep: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/conv8posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 192
        NKfirst = 192
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NKfirst, N, 'conv1')
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NKfirst, NK, N, 'conv2')
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = relu_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = relu_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = relu_conv_pos_dep_bias(conv5, 3, NK, NK, N, 'conv6')
        conv7 = relu_conv_pos_dep_bias(conv6, 3, NK, NK, N, 'conv7')
        conv8 = conv_pos_dep_bias(conv7, 3, NK, 1, N, 'conv8') 
        logits = tf.reshape(conv8, [-1, N*N])        
        return logits

class Conv10PosDep: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/conv10posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 192
        NKfirst = 192
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NKfirst, N, 'conv1')
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NKfirst, NK, N, 'conv2')
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = relu_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = relu_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = relu_conv_pos_dep_bias(conv5, 3, NK, NK, N, 'conv6')
        conv7 = relu_conv_pos_dep_bias(conv6, 3, NK, NK, N, 'conv7')
        conv8 = relu_conv_pos_dep_bias(conv7, 3, NK, NK, N, 'conv8')
        conv9 = relu_conv_pos_dep_bias(conv8, 3, NK, NK, N, 'conv9')
        conv10 = conv_pos_dep_bias(conv9, 3, NK, 1, N, 'conv10') 
        logits = tf.reshape(conv10, [-1, N*N])        
        return logits

# ELUs seem to give a ~1.1% increase in training accuracy out to at least 
# 12K minibatches of 256. This is with the centering transformation
#       loaded_feature_planes = (loaded_feature_planes.astype(np.float32) - 0.154) * 2.77
# on KGS data using make_feature_planes_stones_3liberties_4history_ko
# Using ReLUs, that centering transformation produces only a ~0.2% increase in training accuracy
# which seems to be disappearing after 8K minibatches. But with ELUs it is more permanent?
class Conv10PosDepELU: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/conv10posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 192
        NKfirst = 192
        conv1 = ELU_conv_pos_dep_bias(feature_planes, 5, Nfeat, NKfirst, N, 'conv1')
        conv2 = ELU_conv_pos_dep_bias(conv1, 3, NKfirst, NK, N, 'conv2')
        conv3 = ELU_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = ELU_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = ELU_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = ELU_conv_pos_dep_bias(conv5, 3, NK, NK, N, 'conv6')
        conv7 = ELU_conv_pos_dep_bias(conv6, 3, NK, NK, N, 'conv7')
        conv8 = ELU_conv_pos_dep_bias(conv7, 3, NK, NK, N, 'conv8')
        conv9 = ELU_conv_pos_dep_bias(conv8, 3, NK, NK, N, 'conv9')
        conv10 = conv_pos_dep_bias(conv9, 3, NK, 1, N, 'conv10') 
        logits = tf.reshape(conv10, [-1, N*N])        
        return logits

class Conv12PosDep: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/conv12posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 192
        NKfirst = 192
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NKfirst, N, 'conv1')
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NKfirst, NK, N, 'conv2')
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = relu_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = relu_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = relu_conv_pos_dep_bias(conv5, 3, NK, NK, N, 'conv6')
        conv7 = relu_conv_pos_dep_bias(conv6, 3, NK, NK, N, 'conv7') 
        conv8 = relu_conv_pos_dep_bias(conv7, 3, NK, NK, N, 'conv8')
        conv9 = relu_conv_pos_dep_bias(conv8, 3, NK, NK, N, 'conv9')
        conv10 = relu_conv_pos_dep_bias(conv9, 3, NK, NK, N, 'conv10')
        conv11 = relu_conv_pos_dep_bias(conv10, 3, NK, NK, N, 'conv11')
        conv12 = conv_pos_dep_bias(conv11, 3, NK, 1, N, 'conv12') 
        logits = tf.reshape(conv12, [-1, N*N])        
        return logits


class FirstMoveTest: 
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/first_move_test"
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        bias = tf.Variable(tf.constant(0.0, shape=[self.N, self.N, 1]), name='single_bias')
        logits = tf.reshape(bias, [-1, N*N])
        return logits



class InfluenceConv8PosDep:
    def __init__(self, N, Nfeat):
        self.train_dir = "/home/greg/coding/ML/go/NN/engine/train_dirs/influence_conv8posdep_N%d_fe%d" % (N, Nfeat)
        self.N = N
        self.Nfeat = Nfeat
    def inference(self, feature_planes, N, Nfeat):
        NK = 192
        NKfirst = 192
        conv1 = relu_conv_pos_dep_bias(feature_planes, 5, Nfeat, NKfirst, N, 'conv1')
        conv2 = relu_conv_pos_dep_bias(conv1, 3, NKfirst, NK, N, 'conv2')
        conv3 = relu_conv_pos_dep_bias(conv2, 3, NK, NK, N, 'conv3')
        conv4 = relu_conv_pos_dep_bias(conv3, 3, NK, NK, N, 'conv4')
        conv5 = relu_conv_pos_dep_bias(conv4, 3, NK, NK, N, 'conv5')
        conv6 = relu_conv_pos_dep_bias(conv5, 3, NK, NK, N, 'conv6')
        conv7 = relu_conv_pos_dep_bias(conv6, 3, NK, NK, N, 'conv7')
        conv8 = conv_pos_dep_bias(conv7, 3, NK, 1, N, 'conv8') 
        logits = tf.reshape(conv8, [-1, N*N])        
        return logits # use with sigmoid and sigmoid_cross_entropy_with_logits

