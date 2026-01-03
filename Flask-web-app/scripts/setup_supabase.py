"""
Interactive script to set up Supabase connection
"""
import os

def setup_supabase():
    print("=" * 60)
    print("🔗 Supabase Database Setup")
    print("=" * 60)
    print()
    
    print("Choose setup method:")
    print("1. Use Supabase Connection URL (Recommended)")
    print("2. Use individual database components")
    print("3. Skip and use SQLite (local database)")
    print()
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    env_content = []
    
    if choice == "1":
        print()
        print("Get your connection URL from:")
        print("Supabase Dashboard > Project Settings > Database > Connection Pooling")
        print()
        url = input("Enter Supabase Connection URL: ").strip()
        if url:
            env_content.append(f"SUPABASE_URL={url}")
    
    elif choice == "2":
        print()
        print("Enter your Supabase database credentials:")
        host = input("Database Host (e.g., db.xxxxx.supabase.co): ").strip()
        port = input("Port (default: 5432): ").strip() or "5432"
        db_name = input("Database Name (default: postgres): ").strip() or "postgres"
        user = input("Database User (default: postgres): ").strip() or "postgres"
        password = input("Database Password: ").strip()
        
        if host and password:
            env_content.append(f"SUPABASE_DB_HOST={host}")
            env_content.append(f"SUPABASE_DB_PORT={port}")
            env_content.append(f"SUPABASE_DB_NAME={db_name}")
            env_content.append(f"SUPABASE_DB_USER={user}")
            env_content.append(f"SUPABASE_DB_PASSWORD={password}")
    
    else:
        print()
        print("✅ Will use SQLite (local database)")
        print("You can set up Supabase later by creating a .env file")
        return
    
    if env_content:
        # Write to .env file
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))
            f.write('\n')
        
        print()
        print("✅ Configuration saved to .env file")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start server: python app.py")
        print("3. You should see: '✅ Connected to Supabase (PostgreSQL)'")
    else:
        print()
        print("⚠️ No configuration saved. Using SQLite.")

if __name__ == "__main__":
    setup_supabase()


