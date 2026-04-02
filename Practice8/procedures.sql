-- PROCEDURE 1: Insert or Update user

-- PROCEDURE:
-- Unlike FUNCTION, it does NOT return a value
-- It is used for performing actions (INSERT, UPDATE, DELETE)
CREATE OR REPLACE PROCEDURE insert_or_update_user(u_name TEXT, u_phone TEXT)

LANGUAGE plpgsql

AS $$
BEGIN

    -- IF EXISTS:
    -- Checks if a record already exists in the table
    IF EXISTS (SELECT 1 FROM contacts WHERE name = u_name) THEN

        -- If user exists → update their phone number
        UPDATE contacts
        SET phone = u_phone
        WHERE name = u_name;

    ELSE

        -- If user does not exist → insert new record
        INSERT INTO contacts(name, phone)
        VALUES (u_name, u_phone);

    END IF;

END;
$$;


-- PROCEDURE 2: Insert multiple users

-- names[] and phones[] are arrays
CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])

LANGUAGE plpgsql

AS $$
DECLARE
    -- i is a loop counter variable
    i INT;
BEGIN

    -- Loop through array indexes (from 1 to array length)
    FOR i IN 1..array_length(names, 1)

    LOOP

        -- Validation:
        -- ~ is a regex operator
        -- '^[0-9]+$' means only digits allowed
        IF phones[i] ~ '^[0-9]+$' THEN

            -- If valid → insert into table
            INSERT INTO contacts(name, phone)
            VALUES (names[i], phones[i]);

        ELSE

            -- If invalid → show message
            RAISE NOTICE 'Invalid phone: %', phones[i];

        END IF;

    END LOOP;

END;
$$;


-- PROCEDURE 3: Delete user

CREATE OR REPLACE PROCEDURE delete_user(value TEXT)

LANGUAGE plpgsql

AS $$
BEGIN

    -- DELETE:
    -- Removes records from the table
    DELETE FROM contacts

    -- Deletes by either name OR phone
    WHERE name = value
       OR phone = value;

END;
$$;

-- PROCEDURE 3: Insert many users with validation

-- This procedure inserts multiple users from arrays
-- names[] → array of names
-- phones[] → array of phone numbers
CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;  -- loop counter
BEGIN

    -- LOOP through all elements of arrays
    FOR i IN 1..array_length(names, 1)
    LOOP

        -- IF condition:
        -- Validate phone number (only digits allowed)
        IF phones[i] ~ '^[0-9]+$' THEN

            -- Insert user into table
            INSERT INTO contacts(name, phone)
            VALUES(names[i], phones[i])

            -- ON CONFLICT:
            -- Avoid duplicates (if constraint exists)
            ON CONFLICT DO NOTHING;

        ELSE
            -- If phone is invalid → show message
            RAISE NOTICE 'Invalid phone: %', phones[i];
        END IF;

    END LOOP;

END;
$$;