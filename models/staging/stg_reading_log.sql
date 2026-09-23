-- One row per reading attempt (a reread is a new row).
-- Normalizes the messy free-text fields from the raw export into clean, typed columns.

with source as (

    select * from {{ ref('raw_reading_log') }}

),

cleaned as (

    select
        cast(entry_id as integer)   as entry_id,
        cast(book_id as integer)    as book_id,

        -- Status: many spellings, three real states
        case
            when lower(trim(status)) in ('finished', 'read', 'done')
                then 'finished'
            when lower(trim(status)) in ('reading', 'currently reading', 'in progress')
                then 'reading'
            when lower(trim(status)) in ('dnf', 'did not finish', 'abandoned')
                then 'dnf'
        end as status,

        -- Dates arrive as either 2024-03-05 or 03/05/2024: try both
        coalesce(
            try_strptime(trim(date_started), '%Y-%m-%d'),
            try_strptime(trim(date_started), '%m/%d/%Y')
        )::date as started_on,

        coalesce(
            try_strptime(trim(date_finished), '%Y-%m-%d'),
            try_strptime(trim(date_finished), '%m/%d/%Y')
        )::date as ended_on,

        -- Rating: "4", "4/5", or blank -> integer or null
        try_cast(
            split_part(nullif(trim(rating), ''), '/', 1) as integer
        ) as rating,

        -- Format: collapse spellings like "HC", "Hardback", "Kindle ", "Audible"
        case
            when lower(trim(format)) in ('hardcover', 'hardback', 'hc')
                then 'hardcover'
            when lower(trim(format)) in ('paperback', 'pb', 'soft cover')
                then 'paperback'
            when lower(trim(format)) in ('kindle', 'ebook', 'e-book')
                then 'ebook'
            when lower(trim(format)) in ('audiobook', 'audio', 'audible')
                then 'audiobook'
        end as book_format

    from source

)

select * from cleaned
