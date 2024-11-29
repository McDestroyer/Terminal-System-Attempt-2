class BaseObject:
    def __init__(self, name: str, description: str, location: str):
        self.name = name
        self.description = description
        self.location = location

    def __str__(self):
        return f"{self.name} is {self.description} and is located in {self.location}"