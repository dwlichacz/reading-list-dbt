"""
Generate mock seed data for the reading-list dbt project.

The output mimics a hand-kept reading log exported from a spreadsheet or app,
including the kind of messiness real exports have:
  - inconsistent casing and stray whitespace
  - two different date formats
  - ratings stored as "4", "4/5", or blank
  - several spellings of the same book format ("audio" vs "Audiobook")
  - rereads (the same book logged more than once)

Run from the project root:
    python scripts/generate_mock_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
START = date(2022, 1, 3)
END = date(2026, 9, 15)
SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds"

# title, author, genres (pipe-delimited), approx page count, first published
BOOKS = [
    ("Project Hail Mary", "Andy Weir", "Science Fiction", 476, 2021),
    ("The Martian", "Andy Weir", "Science Fiction", 369, 2011),
    ("Dune", "Frank Herbert", "Science Fiction|Classics", 612, 1965),
    ("Neuromancer", "William Gibson", "Science Fiction|Cyberpunk", 271, 1984),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", "Science Fiction|Classics", 304, 1969),
    ("Children of Time", "Adrian Tchaikovsky", "Science Fiction", 600, 2015),
    ("Recursion", "Blake Crouch", "Science Fiction|Thriller", 326, 2019),
    ("Dark Matter", "Blake Crouch", "Science Fiction|Thriller", 342, 2016),
    ("Station Eleven", "Emily St. John Mandel", "Literary Fiction|Science Fiction", 333, 2014),
    ("Klara and the Sun", "Kazuo Ishiguro", "Literary Fiction|Science Fiction", 303, 2021),
    ("Never Let Me Go", "Kazuo Ishiguro", "Literary Fiction", 288, 2005),
    ("The Remains of the Day", "Kazuo Ishiguro", "Literary Fiction|Classics", 245, 1989),
    ("Tomorrow, and Tomorrow, and Tomorrow", "Gabrielle Zevin", "Literary Fiction", 401, 2022),
    ("The Name of the Wind", "Patrick Rothfuss", "Fantasy", 662, 2007),
    ("Mistborn: The Final Empire", "Brandon Sanderson", "Fantasy", 541, 2006),
    ("The Way of Kings", "Brandon Sanderson", "Fantasy", 1007, 2010),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy|Classics", 310, 1937),
    ("A Wizard of Earthsea", "Ursula K. Le Guin", "Fantasy|Classics", 183, 1968),
    ("The Night Circus", "Erin Morgenstern", "Fantasy", 387, 2011),
    ("Gone Girl", "Gillian Flynn", "Thriller|Mystery", 415, 2012),
    ("The Silent Patient", "Alex Michaelides", "Thriller|Mystery", 336, 2019),
    ("Big Little Lies", "Liane Moriarty", "Mystery", 460, 2014),
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", "Thriller|Mystery", 465, 2005),
    ("And Then There Were None", "Agatha Christie", "Mystery|Classics", 272, 1939),
    ("1984", "George Orwell", "Classics|Science Fiction", 328, 1949),
    ("Brave New World", "Aldous Huxley", "Classics|Science Fiction", 268, 1932),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Classics", 180, 1925),
    ("Of Mice and Men", "John Steinbeck", "Classics", 107, 1937),
    ("Thinking, Fast and Slow", "Daniel Kahneman", "Nonfiction|Psychology", 499, 2011),
    ("Sapiens", "Yuval Noah Harari", "Nonfiction|History", 443, 2011),
    ("Atomic Habits", "James Clear", "Nonfiction|Self Help", 320, 2018),
    ("Deep Work", "Cal Newport", "Nonfiction|Productivity", 296, 2016),
    ("The Signal and the Noise", "Nate Silver", "Nonfiction|Data", 534, 2012),
    ("Storytelling with Data", "Cole Nussbaumer Knaflic", "Nonfiction|Data", 288, 2015),
    ("Weapons of Math Destruction", "Cathy O'Neil", "Nonfiction|Data", 272, 2016),
    ("How to Lie with Statistics", "Darrell Huff", "Nonfiction|Data|Classics", 142, 1954),
    ("Naked Statistics", "Charles Wheelan", "Nonfiction|Data", 282, 2013),
    ("Designing Data-Intensive Applications", "Martin Kleppmann", "Nonfiction|Technology", 616, 2017),
    ("The Pragmatic Programmer", "David Thomas", "Nonfiction|Technology", 352, 1999),
    ("Clean Code", "Robert C. Martin", "Nonfiction|Technology", 464, 2008),
    ("The Phoenix Project", "Gene Kim", "Fiction|Technology", 345, 2013),
    ("Blood, Sweat, and Pixels", "Jason Schreier", "Nonfiction|Video Games", 304, 2017),
    ("Masters of Doom", "David Kushner", "Nonfiction|Video Games|Biography", 335, 2003),
    ("Press Reset", "Jason Schreier", "Nonfiction|Video Games", 304, 2021),
    ("Ready Player One", "Ernest Cline", "Science Fiction|Video Games", 374, 2011),
    ("Shoe Dog", "Phil Knight", "Nonfiction|Biography|Business", 386, 2016),
    ("Steve Jobs", "Walter Isaacson", "Nonfiction|Biography", 656, 2011),
    ("The Big Short", "Michael Lewis", "Nonfiction|Business", 266, 2010),
    ("Moneyball", "Michael Lewis", "Nonfiction|Sports|Data", 288, 2003),
    ("Freakonomics", "Steven D. Levitt", "Nonfiction|Economics", 268, 2005),
    ("Educated", "Tara Westover", "Nonfiction|Memoir", 334, 2018),
    ("Born a Crime", "Trevor Noah", "Nonfiction|Memoir", 288, 2016),
    ("The Body Keeps the Score", "Bessel van der Kolk", "Nonfiction|Psychology", 464, 2014),
    ("Into Thin Air", "Jon Krakauer", "Nonfiction|Adventure", 333, 1997),
    ("The Road", "Cormac McCarthy", "Literary Fiction", 287, 2006),
    ("Life of Pi", "Yann Martel", "Literary Fiction|Adventure", 319, 2001),
    ("The Handmaid's Tale", "Margaret Atwood", "Literary Fiction|Classics", 311, 1985),
    ("Circe", "Madeline Miller", "Fantasy|Mythology", 393, 2018),
    ("The Song of Achilles", "Madeline Miller", "Fantasy|Mythology", 378, 2011),
    ("Mythos", "Stephen Fry", "Nonfiction|Mythology", 416, 2017),
    ("Hyperion", "Dan Simmons", "Science Fiction|Classics", 482, 1989),
    ("Foundation", "Isaac Asimov", "Science Fiction|Classics", 255, 1951),
    ("The Three-Body Problem", "Liu Cixin", "Science Fiction", 400, 2008),
    ("Piranesi", "Susanna Clarke", "Fantasy|Literary Fiction", 272, 2020),
    ("The Fifth Season", "N.K. Jemisin", "Fantasy|Science Fiction", 468, 2015),
    ("Rebecca", "Daphne du Maurier", "Mystery|Classics", 449, 1938),
    ("Range", "David Epstein", "Nonfiction|Psychology", 339, 2019),
    ("The Undoing Project", "Michael Lewis", "Nonfiction|Psychology|Biography", 362, 2016),
    ("Algorithms to Live By", "Brian Christian", "Nonfiction|Data", 368, 2016),
    ("The Art of Game Design", "Jesse Schell", "Nonfiction|Video Games", 600, 2008),
]

# Canonical format -> the messy spellings that show up in the raw export
FORMAT_SPELLINGS = {
    "hardcover": ["Hardcover", "hardcover", "HC", "Hardback"],
    "paperback": ["Paperback", "paperback", "PB", "soft cover"],
    "ebook": ["Kindle", "ebook", "E-book", "kindle "],
    "audiobook": ["Audiobook", "audio", "Audible", " audiobook"],
}

STATUS_SPELLINGS = {
    "finished": ["Finished", "finished", "READ", "Read", "done"],
    "reading": ["Reading", "currently reading", "IN PROGRESS"],
    "dnf": ["DNF", "dnf", "Did Not Finish", "abandoned"],
}


def messy(text: str, rng: random.Random) -> str:
    """Occasionally add stray whitespace, like a hand-typed spreadsheet."""
    roll = rng.random()
    if roll < 0.08:
        return f" {text}"
    if roll < 0.15:
        return f"{text}  "
    return text


def fmt_date(d: date, rng: random.Random) -> str:
    """Mix ISO dates with North American MM/DD/YYYY, as imports often do."""
    return d.strftime("%m/%d/%Y") if rng.random() < 0.3 else d.isoformat()


def fmt_rating(r: int | None, rng: random.Random) -> str:
    if r is None:
        return ""
    return f"{r}/5" if rng.random() < 0.35 else str(r)


def pages_per_day(fmt: str, rng: random.Random) -> float:
    base = {"hardcover": 32, "paperback": 35, "ebook": 40, "audiobook": 55}[fmt]
    return max(8.0, rng.gauss(base, 12))


def main() -> None:
    rng = random.Random(SEED)
    SEEDS_DIR.mkdir(exist_ok=True)

    # ---------- books ----------
    book_rows = []
    for i, (title, author, genres, pages, year) in enumerate(BOOKS, start=1):
        # Genres in the raw export are inconsistently cased
        genre_str = "|".join(
            g.lower() if rng.random() < 0.2 else g for g in genres.split("|")
        )
        book_rows.append(
            {
                "book_id": i,
                "title": messy(title, rng),
                "author": messy(author, rng),
                "genres": genre_str,
                # A few books are missing page counts, as real exports are
                "page_count": "" if rng.random() < 0.05 else pages,
                "year_published": year,
            }
        )

    # ---------- reading log ----------
    # Walk forward in time; roughly one book on the go at any point, with
    # occasional overlap and a handful of rereads.
    log_rows = []
    cursor = START
    order = list(range(1, len(BOOKS) + 1))
    rng.shuffle(order)
    reread_pool: list[int] = []
    entry_id = 1

    while cursor < END and (order or reread_pool):
        if reread_pool and rng.random() < 0.12:
            book_id = reread_pool.pop(rng.randrange(len(reread_pool)))
        elif order:
            book_id = order.pop()
        else:
            break

        pages = BOOKS[book_id - 1][3]
        fmt = rng.choices(
            ["hardcover", "paperback", "ebook", "audiobook"],
            weights=[2, 3, 3, 2],
        )[0]
        start = cursor + timedelta(days=rng.randint(0, 12))

        roll = rng.random()
        status = "dnf" if roll < 0.08 else "finished"
        if status == "finished":
            days = max(1, round(pages / pages_per_day(fmt, rng)))
            finish = start + timedelta(days=days)
            if finish > END:
                status, finish = "reading", None
            # Ratings skew positive (people finish books they like)
            rating = rng.choices([2, 3, 4, 5], weights=[1, 3, 5, 3])[0]
            if rng.random() < 0.1:
                rating = None  # finished but never rated
        else:
            finish = start + timedelta(days=rng.randint(5, 25))  # date abandoned
            rating = rng.choice([1, 2, None])

        if status == "reading":
            rating = None

        log_rows.append(
            {
                "entry_id": entry_id,
                "book_id": book_id,
                "status": messy(rng.choice(STATUS_SPELLINGS[status]), rng),
                "date_started": fmt_date(start, rng),
                "date_finished": fmt_date(finish, rng) if finish else "",
                "rating": fmt_rating(rating, rng),
                "format": rng.choice(FORMAT_SPELLINGS[fmt]),
            }
        )
        entry_id += 1

        if status == "finished" and rating and rating >= 4 and rng.random() < 0.3:
            reread_pool.append(book_id)

        # Next book starts a bit after this one ends (or overlaps slightly)
        end_point = finish or start
        cursor = end_point + timedelta(days=rng.randint(-3, 18))

    # Whatever is on the nightstand right now: one in-progress book
    if order:
        log_rows.append(
            {
                "entry_id": entry_id,
                "book_id": order.pop(),
                "status": rng.choice(STATUS_SPELLINGS["reading"]),
                "date_started": fmt_date(END - timedelta(days=4), rng),
                "date_finished": "",
                "rating": "",
                "format": rng.choice(FORMAT_SPELLINGS["ebook"]),
            }
        )

    with open(SEEDS_DIR / "raw_books.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=book_rows[0].keys(), lineterminator="\n")
        w.writeheader()
        w.writerows(book_rows)

    with open(SEEDS_DIR / "raw_reading_log.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=log_rows[0].keys(), lineterminator="\n")
        w.writeheader()
        w.writerows(log_rows)

    print(f"Wrote {len(book_rows)} books and {len(log_rows)} reading log entries")


if __name__ == "__main__":
    main()
