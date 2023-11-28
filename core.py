import re
import typing
from pathlib import Path

import json

ABBREVIATIONS = {
    'Genesis': 'Gen',
    'Exodus': 'Ex',
    'Leviticus': 'Lev',
    'Numbers': 'Num',
    'Deuteronomy': 'Dtn',
    'Joshua': 'Jos',
    'Judges': 'Jdg',
    'Ruth': 'Ruth',
    'I_Samuel': '1Sam',
    'II_Samuel': '2Sam',
    'I_Kings': '1Kgs',
    'II_Kings': '2Kgs',
    'I_Chronicles': '1Chr',
    'II_Chronicles': '2Chr',
    'Ezra': 'Ezr',
    'Nehemiah': 'Neh',
    'Esther': 'Est',
    'Job': 'Job',
    'Psalms': 'Ps',
    'Proverbs': 'Prov',
    'Ecclesiastes': 'Ecc',
    'Song_of_Solomon': 'Song',
    'Isaiah': 'Is',
    'Jeremiah': 'Jer',
    'Lamentations': 'Lam',
    'Ezekiel': 'Ez',
    'Daniel': 'Dan',
    'Hosea': 'Hos',
    'Joel': 'Jo',
    'Amos': 'Am',
    'Obadiah': 'Ob',
    'Jonah': 'Jon',
    'Micah': 'Mi',
    'Nahum': 'Nah',
    'Habakkuk': 'Hab',
    'Zephaniah': 'Zeph',
    'Haggai': 'Hag',
    'Zechariah': 'Zech',
    'Malachi': 'Mal',
    'Matthew': 'Mt',
    'Mark': 'Mk',
    'Luke': 'Lk',
    'John': 'Jn',
    'Acts': 'Acts',
    'Romans': 'Rom',
    'I_Corinthians': '1Cor',
    'II_Corinthians': '2Cor',
    'Galatians': 'Gal',
    'Ephesians': 'Eph',
    'Philippians': 'Phil',
    'Colossians': 'Col',
    'I_Thessalonians': '1Thess',
    'II_Thessalonians': '2Thess',
    'I_Timothy': '1Tim',
    'II_Timothy': '2Tim',
    'Titus': 'Tit',
    'Philemon': 'Phil',
    'Hebrews': 'Hebr',
    'James': 'Jm',
    'I_Peter': '1Pt',
    'II_Peter': '2Pt',
    'I_John': '1Jn',
    'II_John': '2Jn',
    'III_John': '3Jn',
    'Jude': 'Jud',
    'Revelation_of_John': 'Rev',
}


class IndexMixin:
    # noinspection PyUnresolvedReferences
    @property
    def number(self):
        return f'{(self.index + 1):02d}'


class Bible:
    def __init__(self, books):
        self.books = books

    def __iter__(self):
        return iter(self.books)

    @classmethod
    def from_json(cls, path=Path('json/ESV.json')):
        with open(path) as file:
            books = [
                Book(index, title, chunks)
                for index, (title, chunks)
                in enumerate(json.load(file)["books"].items())
            ]

            return cls(books)


class Book(IndexMixin):
    def __init__(self, index, title, chunks):
        self.index = index
        self.title = title
        self.chunks = chunks

    def __iter__(self):
        """Enumerate chapters of this book."""
        return iter(self.chapters)

    def __str__(self):
        return f'{self.number} {self.title} ({self.abbreviation})'

    @property
    def safe_title(self):
        """Title of the book, but spaces are replaced by underscores.

        Safe for file or dictionary names or
        for building key lookups, i.e. abbreviations.
        """
        return self.title.replace(' ', '_')

    @property
    def abbreviation(self):
        """Abbreviation for this book."""
        return ABBREVIATIONS[self.safe_title]

    @property
    def chapters(self):
        """Chapters of this book."""
        return [
            Chapter(index, chunks)
            for index, chunks
            in enumerate(self.chunks)
        ]


class Chapter(IndexMixin):
    def __init__(self, index, chunks):
        self.index = index
        self.chunks = chunks

    def __iter__(self):
        return iter(self.verses)

    def __str__(self):
        return f'Chapter {self.number}'

    @property
    def verses(self) -> typing.Generator:
        for index, _ in enumerate(self.chunks):
            chunks = self.chunks[index]
            text = " ".join([chunk[0]
                             for chunk in chunks if not isinstance(chunk[0], list)])
            text = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', text)

            yield Verse(index, text)


class Verse(IndexMixin):
    def __init__(self, index, text):
        self.index = index
        self.text = text

    def __str__(self):
        return f'{self.number} {self.text}'


if __name__ == '__main__':
    for book in Bible.from_json():
        print(book)

        for chapter in book:
            print('\t', chapter)

            for verse in chapter:
                print('\t\t', verse)
