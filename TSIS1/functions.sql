-- ===============================
-- FUNCTION 1: ADVANCED SEARCH
-- ===============================

-- This function searches contacts by:
-- name, email, or phone number
-- p_query is the input text from the user

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)

-- RETURNS TABLE means the function returns a result set like SELECT
RETURNS TABLE(
    id INT,              -- contact ID
    name TEXT,           -- contact name
    email TEXT,          -- email address
    birthday DATE,       -- date of birth
    group_name TEXT,     -- group name (Friend, Work, etc.)
    phone TEXT,          -- phone number
    type TEXT            -- phone type (mobile/home/work)
)

AS $$

BEGIN
    -- RETURN QUERY executes SELECT and returns its result
    RETURN QUERY

    SELECT
        c.id,                    -- id from contacts table
        c.name::TEXT,            -- contact name (cast to TEXT)
        c.email::TEXT,           -- email
        c.birthday,              -- date of birth
        g.name::TEXT,            -- group name from groups table
        p.phone::TEXT,           -- phone number from phones table
        p.type::TEXT             -- phone type

    FROM contacts c

    -- LEFT JOIN keeps contacts even if they don't have a group
    LEFT JOIN groups g ON c.group_id = g.id

    -- LEFT JOIN keeps contacts even if they don't have phones
    LEFT JOIN phones p ON c.id = p.contact_id

    -- ILIKE is case-insensitive search
    WHERE
        c.name ILIKE '%' || p_query || '%'     -- search by name
        OR c.email ILIKE '%' || p_query || '%' -- search by email
        OR p.phone ILIKE '%' || p_query || '%' -- search by phone

    -- sort results by contact id
    ORDER BY c.id;

END;

-- function is written in PostgreSQL procedural language
$$ LANGUAGE plpgsql;



-- ===============================
-- FUNCTION 2: PAGINATION
-- ===============================

-- This function returns contacts in pages
-- lim = number of records per page
-- off = how many records to skip (offset)

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)

RETURNS TABLE(
    id INT,
    name TEXT,
    email TEXT,
    birthday DATE,
    group_name TEXT,
    phone TEXT,
    type TEXT
)

AS $$

BEGIN
    RETURN QUERY

    SELECT
        c.id,                    -- contact ID
        c.name::TEXT,            -- name
        c.email::TEXT,           -- email
        c.birthday,              -- date of birth
        g.name::TEXT,            -- group name
        p.phone::TEXT,           -- phone number
        p.type::TEXT             -- phone type

    FROM contacts c

    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id

    -- ordering is important for consistent pagination
    ORDER BY c.id

    -- LIMIT defines how many rows to return
    LIMIT lim

    -- OFFSET defines how many rows to skip
    OFFSET off;

END;

$$ LANGUAGE plpgsql;