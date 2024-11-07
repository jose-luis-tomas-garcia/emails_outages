# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
import glob
os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/ZscalerRootCA.crt'
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, DirectoryReadTool
from custom_tools_crewAI import file_writer


# Defining the LLM

ollama_llm = LLM(
    model="ollama/granite3-dense",
    base_url="http://192.168.0.73:11434",
    api_key="NA",
    temperature=0.2
)

# Defining tool instances

FileRead_Tool = FileReadTool()
FileWriter_Tool = file_writer()
DirectoryRead_Tool = DirectoryReadTool()


# Agent monitoring

# import agentops
# agentops.init('')


def analyze_email(email_content, analysis_instructions):

    # Defining the agents

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

    email_analysis_task = Task(
        description=f"""

Consider the following email:\n

-----------------------\n
{email_content}
-----------------------\n\n

Now, please follow the following instructions:\n

-----------------------\n

{analysis_instructions}
-----------------------\n

""",
        expected_output=(
            "A file inside the folder analyzed_emails_Ollama with the extracted key fields. "
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
        output_log_file="debugging_Ollama.txt"  # Specify the path to save the log file
    )

    result = network_crew.kickoff()
    print(result)

def main():

    # Reading files and calling analysis

    folder_to_analyze = 'emails_to_analyze/*'  # Adjust the pattern as needed
    analysis_instructions_file = 'instructions_for_extraction/instructions'
    for filepath in glob.glob(folder_to_analyze):
        with open(filepath, 'r') as file:
            email_content = file.read()
            analysis_instructions = open(analysis_instructions_file, 'r').read()
            analyze_email(email_content, analysis_instructions)

if __name__ == "__main__":
    main()