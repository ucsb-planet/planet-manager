from planet_manager.collection import Collection


class Collections:
    def __init__(self, collections: list[Collection] = []):
        self.__collections = collections
        self.__current = 0

    def append(self, collection):
        self.__collections.append(collection)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current >= len(self.__collections):
            raise StopIteration

        el = self.__collections[self.__current]
        self.__current += 1

        return el

    @staticmethod
    def load(input: list):
        collections = []
        for collection_json in input:
            collection = Collection.load(collection_json)
            collections.append(collection)

        return Collections(collections)
