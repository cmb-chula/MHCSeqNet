import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Embedding, Flatten
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping


class AminoAcidRepresentationModel:
    AMINO_ACIDS = ['^', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W',
                   'Y']
    proteinSize = 0

    def count_amino_acid_pair_frequency(self,
                                        filename,
                                        window_size=2):
        print("Pre-processing Data. This may take some time.")
        file = open(filename, "r")
        pair_map = {}
        line_count = 0
        for line in file:
            line = "^" + line
            line_count += 1
            for i in range(len(line)):
                for j in range(i - window_size, i + window_size + 1):
                    if j < 0 or j >= len(line) or i == j or line[i] not in self.AMINO_ACIDS or line[j] not in self.AMINO_ACIDS:
                        continue
                    try:
                        pair_map[(line[i], line[j])] += 1
                    except KeyError:
                        pair_map[(line[i], line[j])] = 1
        pair_list = []
        pair_distribution = []
        for key, value in pair_map.items():
            pair_list.append(key)
            pair_distribution.append(value)
        return pair_distribution, pair_list
    
    def __init__(self,
                 data_filename,
                 window_size,
                 embedding_dim,
                 model_filename):
        self.model_filename = model_filename
        self.embedding_dim = embedding_dim
        self.proteinSize = len(self.AMINO_ACIDS)
        pair_distribution, pair_list = self.count_amino_acid_pair_frequency(data_filename, window_size)

        self.pairDistribution = np.array(pair_distribution)
        self.pairDistribution = self.pairDistribution / np.sum(self.pairDistribution)
        self.pairArraySize = len(pair_list)
        self.model = self._create_model(embedded_dim=self.embedding_dim)

        self.protein2int = {}
        self.int2protein = {}
        self.proteinPairArray = np.array(pair_list)
        for i, protein in enumerate(self.AMINO_ACIDS):
            self.protein2int[protein] = i
            self.int2protein[i] = protein

        self.proteinPairArray = np.array(pair_list)
        proteinPairArrayTempX = np.zeros(self.pairArraySize)
        proteinPairArrayTempY = np.zeros((self.pairArraySize, self.proteinSize))
        for i in range(self.pairArraySize):
            proteinPairArrayTempX[i] = self.protein2int[self.proteinPairArray[i, 0]]
            proteinPairArrayTempY[i] = self._to_one_hot(
                self.protein2int[self.proteinPairArray[i, 1]],
                vocab_size=self.proteinSize)
        self.proteinPairArray_x = proteinPairArrayTempX  # Input is array of index
        self.proteinPairArray_y = proteinPairArrayTempY  # Output is one-hot

    def train(self,
              step_size,
              step_per_epoch,
              max_num_epoch):

        callbacks_list = [
            ModelCheckpoint(
                self.model_filename + ".h5",
                save_best_only=True,
                save_weights_only=True,
                monitor='val_loss',
                mode='min',
                verbose=1
            ),
            EarlyStopping(monitor='val_loss',
                          min_delta=0,
                          patience=7,
                          verbose=2, mode='auto')
        ]
        self.model.fit_generator(self._generate_data(step_size),
                                 epochs=max_num_epoch,
                                 steps_per_epoch=step_per_epoch,
                                 verbose=2,
                                 callbacks=callbacks_list,
                                 validation_data=self._generate_data(step_size),
                                 validation_steps=step_per_epoch)

    def _create_model(self, embedded_dim):
        input1 = Input(shape=(1,))
        x = Embedding(input_dim=self.proteinSize,
                      input_length=1,
                      output_dim=embedded_dim)(input1)
        x = Flatten()(x)
        out = Dense(self.proteinSize, activation='sigmoid')(x)

        model = Model(inputs=input1, outputs=out)
        model.compile(optimizer=Adam(),
                      loss='categorical_crossentropy',
                      metrics=['acc'])
        return model

    def _generate_data(self, size):
        for i in range(10**100):
            data_index = np.random.choice(self.pairArraySize,
                                          size,
                                          p=self.pairDistribution)
            data_x = self.proteinPairArray_x[data_index]
            data_y = self.proteinPairArray_y[data_index]
            x_train = data_x
            y_train = data_y
            yield x_train, y_train

    def _to_one_hot(self, index, vocab_size):
        temp = np.zeros(vocab_size)
        temp[index] = 1
        return temp



