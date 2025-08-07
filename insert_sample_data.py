import psycopg
from psycopg.rows import dict_row

def insert_sample_data():
    """Insert sample data into the posts table"""
    try:
        # Connect to database
        conn = psycopg.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password='priyam@9753',
            port='5432'
        )
        print("✅ Connected to database!")
        
        cursor = conn.cursor(row_factory=dict_row)
        
        # Insert sample data
        sample_posts = [
            ('First Post', 'This is the content of the first post', True, 5),
            ('Second Post', 'This is the content of the second post', False, 3),
            ('Third Post', 'This is the content of the third post', True, 4)
        ]
        
        for title, content, published, rating in sample_posts:
            cursor.execute("""
                INSERT INTO posts (title, content, published, rating) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (title, content, published, rating))
        
        conn.commit()
        print("✅ Sample data inserted successfully!")
        
        # Verify the data
        cursor.execute("SELECT * FROM posts;")
        posts = cursor.fetchall()
        print(f"✅ Found {len(posts)} posts in the database:")
        for post in posts:
            print(f"  - ID: {post['id']}, Title: {post['title']}")
        
        cursor.close()
        conn.close()
        
    except Exception as error:
        print(f"❌ Error inserting sample data: {error}")

if __name__ == "__main__":
    insert_sample_data() 