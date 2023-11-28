import re
import shutil
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
    """Add human-readable numbering to mixed-in class."""

    # noinspection PyUnresolvedReferences
    @property
    def number(self):
        return f'{(self.index + 1):02d}'


class Bible:
    """The holy book."""

    def __init__(self, books):
        self.books = books

    def __iter__(self):
        return iter(self.books)

    @classmethod
    def from_json(cls, path=Path('json/ESV.json')):
        """Read book with chapters and verses from JSON file."""
        with open(path) as file:
            books = [
                Book(index, title, chunks)
                for index, (title, chunks)
                in enumerate(json.load(file)["books"].items())
            ]

            return cls(books)


class Book(IndexMixin):
    """A book of the bible."""

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
            Chapter(index, self, chunks)
            for index, chunks
            in enumerate(self.chunks)
        ]


class Chapter(IndexMixin):
    """A chapter of a book."""

    def __init__(self, index, book, chunks):
        self.book = book
        self.index = index
        self.chunks = chunks

    def __iter__(self):
        """Iterate all verses in chapter."""
        return iter(self.verses)

    def __str__(self):
        """Output Chapter with number."""
        return f'Chapter {self.number}'

    @property
    def verses(self) -> typing.Generator:
        for index, _ in enumerate(self.chunks):
            chunks = self.chunks[index]
            text = " ".join([chunk[0]
                             for chunk in chunks if not isinstance(chunk[0], list)])
            text = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', text)

            yield Verse(index, self, text)


class Verse(IndexMixin):
    """A single bible verse."""

    def __init__(self, index, chapter, text):
        self.index = index
        self.chapter = chapter
        self.text = text

    def __str__(self):
        return f'{self.number} {self.text}'


# noinspection PyUnusedLocal
def noop(*args, **kwargs):
    pass


class BibleWriter:
    def __init__(
            self,
            bible,
            book_hook=noop,
            chapter_hook=noop,
            verse_hook=noop,
            output_directory=Path('default'),
    ):
        self.build_dir = Path(__file__).with_name('build') / output_directory
        self.bible = bible
        self.book_hook = book_hook
        self.chapter_hook = chapter_hook
        self.verse_hook = verse_hook

    def _recreate_build_dir(self):
        """Clean and recreate output directory"""
        shutil.rmtree(self.build_dir, ignore_errors=True)
        self.build_dir.mkdir(parents=True)

    def run(self):
        self._recreate_build_dir()

        for book in self.bible:
            self.book_hook(book, self)

            for chapter in book:
                self.chapter_hook(chapter, self)

                for verse in chapter:
                    self.verse_hook(verse, self)

    def create_directory(self, path: Path, parents=True, exist_ok=True):
        """Create directory inside build_dir."""
        return (self.build_dir / path).mkdir(parents=parents, exist_ok=exist_ok)

    def create_file(self, path, content):
        """Create directory with path inside build_dir."""
        with open(self.build_dir / path, 'wt') as file:
            file.write(content)
            file.write('\n')
