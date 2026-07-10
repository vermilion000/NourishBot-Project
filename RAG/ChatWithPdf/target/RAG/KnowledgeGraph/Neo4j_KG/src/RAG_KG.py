import dotenv
import os
from langchain_community.graphs import NeojGraph
from langchain_google_genai import chatGoogleGenerativeAI
from langchain_core import HumanMessage,AIMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate

#setting env from config.env file
dotenv.load_dotenv('.env', override=True)

#connecting to Neo4jAPI
graph = Neo4jGraph(
    url=os.environ['NEO4J_URI'], 
    username=os.environ['NEO4J_USERNAME'],
    password=os.environ['NEO4J_PASSWORD'],
))

#connecting to GoogleAIStudios API
gemini_2.5 =  "models/gemini-2.5-pro"
llm = chatGoogleGenerativeAI(
  model = gemini_2.5,
  temperature = 0.1
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful database assistant. Use the following context to answer the user's question:\n\n{context}"),
    ("human", "{input}")
])
