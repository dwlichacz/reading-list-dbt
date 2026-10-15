{# DuckDB has no INITCAP(), so this builds one: "science FICTION" -> "Science Fiction" #}

{% macro title_case(column_name) %}
    array_to_string(
        list_transform(
            string_split(trim(lower({{ column_name }})), ' '),
            lambda w: upper(w[1]) || w[2:]
        ),
        ' '
    )
{% endmacro %}