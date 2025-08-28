## How to run locally

1. Create and activate virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Start the server:
   uvicorn app.main:app --reload

4. Test endpoint:
   Visit http://127.0.0.1:8000/health