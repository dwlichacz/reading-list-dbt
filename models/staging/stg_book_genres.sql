-- One row per book per genre

WITH books AS (
    SELECT book_id, genres FROM {{ ref('stg_books') }}
),

split AS (
    SELECT
        book_id,
        UNNEST(STRING_SPLIT(genres, '|')) AS split_genre
    FROM books
),

cleaned AS (
    SELECT DISTINCT
        book_id,
        {{ title_case('split_genre') }} AS genre
    FROM split
)

SELECT book_id, genre,
       CAST(book_id AS STRING) || '-' || REPLACE(LOWER(genre), ' ', '-') AS book_genre_id
FROM cleaned
WHERE genre != ''
