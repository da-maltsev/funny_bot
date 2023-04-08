from telegram.ext.filters import MessageFilter


class MakePictureFilter(MessageFilter):
    list_of_triggers = [
        "Картинка, где",
        "Картинка где",
        "Бот дай картинку, где",
        "Бот дай картинку где",
        "Хочу картинку где",
        "Хочу картинку, где",
    ]

    def filter(self, message):
        return any([message.text.startswith(expression) for expression in self.list_of_triggers])

    @classmethod
    def len_trigger(cls, text: str) -> int:  # type: ignore
        for trigger in cls.list_of_triggers:
            if text.startswith(trigger):
                return len(trigger) + 1


make_picture_filter = MakePictureFilter()
