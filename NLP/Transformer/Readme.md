### Introducction

To combine the advantages from both CNNs and RNNs, [Vaswani et al., 2017] designed a novel architecture using the attention mechanism.

This architecture, which is called as Transformer, achieves parallelization by capturing recurrence sequence with attention and at the same time encodes each item’s position in the sequence. As a result, Transformer leads to a compatible model with significantly shorter training time.

Similar to the seq2seq model, Transformer is also based on the encoder-decoder architecture. However, Transformer differs from the former by replacing the recurrent layers in seq2seq with multi-head attention layers, incorporating the position-wise information through position encoding, and applying layer normalization. We compare Transformer and seq2seq side-by-side.
