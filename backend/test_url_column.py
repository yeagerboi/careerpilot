import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from db.supabase import supabase

async def main():
    print("Testing jobs table columns...")
    try:
        # Try to select the url column from jobs
        result = await supabase.table("jobs").select("id, url").limit(1).execute()
        print("Success! 'url' column exists in 'jobs' table.")
        print("Data sample:", result.data)
    except Exception as e:
        print("Error encountered:")
        print(str(e))

if __name__ == "__main__":
    asyncio.run(main())
