import psycopg
from psycopg.rows import dict_row

def test_database_connection():
    """Test database connection and check if posts table exists"""
    try:
        # Test connection
        conn = psycopg.connect(
            host='localhost',
            dbname='fastapi',
            user='postgres',
            password='priyam@9753',
            port='5432'
        )
        print("✅ Database connection successful!")
        
        # Test cursor creation
        cursor = conn.cursor(row_factory=dict_row)
        print("✅ Cursor created successfully!")
        
        # Check if posts table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'posts'
            );
        """)
        
        table_exists = cursor.fetchone()['exists']
        if table_exists:
            print("✅ Posts table exists!")
            
            # Try to fetch data
            cursor.execute("SELECT * FROM posts;")
            posts = cursor.fetchall()
            print(f"✅ Found {len(posts)} posts in the database")
            for post in posts:
                print(f"  - {post}")
        else:
            print("❌ Posts table does not exist!")
            print("You need to create the posts table first.")
            
        cursor.close()
        conn.close()
        
    except Exception as error:
        print(f"❌ Database connection failed: {error}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if the database 'fastapi' exists")
        print("3. Verify username and password")
        print("4. Ensure the posts table exists")

if __name__ == "__main__":
    test_database_connection() 