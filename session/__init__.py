from dataclasses import dataclass, field


@dataclass
class Session:
    values : dict = field(default_factory=dict)

    def add_to_session(self, key, value):
        for k, v in self.values.items():
            if v == value:
                del self.values[k]
                break
        self.values[key] = value

    def get_values(self):
        return self.values.values()


        