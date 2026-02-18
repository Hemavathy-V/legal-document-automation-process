import os
import shutil
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get MySQL credentials from .env
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# Define output folder path
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def fetch_templates_from_db():
    """
    Fetch contract templates from MySQL database and save them to output folder
    """
    try:
        # Create output folder if it doesn't exist
        Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
        print(f"Output folder ready: {OUTPUT_FOLDER}")
        
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all contract templates from database
        query = "SELECT id, template_name, template_type, file_path FROM contract_templates"
        cursor.execute(query)
        templates = cursor.fetchall()
        
        if not templates:
            print("No templates found in database.")
            cursor.close()
            connection.close()
            return
        
        print(f"Found {len(templates)} templates in database.\n")
        
        # Process each template
        for template in templates:
            template_id = template['id']
            template_name = template['template_name']
            template_type = template['template_type']
            file_path = template['file_path']
            
            # Construct full file path
            full_source_path = os.path.join(PROJECT_ROOT, file_path)
            
            # Check if source file exists
            if not os.path.exists(full_source_path):
                print(f"Template {template_id} ({template_name}): File not found at {full_source_path}")
                continue
            
            # Create destination path
            destination_path = os.path.join(OUTPUT_FOLDER, os.path.basename(file_path))
            
            try:
                # Copy file to output folder
                shutil.copy2(full_source_path, destination_path)
                print(f"Template {template_id} ({template_name}): Successfully copied to {destination_path}")
            except Exception as e:
                print(f"Template {template_id} ({template_name}): Error copying file - {str(e)}")
        
        cursor.close()
        connection.close()
        print(f"\nAll available templates have been processed and saved to: {OUTPUT_FOLDER}")
        
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    fetch_templates_from_db()
