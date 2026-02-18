from .base import ClauseRetriever
from database.db_connection import get_connection




class SQLRetriever(ClauseRetriever):

    def retrieve(self, user_query: str):

        # Simple keyword detection (temporary logic)
        categories = []
        if "payment" in user_query.lower():
            categories.append("Payment")
        if "liability" in user_query.lower():
            categories.append("Liability")

        if not categories:
            categories.append("General")

        conn = get_connection()
        cursor = conn.cursor()


        placeholders = ','.join(['%s'] * len(categories))
        query = f"""
        SELECT clause_title, clause_text, clause_category
        FROM clauses
        WHERE clause_category IN ({placeholders})
        LIMIT 5
        """
        cursor.execute(query, categories)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
