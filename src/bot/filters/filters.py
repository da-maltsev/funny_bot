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


class AskQuestionFilter(MessageFilter):
    list_of_nice = [
        "Бот есть вопрос",
        "Бот ответь",
        "Бот как думаешь",
        "Бот скажи",
    ]
    list_of_toxic = [
        "Э слыш",
        "Слыш бот ответь",
        "Слыш есть вопрос",
        "Слыш скажи",
        "Слыш ответь",
    ]

    def filter(self, message):
        return any([message.text.startswith(expression) for expression in self.get_list_of_triggers()])

    @classmethod
    def get_list_of_triggers(self) -> list[str]:
        return [*self.list_of_toxic, *self.list_of_nice]

    @classmethod
    def len_trigger(cls, text: str) -> int:  # type: ignore
        for trigger in cls.get_list_of_triggers():
            if text.startswith(trigger):
                return len(trigger) + 1

    @classmethod
    def is_toxic(cls, text: str) -> bool:
        for trigger in cls.list_of_toxic:
            if text.startswith(trigger):
                return True
        return False


make_picture_filter = MakePictureFilter()
ask_question_filter = AskQuestionFilter()
