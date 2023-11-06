

class Scenario:
    def __init__(self, name: str, number: int, introduction: Choice):
        self.__name = name
        self.__number = number
        self.__introduction = introduction

    @property
    def name(self) -> str:
        return self.__name

    @property
    def number(self) -> int:
        return self.__number

    @property
    def introduction(self) -> Choice:
        return self.__introduction


class Choice:
    def __init__(self, number: int, lib: str, text: str, choices: list[Choice]):
        self.__number = number
        self.__lib = lib
        self.__text = text
        self.__choices = choices

    @property
    def number(self) -> int:
        return self.__number

    @property
    def lib(self) -> str:
        return self.__lib

    @property
    def text(self) -> str:
        return self.__text

    @property
    def choices(self) -> list[Choice]:
        return self.__choices

    def __str__(self) -> str:
        result = self.text + '\n'
        for choice in self.choices:
            result += f"{choice.number}. {choice.lib}\n"
        return result

    def isfinal(self) -> bool:
        return not len(self.choices)

