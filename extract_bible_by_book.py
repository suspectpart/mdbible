import io
from pathlib import Path

from scripture import BibleWriter, Book, Bible


def by_book(book: Book, writer: BibleWriter):
    book_file = f'{book.number}_{book.safe_title}.md'

    content = io.StringIO()
    content.write(f'# {book.title}\n\n')

    for chapter in book:
        content.write(f'## Chapter {chapter.index + 1}\n\n')

        for verse in chapter:
            content.write(f'{verse.index + 1}. {verse.text}\n')

        content.write('\n')

    writer.create_file(book_file, content.getvalue())


if __name__ == '__main__':
    BibleWriter(
        Bible.from_json(),
        book_hook=by_book,
        output_directory=Path('by_book'),
    ).run()
