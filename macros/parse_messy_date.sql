{# Checks for dates in ISO format and US format and keeps whatever works; null if neither works #}
{# Ultimately, converts all to date format.  Assumes 03/05/2026 is March 5. #}

{% macro parse_messy_date(column_name) -%}
    coalesce(
        try_strptime(trim({{ column_name }}), '%Y-%m-%d'),
        try_strptime(trim({{ column_name }}), '%m/%d/%Y')
    )::date
{%- endmacro %}