"""
attention connect encoder and decoder
In "encoder-decoder attention" layers, the queries come from the previous decoder layer,
and the memory keys and values come from the output of the encoder. This allows every
position in the decoder to attend over all positions in the input sequence. This mimics the
typical encoder-decoder attention mechanisms in sequence-to-sequence models.
"""
import tensorflow as tf
from a2_base_model import BaseClass
from  a2_multi_head_attention import MultiHeadAttention

class AttentionEncoderDecoder(BaseClass):
    def __init__(self,d_model, d_k, d_v, sequence_length, h, batch_size,Q, K_s,layer_index,decoder_sent_length,type="attention"):
        """
        :param d_model:
        :param d_k:
        :param d_v:
        :param sequence_length:
        :param h:
        :param batch_size:
        :param Q: value from decoder
        :param K_s: output of encoder
        """
        super(AttentionEncoderDecoder, self).__init__(d_model, d_k, d_v, sequence_length, h, batch_size)
        self.Q=Q
        self.K_s=K_s
        self.layer_index=layer_index
        self.type=type
        self.decoder_sent_length=decoder_sent_length
        self.initializer = tf.random_normal_initializer(stddev=0.1)

    def attention_encoder_decoder_fn(self):
        #call multi head attention function to perform this task.
        return self.sub_layer_multi_head_attention(self.layer_index,self.Q,self.K_s,self.type)


#test attention between encoder and decoder
def test():
    d_model = 512
    d_k = 64
    d_v = 64
    sequence_length = 10
    decoder_sent_length=6
    h = 8
    batch_size=4
    initializer = tf.random_normal_initializer(stddev=0.1)
    # 2.set Q,K,V
    vocab_size=1000
    embed_size=d_model
    Embedding = tf.get_variable("Embedding", shape=[vocab_size, embed_size],initializer=initializer)
    input_x = tf.placeholder(tf.int32, [batch_size,decoder_sent_length], name="input_x") #[4,10]
    print("input_x:",input_x)
    input_x_=tf.reshape(input_x,(batch_size*decoder_sent_length,)) #[batch_size*decoder_sent_length]
    embedded_words = tf.nn.embedding_lookup(Embedding, input_x_) #[batch_size*decoder_sent_length,embed_size]

    Q = embedded_words  #[batch_size*decoder_sent_length,embed_size]
    K_s = tf.ones((batch_size*sequence_length,embed_size),dtype=tf.float32)  # [batch_size*sequence_length,embed_size]
    layer_index = 0
    attention_between_encoder_decoder_class=AttentionEncoderDecoder(d_model, d_k, d_v, sequence_length, h, batch_size,Q, K_s,layer_index,decoder_sent_length)
    attention_output=attention_between_encoder_decoder_class.attention_encoder_decoder_fn()
    print("attention_output:",attention_output)

#test()