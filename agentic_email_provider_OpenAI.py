# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/ZscalerRootCA.crt'
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, DirectoryReadTool
from custom_tools_crewAI import file_writer

# Defining the LLM

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
os.environ["OPENAI_API_KEY"] = ""

# Defining instances of the tools

FileRead_Tool = FileReadTool()
FileWriter_Tool = file_writer()
DirectoryRead_Tool = DirectoryReadTool()


# Defining the agents

change_analyst_agent = Agent(
    role='IT Change Management analyst',
    goal="Extract key fields from emails.",
    backstory=(
        "You work for a Tier-1 Service Provider. "
        "You are a seasoned analyst who receives emails from our telecommunication providers, regarding their maintenance works. "
        "Those works could mean fiber outages. Our network relies on those fibers, hence we could be impacted, too. "
        "You are an expert at reading such emails and extracting their key information fields. "
        "It is crucial that the information is retrieve accurately, so that we do miss potential outages in our network. "
    ),
    # llm=ollama_llm,
    allow_delegation=False,
    verbose=True,
    memory=False,
)

# Defining the tasks

email_analysis_task = Task(
    description=("""
Extract the key information fields from the emails provided. 
The emails are in the folder emails_to_analyse, one email per file. 
For each one, you need to extract the fields: 
    - Name of the provider sending the notification 
    - Provider's Maintenance Notification reference
    - Description of the outage
    - Outage duration
    - Locations impacted
    - Scheduled start
    - Scheduled end
    - Circuit IDs affected
Note: The Circuit ID or IDs affected are short designators, and they usually come with a number, along with other words like 'ETH', 'UIF, or similar.
Information like cirty, location or street are not part of the Circuit IDs.
                 

"""
    ),
    expected_output=(
        "Those fields need to be saved the folder analyzed_emails, one file for each email processed. "
    ),
    agent=change_analyst_agent,
    tools=[DirectoryRead_Tool, FileRead_Tool, FileWriter_Tool],
    allow_delegation=False,
    verbose=True,
    memory=False,
)

# Defining the crew

network_crew = Crew(
    agents=[change_analyst_agent],
    tasks=[email_analysis_task],
    process=Process.sequential,
    verbose=True,
    output_log_file="debugging_OpenAI.txt"  # Specify the path to save the log file
)

result = network_crew.kickoff()
print(result)
