from pathlib import Path

from scripture import Bible, Verse, BibleWriter


def one_file_per_verse(verse: Verse, writer: BibleWriter):
    book = verse.chapter.book
    chapter = verse.chapter

    # One directory per book and chapter
    book_dir = Path(f'{book.number}_{book.abbreviation}')
    chapter_dir = book_dir / f'Chapter_{chapter.number}'

    # One file per verse
    verse_file = f'{book.abbreviation}{chapter.number}-{verse.number}.md'

    # Create directory structure and verse files
    writer.create_directory(chapter_dir)
    writer.create_file(chapter_dir / verse_file, verse.text)


if __name__ == '__main__':
    BibleWriter(
        Bible.from_json(),
        verse_hook=one_file_per_verse,
        output_directory='by_verse',
    ).run()
