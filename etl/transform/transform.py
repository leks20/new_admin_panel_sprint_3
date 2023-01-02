from typing import Any


class DataTransformer:
    def __init__(self) -> None:
        self.result: dict[str, Any] = {}

    def _fill_in_participants(
        self, filmwork_unit: dict[str, Any], data: list[Any]
    ) -> dict[str, Any]:

        role = data[7]
        participant_id = data[8]
        name = data[9]

        if role == "director":
            filmwork_unit["director"].append(name)
        elif role == "writer" and name not in filmwork_unit["writers_names"]:
            filmwork_unit["writers"].append({"id": participant_id, "name": name})
            filmwork_unit["writers_names"].append(name)
        elif role == "actor" and name not in filmwork_unit["actors_names"]:
            filmwork_unit["actors"].append({"id": participant_id, "name": name})
            filmwork_unit["actors_names"].append(name)

        return filmwork_unit

    def _fill_in_genres(
        self, filmwork_unit: dict[str, Any], data: list[Any]
    ) -> dict[str, Any]:

        genre = data[10]

        if genre in filmwork_unit["genre"]:
            return filmwork_unit

        filmwork_unit["genre"].append(genre)
        return filmwork_unit

    def transform_data(self, filmwork_data: list[list[Any]]) -> dict[str, Any]:

        for data in filmwork_data:
            data_id = data[0]

            if filmwork_unit := self.result.get(data_id):
                filmwork_unit = self._fill_in_participants(filmwork_unit, data)
                filmwork_unit = self._fill_in_genres(filmwork_unit, data)

            else:
                filmwork_unit = {}

                filmwork_unit["id"] = data_id
                filmwork_unit["imdb_rating"] = data[3]
                filmwork_unit["title"] = data[1]
                filmwork_unit["genre"] = []
                filmwork_unit["description"] = data[2]
                filmwork_unit["director"] = []
                filmwork_unit["actors_names"] = []
                filmwork_unit["writers_names"] = []
                filmwork_unit["actors"] = []
                filmwork_unit["writers"] = []

                filmwork_unit = self._fill_in_participants(filmwork_unit, data)
                filmwork_unit = self._fill_in_genres(filmwork_unit, data)

            self.result[data_id] = filmwork_unit

        return self.result
