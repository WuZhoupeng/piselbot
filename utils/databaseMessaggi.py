import asyncpg
import os
#from dotenv import load_dotenv

#load_dotenv()

class Database:
    def __init__(self):
        self.pool = None
        
    async def create_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                dsn=os.getenv("DATABASE_URL"),
                ssl="require"
            )
            
        return self.pool

db_messaggi = Database()