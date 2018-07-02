from keras.models import Model
from keras.layers import Input, Dense, GRU, Embedding, Concatenate, Bidirectional, Dropout
from keras.optimizers import Adam


class OnehotBasedModel:
    @staticmethod
    def get_default_configuration():
        return {'num_model': 5,
                'max_num_epoch': 500,
                'embedded_dim': 6,
                'gru_dim': 160,
                'dropout_gru': 0.4,
                'dropout_recurrence_gru': 0.3,
                'dense_dropout': 0.4}

    @staticmethod
    def get_one_hot_based_model(configuration, max_peptide_length, num_acceptable_allele):
        input1 = Input(shape=(max_peptide_length,))
        input2 = Input(shape=(num_acceptable_allele,))
        x1_1 = Embedding(input_dim=21,
                         output_dim=configuration['embedded_dim'],
                         mask_zero=True,
                         name="Amino_Acid_Embedding_Layer")(input1)
        x1_1 = Bidirectional(GRU(configuration['gru_dim'],
                                 dropout=configuration['dropout_gru'],
                                 recurrent_dropout=configuration['dropout_recurrence_gru']))(x1_1)

        x3 = Concatenate()([x1_1, input2])
        x3 = Dense(210, activation='relu')(x3)
        x3 = Dense(210, activation='relu')(x3)
        x3 = Dropout(configuration['dense_dropout'])(x3)
        out = Dense(1, activation='sigmoid')(x3)

        model = Model(inputs=[input1, input2], outputs=out)
        model.compile(optimizer=Adam(),
                      loss='binary_crossentropy',
                      metrics=['acc'])
        return model