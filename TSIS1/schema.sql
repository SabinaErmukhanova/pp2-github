-- Create table for storing groups (categories of contacts)
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,           -- unique identifier for each group (auto-increment)
    name VARCHAR(50) UNIQUE NOT NULL -- group name must be unique and cannot be NULL
);

-- Insert default groups into the table
INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;  -- prevents inserting duplicates if groups already exist


-- Create table for storing contacts
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,           -- unique identifier for each contact
    name VARCHAR(100) UNIQUE NOT NULL, -- contact name must be unique and cannot be NULL
    email VARCHAR(100),              -- optional email field
    birthday DATE,                   -- optional date of birth
    group_id INTEGER REFERENCES groups(id), 
    -- foreign key linking contact to a group (one group per contact)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- automatically stores the time when the contact was created
);


-- Create table for storing phone numbers
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,           -- unique identifier for each phone record
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    -- foreign key linking phone to a contact
    -- ON DELETE CASCADE means: if contact is deleted → all their phones are deleted

    phone VARCHAR(20) NOT NULL,      -- phone number (cannot be empty)

    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
    -- restricts phone type to only these values
);