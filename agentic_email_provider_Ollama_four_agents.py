# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/ZscalerRootCA.crt'
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, DirectoryReadTool
from custom_tools_crewAI import file_writer

# Agent monitoring

# import agentops
# os.environ["AGENTOPS_API_KEY"] = 
# agentops.init('252b425d-efe8-4155-8c5c-1db6edad7e84')


# Defining the LLM in Ollama

ollama_llm = LLM(
    model="ollama/granite3-dense",
    base_url="http://192.168.0.73:11434",
    api_key="NA",
    temperature=0
)

# Defining instances of the tools

FileRead_Tool = FileReadTool()
FileWriter_Tool = file_writer()
DirectoryRead_Tool = DirectoryReadTool()


# Defining the agents

email_reader_agent = Agent(
    role='File reader',
    goal="Read contents of a local file.",
    backstory=(
        "You work for a Tier-1 Service Provider. "
        "You read emails stored locally as text files. "
    ),
    llm=ollama_llm,
    allow_delegation=False,
    verbose=True,
    memory=False,
)

provider_selector_agent = Agent(
    role='IT Change Management analyst',
    goal="Identify the Provider that sent the email.",
    backstory=(
        "You work for a Tier-1 Service Provider. "
        "You read emails stored locally as text files. "
        "You identify the name of the Provider the email comes from. "
    ),
    llm=ollama_llm,
    allow_delegation=False,
    verbose=True,
    memory=False,
)

change_analyst_agent = Agent(
    role='IT Change Management analyst',
    goal="Extract key fields from emails.",
    backstory=(
        "You work for a Tier-1 Service Provider. "
        "You are a seasoned analyst who receives emails from our telecommunication providers, regarding their maintenance works. "
        "Those works could mean fiber outages. Our network relies on those fibers, hence we could be impacted, too. "
        "You are an expert at reading such emails and extracting their key information fields. "
        "It is crucial that the information is retrieve accurately, so that we do not miss potential outages in our network. "
    ),
    llm=ollama_llm,
    allow_delegation=False,
    verbose=True,
    memory=False,
)

# Defining the tasks


file_reading_task = Task(
    description=("Read the contents of the file contoso in the local folder emails_to_analyze."
    ),
    expected_output=(
        "The contents of the email text to analyze. "
    ),
    agent=email_reader_agent,
    tools=[DirectoryRead_Tool, FileRead_Tool],
    allow_delegation=False,
    verbose=True,
    memory=False,
)

selecting_provider_task = Task(
    description=(
        "Read the contents of the file produced by the agent email_reader_agent, and identify the name of the Provider sending us the email."
        "If no Provider is identified, name is Default. "
    ),
    expected_output=(
        "The name of the Provider sending us emails. "
    ),
    agent=provider_selector_agent,
    tools=[DirectoryRead_Tool, FileRead_Tool],
    allow_delegation=False,
    verbose=True,
    memory=False,
)

reading_provider_example_task = Task(
    description=(
        "List the files of the folder examples_extraction. Each file contains an example on how to analyze an email for a given Provider."
        "Use the name of Provider identified by the agent provider_selector_agent, and read the contents of that example file belonging to that Provider."
        "If no Provider file is identified, read the contents of the file default. "
    ),
    expected_output=(
        "The contents of the example file for the selected Provider. "
    ),
    agent=email_reader_agent,
    tools=[DirectoryRead_Tool, FileRead_Tool],
    allow_delegation=False,
    verbose=True,
    memory=False,
)


email_analysis_task = Task(
    description=("""
You need to analyze the contents of the file produced by the first task, task file_reading_task.
Extract the key information fields from the email provided below. 
You need to extract the following fields, and only those fields:
    - Name of the provider sending the notification 
    - Provider's Maintenance Notification reference
    - Description of the outage
    - Outage duration
    - Locations impacted
    - Scheduled start
    - Scheduled end
    - Service IDs affected

You can use the example given by the output of the previous task, reading_provider_example_task
"""
    ),
    expected_output=(
        "The key fields. "
    ),
    agent=change_analyst_agent,
    allow_delegation=False,
    verbose=True,
    memory=False,
)

# Defining the crew

network_crew = Crew(
    agents=[email_reader_agent, provider_selector_agent, email_reader_agent, change_analyst_agent],
    tasks=[file_reading_task, selecting_provider_task, reading_provider_example_task, email_analysis_task],
    process=Process.sequential,
    verbose=True,
    output_log_file="debugging_Ollama.txt"  # Specify the path to save the log file
)

result = network_crew.kickoff()
print(result)
