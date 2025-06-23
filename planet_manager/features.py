from planet_manager.feature import Feature


class Features:
    def __init__(self, features: list[Feature] = []):
        self.__features = features
        self.__current = 0

    def append(self, collection):
        self.__features.append(collection)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current >= len(self.__features):
            raise StopIteration

        el = self.__features[self.__current]
        self.__current += 1

        return el

    @staticmethod
    def load(input: list):
        features = []
        for feature_json in input:
            feature = Feature.load(feature_json)
            features.append(feature)

        return Features(features)
