from telegram.ext.filters import MessageFilter


class MakePictureFilter(MessageFilter):
    list_of_triggers = [
        "картинка, где",
        "картинка где",
        "бот дай картинку, где",
        "бот дай картинку где",
        "хочу картинку где",
        "хочу картинку, где",
    ]

    def filter(self, message):
        return any([message.text.lower().startswith(expression) for expression in self.list_of_triggers])

    @classmethod
    def len_trigger(cls, text: str) -> int:  # type: ignore
        for trigger in cls.list_of_triggers:
            if text.lower().startswith(trigger):
                return len(trigger) + 1


class AskQuestionFilter(MessageFilter):
    list_of_nice = [
        "бот есть вопрос",
        "бот ответь",
        "бот как думаешь",
        "бот скажи",
        "бот напиши",
    ]
    list_of_toxic = [
        "э слыш",
        "слыш бот ответь",
        "слыш есть вопрос",
        "слыш скажи",
        "слыш ответь",
    ]

    def filter(self, message):
        return any([message.text.lower().startswith(expression) for expression in self.get_list_of_triggers()])

    @classmethod
    def get_list_of_triggers(self) -> list[str]:
        return [*self.list_of_toxic, *self.list_of_nice]

    @classmethod
    def len_trigger(cls, text: str) -> int:  # type: ignore
        for trigger in cls.get_list_of_triggers():
            if text.lower().startswith(trigger):
                return len(trigger) + 1

    @classmethod
    def is_toxic(cls, text: str) -> bool:
        for trigger in cls.list_of_toxic:
            if text.lower().startswith(trigger):
                return True
        return False


make_picture_filter = MakePictureFilter()
ask_question_filter = AskQuestionFilter()
