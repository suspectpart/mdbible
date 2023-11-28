import io
from pathlib import Path

from scripture import BibleWriter, Bible, Chapter


def by_chapter(chapter: Chapter, writer: BibleWriter):
    # One directory per book, one file per chapter
    book_dir = Path(f'{chapter.book.number}_{chapter.book.safe_title}')
    chapter_file = book_dir / Path(f'Chapter_{chapter.number}.md')

    # create contents of verse file
    buffer = io.StringIO()
    buffer.write(f'# Chapter {chapter.index + 1}\n\n')

    for verse in chapter:
        buffer.write(f'{verse.index + 1}. {verse.text}\n')

    # write directories and files
    writer.create_directory(book_dir)
    writer.create_file(chapter_file, buffer.getvalue())


if __name__ == '__main__':
    BibleWriter(
        Bible.from_json(),
        chapter_hook=by_chapter,
        output_directory=Path('by_chapter'),
    ).run()
