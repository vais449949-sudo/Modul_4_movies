import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("SUPER_ADMIN_USERNAME"))
print(os.getenv("SUPER_ADMIN_PASSWORD"))

class SuperAdminCreds:
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')
