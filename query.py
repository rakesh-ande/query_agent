import time
import traceback
import os
import requests
from google.oauth2 import service_account
from dotenv import load_dotenv
import google.auth.transport.requests 
import google.oauth2.id_token    
from logging import Logger

load_dotenv()

from vertexai import agent_engines

cloud_fun_url=os.environ.get("CLOUD_FUNCTION_URL")
SERVICE_ACCOUNT_KEY_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

print(f"Service Account Key Path: {SERVICE_ACCOUNT_KEY_PATH}")

def query_the_agent(user_id: str, agent_path: str,query:str, session_id: str = None):
    """Sends a single query to the deployed agent to generate a log entry."""
    try:
        # Load credentials for Vertex AI agent interaction
        if SERVICE_ACCOUNT_KEY_PATH:
            credentials_vertex_ai = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH)
        else:
            Logger.info("please set GCP service account path")
            
        agent = agent_engines.get(agent_path)

        if not session_id:
            session_id = agent.create_session(user_id=user_id)["id"]
            


        

        # --- AUTHENTICATION FOR CLOUD RUN CALL ---
        # Load credentials for Cloud Run invocation
        credentials_cloud_run = None
        if SERVICE_ACCOUNT_KEY_PATH and os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            credentials_cloud_run = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH)
        else:
            # Fallback to Application Default Credentials for Cloud Run if no explicit SA path
            credentials_cloud_run, _ = google.auth.default()

        if credentials_cloud_run is None:
            raise ValueError("No credentials found for Cloud Run invocation. Please set GOOGLE_APPLICATION_CREDENTIALS or ensure gcloud auth is configured.")

        # Create a Request object to use with ID Token generation
        auth_req = google.auth.transport.requests.Request()
        
        
        target_audience = cloud_fun_url
        
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)
        
        headers = {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json" # Ensure content type is set for JSON payload
        }
        # print(f"--- Generated ID Token for Cloud Run URL: {target_audience} ---")
        # --- END AUTHENTICATION SETUP ---

        
        events_iterator = agent.stream_query(user_id=user_id, session_id=session_id, message=query)
        events = list(events_iterator)
        final_response=""
        for _ in events:
            
            # final_response=event.get("content").get("parts")[0].get("text")
            pass
            

        payload = dict(session_id=session_id, agent_path=agent_path, events=events, user_id=user_id)
        

        response = requests.post(url=target_audience, json=payload, headers=headers)

        # print(f"Cloud Run Response Status Code: {response.status_code}")
        try:
            return (response.json().get("agent"),session_id)
        except requests.exceptions.JSONDecodeError:
            print("Cloud Run Response Body (not JSON):", response.text)


    except Exception as e:
        print("\nAn exception occurred in the main process:")
        print(traceback.format_exc())




if __name__ == "__main__":
    

    agents = {
        "Shopping Agent":
        "projects/588981535607/locations/us-central1/reasoningEngines/8653130122318053376",

        "Web Scraping Agent":
        "projects/588981535607/locations/us-central1/reasoningEngines/3865803718423216128",

        "Weather & Time Agent":
        "projects/588981535607/locations/us-central1/reasoningEngines/1486777215264751616",

        "Movie Booking Engine":
        "projects/588981535607/locations/us-central1/reasoningEngines/8487622836012187648",

        "Restaurant Booking Engine":
        "projects/588981535607/locations/us-central1/reasoningEngines/1899419531122573312"
    }

    current_agent=None
    while True:

        if current_agent:
            break

        else :
            agent_list=[agent for agent in agents.keys()]
            for i in range(len(agent_list)):
                print(i+1,".",agent_list[i])
            print("select agents from above list or exit,0 to Quit")
            select_agent=input("Select Agent :")
            select_agent=int(select_agent) if select_agent.isdigit() else select_agent
            if select_agent in ["exit",0,"bye"]:
                break  
            elif select_agent > -1 and select_agent < len(agent_list):
                current_agent=agent_list[select_agent-1]
            else:
                print("please select from above agents only")

    print("-"*100)
    print(" "*47,"BYE!")if not current_agent else print(" "*30,f"YOU ARE CURRENTLY TALKING TO THE {current_agent}")
    print("-"*100)
    session_id=""
    while current_agent:
        resouce_id=agents[current_agent]
        print("Say HI! to start conversation, or type exit to Quit")
        query=input("YOU : ")
        if query in ["exit","0","bye"]:
            break  
        if session_id:
            response,_=query_the_agent(user_id="sai",agent_path=resouce_id,query=query,session_id=session_id)
        else:
            response,session_id=query_the_agent(user_id="sai",agent_path=resouce_id,query=query)
        print("AGENT : ",response)
    
        
        
 