import random

from features.publishers.publisher_abs import Publisher
from shared.payload import Payload
from shared.enum.scalar import Scalar


class HumidityPublisher(Publisher):
    def generate_data(self):
        value = round(random.uniform(self.min_value, self.max_value), 2)
        payload = Payload(Scalar.UMIDADE, self.id, value)
        return payload