git clone <your-repo-url>(PROJECT)
cd PROJECT

2. Create a virtual environment
python -m venv .venv

3. Activate the virtual environment
Windows (PowerShell / CMD):
.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Add environment variables
Create a file called .env in the root folder with the following content:
# Path to your GCP service account key JSON file
SERVICE_ACCOUNT_KEY_PATH=C:\Users\user\Downloads\shared_jason.json

# Cloud Function URL (update this with your actual deployed URL)
CLOUD_FUNCTION_URL=https://<your-cloud-function-url>

6.Running the Project
Run the Python script:
python query.py

YOU WILL SEE:
1 . Shopping Agent
2 . Web Scraping Agent
3 . Weather & Time Agent
4 . Movie Booking Engine
5 . Restaurant Booking Engine
select agents from above list or exit,0 to Quit
Select Agent : 1
----------------------------------------------------------------------------------------------------
                               YOU ARE CURRENTLY TALKING TO THE Shopping Agent
----------------------------------------------------------------------------------------------------
Say HI! to start conversation, or type exit to Quit
YOU : hi
Cloud Run Response Status Code: 200
Cloud Run Response Body: {'agent': 'Hello! How can I help you with your shopping today? Are you looking for anything specific, or would you like to browse our catalog?\n'}
AGENT :  Hello! How can I help you with your shopping today? Are you looking for anything specific, or would you like to browse our catalog?

