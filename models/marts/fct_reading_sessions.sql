-- Fact table: one row per reading attempt, with book details and time to finish.

with sessions as (

    select * from {{ ref('stg_reading_log') }}

),

books as (

    select book_id, title, author, page_count from {{ ref('stg_books') }}

)

select
    s.entry_id,
    s.book_id,
    b.title,
    b.author,
    s.status,
    s.book_format,
    s.started_on,
    s.ended_on,
    s.rating,

    -- Inclusive day count: starting and finishing on the same day = 1 day
    case
        when s.status = 'finished'
            then date_diff('day', s.started_on, s.ended_on) + 1
    end as days_to_finish,

    case when s.status = 'finished' then b.page_count end as pages_read

from sessions s
inner join books b on s.book_id = b.book_id
