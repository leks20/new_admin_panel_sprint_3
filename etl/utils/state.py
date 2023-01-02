import abc
import json
from datetime import datetime
from typing import Any


def json_serial(obj: Any) -> Any:
    if isinstance(obj, (datetime)):
        return obj.isoformat()


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_state(self, new_state: dict[str, Any]) -> None:
        state = self.retrieve_state()
        state.update(new_state)
        with open(self.file_path, "w") as outfile:
            json.dump(state, outfile, default=json_serial)

    def retrieve_state(self) -> dict[str, Any]:
        try:
            with open(self.file_path, "r") as openfile:
                return json.load(openfile)

        except json.decoder.JSONDecodeError:
            return {}


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.data: dict[str, Any] = {}

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.data[key] = value
        self.storage.save_state(self.data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        self.data = self.storage.retrieve_state()

        if self.data:
            return self.data.get(key)


def start_state() -> State:
    storage = JsonFileStorage("./state.json")
    state = State(storage)

    if not state.get_state("person_modified"):
        state.set_state("person_modified", datetime.min)

    if not state.get_state("filmwork_modified"):
        state.set_state("filmwork_modified", datetime.min)

    return state
