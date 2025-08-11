async def SetupTables(db):
    db_pool = db

    async with db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS reminder_messages (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                time TIME NOT NULL,
                date DATE NOT NULL
            )
        ''')

    print("Tabelle create")