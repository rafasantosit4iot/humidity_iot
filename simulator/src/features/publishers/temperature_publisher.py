from shared.payload import Payload
from features.publishers.publisher_abs import Publisher

import random

from shared.enum.scalar import Scalar

class TemperaturePublisher(Publisher):
    def generate_data(self):
        value = round(random.uniform(self.min_value, self.max_value), 2)
        payload = Payload(Scalar.TEMPERATURA, self.id, value)
        return payload
