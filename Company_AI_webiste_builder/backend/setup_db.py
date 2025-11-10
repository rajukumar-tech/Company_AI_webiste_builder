import sqlite3
import json

# Create the database and tables
def setup_database():
    conn = sqlite3.connect('company_website.db')
    c = conn.cursor()
    
    # Create services table
    c.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    
    # Create projects table
    c.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        image TEXT NOT NULL,
        tags TEXT NOT NULL
    )
    ''')
    
    # Sample data
    services = [
        ("Web Development", "Custom web applications built with modern technologies"),
        ("Mobile Development", "Native and cross-platform mobile applications"),
        ("Cloud Solutions", "Scalable cloud infrastructure and deployments")
    ]
    
    projects = [
        ("E-commerce Platform", 
         "A full-featured online shopping platform", 
         "https://picsum.photos/800/600?random=1",
         "React,Node.js,MongoDB"),
        ("Healthcare Management System", 
         "Digital solution for healthcare providers", 
         "https://picsum.photos/800/600?random=2",
         "Angular,Python,PostgreSQL"),
        ("Real Estate Portal", 
         "Property listing and management system", 
         "https://picsum.photos/800/600?random=3",
         "Vue.js,Django,MySQL")
    ]
    
    # Insert sample data
    c.execute('DELETE FROM services')
    c.execute('DELETE FROM projects')
    
    c.executemany('INSERT INTO services (name, description) VALUES (?, ?)', services)
    c.executemany('INSERT INTO projects (title, description, image, tags) VALUES (?, ?, ?, ?)', projects)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup complete with sample data!")