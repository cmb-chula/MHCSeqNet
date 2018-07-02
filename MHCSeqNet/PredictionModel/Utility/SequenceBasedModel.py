from keras.models import Model
from keras.layers import Input, Dense, GRU, Embedding, Concatenate, Bidirectional, Dropout, Flatten
from keras.optimizers import Adam


class SequenceBasedModel:
    @staticmethod
    def get_default_configuration():
        return {'num_model': 5,
                'max_num_epoch': 500,
                'embedded_dim': 6,
                'gru_dim': 352,
                'dropout_gru': 0.4,
                'dropout_recurrence_gru': 0.3,
                'allele_dense_size': 250,
                'allele_embedding_size': 6,
                'allele_dropout': 0.5,
                'dense_size': 240,
                'dense_dropout': 0.4}

    @staticmethod
    def get_sequence_based_model(configuration, max_peptide_length, num_acceptable_allele, sequence_lengths):
        # print(embedded_dim, gru_dim, dropout_1, num_dense, dense_size, dropout, dense_allele)
        input1 = Input(shape=(max_peptide_length,))
        input2_mid = Input(shape=(sequence_lengths[1],))
        input2_last = Input(shape=(sequence_lengths[2],))

        # Input 1
        x1_1 = Embedding(input_dim=21,
                         output_dim=configuration['embedded_dim'],
                         mask_zero=True,
                         name="Amino_Acid_Embedding_Layer")(input1)
        x1_1 = Bidirectional(GRU(configuration['gru_dim'],
                                 dropout=configuration['dropout_gru'],
                                 recurrent_dropout=configuration['dropout_recurrence_gru']))(x1_1)

        # Input 2 mid
        x2_mid = Embedding(input_dim=21 + 2, output_dim=configuration['allele_embedding_size'])(input2_mid)
        x2_mid = Flatten()(x2_mid)
        x2_mid = Dense(configuration['allele_dense_size'], activation='relu')(x2_mid)
        x2_mid = Dropout(configuration['allele_dropout'])(x2_mid)

        # Input 2 last
        x2_last = Embedding(input_dim=21+ 2, output_dim=configuration['allele_embedding_size'])(input2_last)
        x2_last = Flatten()(x2_last)
        x2_last = Dense(configuration['allele_dense_size'], activation='relu')(x2_last)
        x2_last = Dropout(configuration['allele_dropout'])(x2_last)

        # Concat
        x3 = Concatenate()([x1_1, x2_mid, x2_last])
        x3 = Dense(configuration['dense_size'], activation='relu')(x3)
        x3 = Dense(configuration['dense_size'], activation='relu')(x3)
        x3 = Dropout(configuration['dense_dropout'])(x3)
        out = Dense(1, activation='sigmoid')(x3)

        model = Model(inputs=[input1, input2_mid, input2_last], outputs=out)
        model.compile(optimizer=Adam(),
                      loss='binary_crossentropy',
                      metrics=['acc'])
        return model