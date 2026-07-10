from crewai import Agent,Crew,Task,Process,LLM

llm = LLM(
        model="watsonx/meta-llama/llama-3-3-70b-instruct",
        base_url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        max_tokens=2000,
)

Social_medial_agent = Agent(
    role = "Social Media Agent",
    goal = "curates summary and short form version of {content}",
    backstory = "A digital storyteller who excels at crafting compelling posts to drive engagement and traffic.",
    llm = llm
    verbose = True,
    allow_delegation = False
)

key_task = Task(
    description = " Generate engaging and platform-specific posts (such as LinkedIn or X/Twitter) based on the research and blog content. This agent will help amplify the reach of users content by distilling key insights into short, compelling messages",
    agent = Social_medial_agent,
    expected_output = "Detailed suggestion of post from analysis of {content} Images with caption in the form of string"
)

crew1 = Crew(
    tasks = [key_task],
    agents = [Social_medial_agent],
    process = Process.Sequential,
    verbode = True
)
