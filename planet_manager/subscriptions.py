from planet_manager.subscription import Subscription


class Subscriptions:
    def __init__(self, subscriptions: list[Subscription] = []):
        self.__subscriptions = subscriptions
        self.__current = 0

    def append(self, subscription):
        self.__subscriptions.append(subscription)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current >= len(self.__subscriptions):
            raise StopIteration

        el = self.__subscriptions[self.__current]
        self.__current += 1

        return el

    @staticmethod
    def load(input: list):
        subscriptions = []
        for subscription_json in input:
            subscription = Subscription.load(subscription_json)
            subscriptions.append(subscription)

        return Subscriptions(subscriptions)
