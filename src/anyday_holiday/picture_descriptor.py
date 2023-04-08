from random import choice


class PictureDescriptorGenerator:
    nice_attributes: list[str] = [
        "sunny",
        "funny",
        "joyable",
        "pretty",
        "handsome",
        "lazy",
        "colorful",
        "fluffy",
    ]
    nice_actions: list[str] = [
        "play",
        "joke",
        "swim",
        "fly",
        "ride",
        "do art",
        "work",
        "play music",
    ]
    nice_creatures: list[str] = [
        "cats",
        "dogs",
        "deers",
        "kittens",
        "puppies",
    ]

    def __call__(self) -> str:
        attribute = choice(self.nice_attributes)
        action = choice(self.nice_actions)
        creatures = choice(self.nice_creatures)
        return f"{attribute} {creatures} {action}"
