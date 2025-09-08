from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.youtube_tool import YouTubeTranscriptTool
from .tools.web_scraping_tool import WebScrapingTool
import os

# Try to import SerperDevTool
try:
    from crewai_tools import SerperDevTool
    SERPER_AVAILABLE = True
except ImportError:
    SERPER_AVAILABLE = False
    print("⚠️ SerperDevTool not available, web search will be limited")


@CrewBase
class FactChecker:
    """Fact checking crew for verifying claims and content"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.serper_key = os.getenv("SERPER_API_KEY")

        # Decide availability
        self.use_openai = bool(self.openai_key)
        self.use_serper = bool(self.serper_key and SERPER_AVAILABLE)

        if not self.use_openai and not self.use_serper:
            raise RuntimeError(
                "❌ No valid API backend: please set OPENAI_API_KEY or SERPER_API_KEY"
            )

    @agent
    def fact_researcher(self) -> Agent:
        tools = [YouTubeTranscriptTool(), WebScrapingTool()]
        if self.use_serper:
            tools.append(SerperDevTool())
        return Agent(
            config=self.agents_config['fact_researcher'],
            verbose=True,
            tools=tools
        )

    @agent
    def content_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_analyzer'],
            verbose=True,
            tools=[YouTubeTranscriptTool(), WebScrapingTool()]
        )

    @agent
    def fact_verifier(self) -> Agent:
        tools = []
        if self.use_serper:
            tools.append(SerperDevTool())
        return Agent(
            config=self.agents_config['fact_verifier'],
            verbose=True,
            tools=tools
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.fact_researcher()
        )

    @task
    def content_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_analysis_task'],
            agent=self.content_analyzer(),
            context=[self.research_task()]
        )

    @task
    def verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['verification_task'],
            agent=self.fact_verifier(),
            context=[self.research_task(), self.content_analysis_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the fact checking crew"""
        return Crew(
            agents=[self.fact_researcher(), self.content_analyzer(), self.fact_verifier()],
            tasks=[self.research_task(), self.content_analysis_task(), self.verification_task()],
            process=Process.sequential,
            verbose=True,
        )
