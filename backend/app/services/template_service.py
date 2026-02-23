from database.db_connection import get_connection

def fetch_templates():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, template_name, template_type, file_path
        FROM contract_templates
        ORDER BY id
    """)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result