from abc import abstractmethod, ABC
from typing import TypeVar, Callable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.psql.connect import Base


class KeyboardsMarkup(ABC):
    @abstractmethod
    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        raise NotImplementedError


class ListKeyboardMarkup(KeyboardsMarkup):
    E = TypeVar('E', bound=Base)

    def __init__(self, list_types: list[E], key_func: Callable[[E], str], val_func: Callable[[E], str],
                 callback_prefix: str, is_back: bool, back_index: int, delimiter: int = 3):
        self.delimiter = delimiter
        self.callback_prefix = callback_prefix
        self.list_types = list_types
        self.key_func = key_func
        self.val_func = val_func
        self.back_index = back_index
        self.is_back = is_back

    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        keyboard_builder = InlineKeyboardBuilder()
        for pt in self.list_types:
            keyboard_builder.button(
                text=self.key_func(pt),
                callback_data=f"{self.callback_prefix}{self.val_func(pt)}"
            )
        keyboard_builder.adjust(self.delimiter)
        if self.is_back:
            back_button = InlineKeyboardButton(
                text="Назад",
                callback_data=f"back_{self.back_index}"
            )
            keyboard_builder.row(back_button)
        return keyboard_builder.as_markup()
