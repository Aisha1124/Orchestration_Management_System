from crewai import Agent, Crew, Process, Task , LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
import os
from dotenv import load_dotenv

load_dotenv()

# llm configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY_1 = os.getenv("GOOGLE_API_KEY_1")
GOOGLE_API_KEY_2 = os.getenv("GOOGLE_API_KEY_2")
GOOGLE_API_KEY_3 = os.getenv("GOOGLE_API_KEY_3")


# LLM initialization
llm1 = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GOOGLE_API_KEY_1,
    temperature=0.7
)

llm2 = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GOOGLE_API_KEY_2,
    temperature=0.7
)

llm3 = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=GOOGLE_API_KEY_3,
    temperature=0.7
)




@CrewBase
class MangerCrew():
    agents_config = "config/agents.yaml"
    # tasks_config = "config/tasks.yaml"

    
   # Fix: Embedder configuration
    embedder = {
    "provider": "google",
    "config": {
        "api_key": GEMINI_API_KEY,
        "model": "models/text-embedding-004"
        }
    }

# Excel source configuration
    excel_source = ExcelKnowledgeSource(
    file_paths=["spreadsheet.xlsx"],
    embedder=embedder
    )




    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Task Coordinator",
            goal="Efficiently assign tasks to the appropriate agents based on the nature of the task",
            backstory="You're an experienced coordinator who understands the strengths of each agent and can make optimal task assignments.",
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=GOOGLE_API_KEY_1,
                temperature=0.7
                ),
            allow_delegation=True    
        )
    

    @agent
    def greeting(self) -> Agent:
        return Agent(
            role="Greeting Agent",
            goal="Interact with users, understand user shopping needs and extract shopping details from the {user_query}.",
            backstory="You are an Greeting Agent. Your goal is to be user-friendly, interact with users, understand their shopping needs and extract shopping details.",
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=GOOGLE_API_KEY_1,
                temperature=0.7
                ),

        )
    
    @agent
    def catalog(self) -> Agent:
        return Agent(
            role="Catalog Agent",
            goal="Find products for the user based on their input from the spreadsheet.xlsx excel file.",
            backstory="You're a catalog agent who has access to a comprehensive product catalog. You can finds products for users based on their requirements from the spreadsheet.xlsx excel file.You can also provide product details and prices.",
            verbose= True,
            knowledge_sources=[self.excel_source],
            embedder=self.embedder,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=GOOGLE_API_KEY_2,
                temperature=0.7
            )
            )
    
    @agent
    def cart(self) -> Agent:
        return Agent(
            role="Cart Agent",
            goal="Handle shopping cart operations and checkout process",
            backstory="You are the Shopping Cart Agent managing the user's shopping cart. You receive products selected by the Shopping Catalog Agent,  create a shopping_cart directory  in this directory create a text and csv file , and add finalized_products to the cart file",
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=GOOGLE_API_KEY_3,
                temperature=0.7
            ),
        )
    
    @task
    def greet_and_understand(self) -> Task:
        return Task(
            description="Welcome the user to the platform, understand their shopping needs, and extract shopping-relevant details.",
            expected_output="A friendly greeting message and comprehensive understanding of the user's shopping needs from the {user_query}",

        )
    @task
    def provide_product_list(self) -> Task:
        return Task(
            description="Search the product catalog based on shopping-relevant details and provide a list of available products.",
            expected_output="A formatted catalog of products from the Catalog based on the shopping-relevant details",
        )
    
    @task 
    def add_to_cart(self) -> Task:
        return Task(
            description="Add user-confirmed products to a shopping cart and save the information in a text and CSV file.",
            expected_output="A text  and CSVfile containing the shopping cart with all selected products and relevant details",
           
            )
    

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents= [self.greeting(),self.catalog(),self.cart()],
            tasks= [self.greet_and_understand(),self.provide_product_list(),self.add_to_cart()],
            knowledge_sources=[self.excel_source],
            manager_agent=self.manager(),
            process=Process.hierarchical,
            verbose=True,
            embedder=self.embedder
            )

            



        






   











