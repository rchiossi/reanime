import argparse
import os

from typing import Optional
from fuzzywuzzy import fuzz


class Anime:
    def __init__(self, title: str, source: str):
        self.title = title
        self.source = source

        self.clean = Anime.strip_annotations(self.title)

    @property
    def path(self) -> str:
        return f'{self.source}/{self.title}'

    @staticmethod
    def __strip_annotation(title: str, marker_start: str, marker_end: Optional[str] = None) -> str:
        start = title.find(marker_start)
        end = title.find(marker_end) if marker_end else None

        while start != -1:
            if end is not None and end == -1:
                break

            if end:
                title = f'{title[:start]}{title[end+1:]}'
            else:
                title = f'{title[:start]}'

            start = title.find(marker_start)
            end = title.find(marker_end) if marker_end else None

        return title

    @staticmethod
    def strip_annotations(title: str) -> str:
        title = Anime.__strip_annotation(title, '[', ']')
        title = Anime.__strip_annotation(title, '{', '}')
        title = Anime.__strip_annotation(title, '(', ')')
        title = Anime.__strip_annotation(title, ' 720p ')
        title = Anime.__strip_annotation(title, ' 1080p ')
        title = Anime.__strip_annotation(title, ' BD ')
        title = Anime.__strip_annotation(title, ' BDRip ')
        title = Anime.__strip_annotation(title, ' WEBRip ')
        title = Anime.__strip_annotation(title, ' 720 ')
        title = Anime.__strip_annotation(title, ' 1080 ')
        title = Anime.__strip_annotation(title, ' (720) ')
        title = Anime.__strip_annotation(title, ' (1080) ')

        return title.strip()


class AnimeCollection:
    def __init__(self, source: str):
        self.source = source
        self.anime_list = list()
        self.mapping = dict()

        self.__init_anime_list()

    def refresh_mapping(self):
        self.mapping = dict()
        self.__map_clean_title()

    def __get_directory_list(self) -> list:
        return [d for d in os.listdir(self.source) if os.path.isdir(f'{self.source}/{d}')]

    def __init_anime_list(self):
        titles = self.__get_directory_list()
        for title in titles:
            self.anime_list.append(Anime(title, self.source))

    def __map_clean_title(self):
        for anime in self.anime_list:
            if anime.clean in self.mapping.keys():
                self.mapping[anime.clean].append(anime.title)
            else:
                self.mapping[anime.clean] = [anime.title]

    def find_duplicates(self) -> list:
        duplicates = list()
        for clean, title_list in self.mapping.items():
            if len(title_list) != 1:
                duplicates.append(clean)

        return duplicates

    def __find_similar_key(self, target: Anime) -> str:
        similar_key = target.clean

        for anime in self.anime_list:
            if anime.title == target.title:
                continue

            ratio = fuzz.partial_ratio(target.clean, anime.clean)

            if ratio == 100:
                # print((target.clean, anime.clean))
                similar_key = min(similar_key, anime.clean)

        return similar_key

    def find_similars(self) -> dict:
        similars = dict()

        for anime in self.anime_list:
            key = self.__find_similar_key(anime)

            if key in similars.keys():
                similars[key].append(anime)
            else:
                similars[key] = [anime]

        return similars


def main():
    parser = argparse.ArgumentParser(description="Rename and move anime")
    parser.add_argument("--source", '-s', type=str, required=True)
    # parser.add_argument("--dst", '-d', type=str, required=True)
    # parser.add_argument("--dry-run", action='store_true', required=False)

    args = parser.parse_args()

    collection = AnimeCollection(args.source)
    collection.refresh_mapping()

    duplicates = collection.find_duplicates()

    print("Duplicates -------")

    for duplicate in duplicates:
        print(f'{duplicate}:')
        for item in collection.mapping[duplicate]:
            print(f'  {item}')
    print()

    print("Similar ----------")
    similars = collection.find_similars()
    for key, val in similars.items():
        if len(val) == 1:
            continue

        print(f'{key}:')
        for item in val:
            print(f'  {item.title}')
    print()


if __name__ == "__main__":
    main()
