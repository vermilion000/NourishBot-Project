import os 
from crewai import Agent,LLM,Crew,Task,Process
from crewai_tools import SerperDevTool

os.environ['SERPER_API_KEY'] = API_key   ###API key to be pasted here



##tool initaiation
search_tool=SerperDevTool()
print(type(search_tool))

##search test for serpertool 
#search_query = "Latest Breakthroughs in machine learning"
#search_results =search_tool.run(query=search_query )

## Print the results
#print(f"Search Results for '{search_results}':\n")

## inspect keys of serper keys
#print("keys of search_results", search_results.keys())



llm = LLM(
        model="watsonx/meta-llama/llama-3-3-70b-instruct",
        base_url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        max_tokens=2000,
)

#######Agents

## Define the Research Agent
research_agent = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge information and insights on any subject with comprehensive analysis',
  backstory="""You are an expert researcher with extensive experience in gathering, analyzing, and synthesizing information across multiple domains. 
  Your analytical skills allow you to quickly identify key trends, separate fact from opinion, and produce insightful reports on any topic. 
  You excel at finding reliable sources and extracting valuable information efficiently.""",
  verbose=True,
  allow_delegation=False,
  llm = llm,
  tools=[SerperDevTool()]
)


## Define the Writer Agent
writer_agent = Agent(
  role='Tech Content Strategist',
  goal='Craft well-structured and engaging content based on research findings',
  backstory="""You are a skilled content strategist known for translating 
  complex topics into clear and compelling narratives. Your writing makes 
  information accessible and engaging for a wide audience.""",
  verbose=True,
  llm = llm,
  allow_delegation=True
)

#######Tasks
## Define the Analyzer Task
research_task = Task(
  description="Analyze the major {topic}, identifying key trends and technologies. Provide a detailed report on their potential impact.",
  agent=research_agent,
  expected_output="A detailed report on {topic}, including trends, emerging technologies, and their impact."
)

## Define the Writter Task
writer_task = Task(
  description="Create an engaging blog post based on the research findings about {topic}. Tailor the content for a tech-savvy audience, ensuring clarity and interest.",
  agent=writer_agent,
  expected_output="A 4-paragraph blog post on {topic}, written clearly and engagingly for tech enthusiasts."
)

#####Define Crew

crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, writer_task],
    process=Process.sequential,
    verbose=True 
)

crew.kickoff(inputs={"topic": "Latest Generative AI breakthroughs"})
