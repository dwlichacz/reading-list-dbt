-- Dimension: one row per book, with a summary of its reading history.
-- Books that were never started still appear here (the to-read backlog).

with books as (

    select * from {{ ref('stg_books') }}

),

history as (

    select
        book_id,
        count(*) filter (where status = 'finished')     as times_finished,
        max(ended_on) filter (where status = 'finished') as last_finished_on,
        round(avg(rating), 2)                            as avg_rating
    from {{ ref('stg_reading_log') }}
    group by book_id

)

select
    b.book_id,
    b.title,
    b.author,
    b.page_count,
    b.year_published,
    b.genres,
    coalesce(h.times_finished, 0) as times_finished,
    h.last_finished_on,
    h.avg_rating

from books b
left join history h on b.book_id = h.book_id
