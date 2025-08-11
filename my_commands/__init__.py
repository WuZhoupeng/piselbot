import os

EXCLUDED_DIRECTORIES = []
EXCLUDED_FILES = ["__init__.py"]

async def setup(bot):
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORIES]
        
        for filename in files:
            if filename.endswith(".py") and filename not in EXCLUDED_FILES:
                rel_path = os.path.relpath(root, os.path.dirname(__file__))
                
                if rel_path == ".":
                    module_name = filename[:-3]
                else:
                    module_name = f"{rel_path.replace(os.sep, '.')}.{filename[:-3]}"
                
                try:
                    await bot.load_extension(f"my_commands.{module_name}")
                    print(f"Caricato il comando {module_name}")
                except Exception as e:
                    print(f"Errore nel caricamento di {module_name}: {e}")