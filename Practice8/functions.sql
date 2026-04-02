-- FUNCTION 1: Search contacts by pattern

-- CREATE OR REPLACE FUNCTION:
-- Creates a new function or replaces it if it already exists
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)

-- RETURNS TABLE:
-- This function returns a table (like SELECT result)
-- We explicitly define column names and types
RETURNS TABLE(id INT, name TEXT, phone TEXT)

-- AS $$ ... $$:
-- This is the body of the function written in PL/pgSQL
AS $$
BEGIN

    -- RETURN QUERY:
    -- Executes a query and returns its result as the function output
    RETURN QUERY

    -- SELECT DISTINCT:
    -- Removes duplicate rows from the result
    SELECT DISTINCT
        c.id,

        -- ::TEXT:
        -- Explicit type casting from VARCHAR to TEXT
        -- Required to match RETURNS TABLE definition
        c.name::TEXT,
        c.phone::TEXT

    -- FROM clause:
    -- "c" is an alias for the contacts table
    FROM contacts c

    -- WHERE clause:
    -- Filters records based on search pattern
    WHERE 
        -- ILIKE:
        -- Case-insensitive search (e.g., "John" = "john")
        -- '%' means "any characters"
        -- || is string concatenation in PostgreSQL
        c.name ILIKE '%' || pattern || '%'
        OR
        c.phone ILIKE '%' || pattern || '%'

    -- ORDER BY:
    -- Sort results by id in ascending order
    ORDER BY c.id;

END;

-- LANGUAGE plpgsql:
-- Specifies that we are using PostgreSQL procedural language
$$ LANGUAGE plpgsql;


-- FUNCTION 2: Pagination (LIMIT + OFFSET)


-- lim → number of rows to return
-- off → number of rows to skip
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)

-- RETURNS TABLE:
-- Function returns a table structure with fixed columns
RETURNS TABLE(id INT, name TEXT, phone TEXT)

-- AS $$ ... $$:
-- Function body starts here
AS $$
BEGIN

    -- RETURN QUERY:
    -- Executes the SELECT query and returns result
    RETURN QUERY

    -- SELECT specific columns (not *)
    -- Important: casting to TEXT to match return type
    SELECT 
        c.id,
        c.name::TEXT,
        c.phone::TEXT

    -- FROM clause with alias
    FROM contacts c

    -- ORDER BY:
    -- Ensures consistent ordering before pagination
    ORDER BY c.id

    -- LIMIT:
    -- Restricts number of rows returned
    LIMIT lim

    -- OFFSET:
    -- Skips first N rows (used for pagination)
    OFFSET off;

END;

-- LANGUAGE plpgsql:
-- Specifies procedural language used
$$ LANGUAGE plpgsql;