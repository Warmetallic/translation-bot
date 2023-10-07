import sqlite3
import pytest


# Define a fixture to create a test database and return a connection
@pytest.fixture
def test_db_setup():
    conn = sqlite3.connect("test-db.sqlite")
    cur = conn.cursor()

    # Create the 'text_history' table if it doesn't exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS text_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_text TEXT,
            translated_text TEXT
        )
    """
    )

    conn.commit()
    yield conn  # Provide the connection to the test function

    # Close the connection at the end of the test
    conn.close()


# Fixture to clear the test database after each test
@pytest.fixture
def clear_test_db():
    conn = sqlite3.connect("test-db.sqlite")
    cur = conn.cursor()

    # Delete all records from the 'text_history' table
    cur.execute("DELETE FROM text_history")
    conn.commit()
    conn.close()


# Test update_user function
def test_update_user(test_db_setup, clear_test_db):
    conn = test_db_setup
    user_id = 1
    original_text = "Hello"
    translated_text = "Bonjour"

    # Call the update_user function
    result = update_user(conn, user_id, original_text, translated_text)

    assert result == "User history updated successfully"


# Test get_user_history function
def test_get_user_history(test_db_setup, clear_test_db):
    conn = test_db_setup
    user_id = 1
    original_text = "Hello"
    translated_text = "Bonjour"

    # Call the update_user function
    update_user(conn, user_id, original_text, translated_text)

    # Call the get_user_history function
    history = get_user_history(conn, user_id)

    assert len(history) == 1
    assert history[0]["original_text"] == original_text
    assert history[0]["translated_text"] == translated_text


# Test delete_user_history function
def test_delete_user_history(test_db_setup, clear_test_db):
    conn = test_db_setup
    user_id = 1
    original_text = "Hello"
    translated_text = "Bonjour"

    # Call the update_user function
    update_user(conn, user_id, original_text, translated_text)

    # Call the delete_user_history function
    deleted_count = delete_user_history(conn, user_id)

    assert deleted_count == 1


# Define the update_user function within the test file
def update_user(conn, user_id, original_text, translated_text):
    cur = conn.cursor()

    # Insert a new text history record
    cur.execute(
        "INSERT INTO text_history (user_id, original_text, translated_text) VALUES (?, ?, ?)",
        (user_id, original_text, translated_text),
    )

    conn.commit()
    return "User history updated successfully"


# Define the get_user_history function within the test file
def get_user_history(conn, user_id):
    cur = conn.cursor()

    cur.execute(
        "SELECT original_text, translated_text FROM text_history WHERE user_id = ?",
        (user_id,),
    )
    history = [
        {"original_text": row[0], "translated_text": row[1]} for row in cur.fetchall()
    ]

    return history


# Define the delete_user_history function within the test file
def delete_user_history(conn, user_id):
    cur = conn.cursor()

    # Delete records for the user and get the count of deleted records
    cur.execute("DELETE FROM text_history WHERE user_id = ?", (user_id,))
    deleted_count = cur.rowcount

    conn.commit()

    return deleted_count
