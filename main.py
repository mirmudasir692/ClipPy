from clippy import setup
import os
from dotenv import load_dotenv
load_dotenv()
setup(uri=os.getenv("MONGO_URI") or "")