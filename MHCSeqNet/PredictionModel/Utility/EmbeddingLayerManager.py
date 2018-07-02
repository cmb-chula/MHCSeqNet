from keras.models import Model
from keras.layers import Input, Dense, Embedding, Flatten
from keras.optimizers import Adam


# Class to load embedding layer to the model.
class EmbeddingLayerManager:
    @staticmethod
    def get_word2vec_model(embedded_dim, num_amino_acid):
        input1 = Input(shape=(1,))
        x = Embedding(input_dim=num_amino_acid, output_dim=embedded_dim)(input1)
        x = Flatten()(x)
        out = Dense(num_amino_acid, activation='sigmoid')(x)
        model = Model(inputs=input1, outputs=out)
        model.compile(optimizer=Adam(),
                      loss='categorical_crossentropy',
                      metrics=['acc'])
        return model

    @staticmethod
    def load_embedded_weight(model, filename, embedded_dim, num_amino_acid, layer_index_to_load=1):
        weight_path = filename
        temp_model = EmbeddingLayerManager.get_word2vec_model(embedded_dim, num_amino_acid)
        temp_model.load_weights(weight_path)
        weight = temp_model.get_layer(index=1).get_weights()
        #model.get_layer(index=layer_index_to_load).set_weights(weight)
        model.get_layer("Amino_Acid_Embedding_Layer").set_weights(weight)