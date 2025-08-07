import psycopg
from psycopg.rows import dict_row

def check_database():
    """Check the actual database structure and data"""
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
        
        # Check table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'posts' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📋 Posts table structure:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']})")
        
        # Check row count
        cursor.execute("SELECT COUNT(*) as count FROM posts;")
        count = cursor.fetchone()['count']
        print(f"\n📊 Total posts in database: {count}")
        
        # Get all posts
        cursor.execute("SELECT * FROM posts;")
        posts = cursor.fetchall()
        
        if posts:
            print("\n📝 Posts in database:")
            for post in posts:
                print(f"  - ID: {post.get('id', 'N/A')}, Title: {post.get('title', 'N/A')}")
        else:
            print("\n❌ No posts found in database")
        
        cursor.close()
        conn.close()
        
    except Exception as error:
        print(f"❌ Error checking database: {error}")

if __name__ == "__main__":
    check_database() 