-- One row per book in the catalogue, typed and trimmed.

with source as (

    select * from {{ ref('raw_books') }}

),

cleaned as (

    select
        cast(book_id as integer)                          as book_id,
        trim(title)                                       as title,
        trim(author)                                      as author,
        try_cast(nullif(trim(page_count), '') as integer) as page_count,
        cast(year_published as integer)                   as year_published,
        trim(genres)                                      as genres

    from source

)

select * from cleaned
