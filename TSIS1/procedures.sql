-- Procedure to add a phone number to an existing contact

CREATE OR REPLACE PROCEDURE add_phone(
    p_name TEXT,     -- input parameter: contact name
    p_phone TEXT,    -- input parameter: phone number to add
    p_type TEXT      -- input parameter: phone type (home/work/mobile)
)
LANGUAGE plpgsql   -- specifies that we use PostgreSQL procedural language
AS $$
DECLARE
    v_contact_id INT;  -- variable to store the contact's ID
BEGIN
    -- find contact ID using the provided name
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_name;

    -- check if contact was found
    IF v_contact_id IS NULL THEN
        -- show message if contact does not exist
        RAISE NOTICE 'Contact not found: %', p_name;
    ELSE
        -- insert a new phone number linked to the contact
        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_type);
    END IF;
END;
$$;


-- Procedure to move a contact into another group

CREATE OR REPLACE PROCEDURE move_to_group(
    p_name TEXT,     -- input parameter: contact name
    p_group TEXT     -- input parameter: new group name
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;  -- variable to store group ID
BEGIN
    -- insert group if it does not exist yet
    INSERT INTO groups(name)
    VALUES (p_group)
    ON CONFLICT (name) DO NOTHING;  -- prevents duplicate groups

    -- get group ID by group name
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group;

    -- update contact's group_id to new group
    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_name;

    -- if no rows were updated, contact does not exist
    IF NOT FOUND THEN
        RAISE NOTICE 'Contact not found: %', p_name;
    END IF;
END;
$$;