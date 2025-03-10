from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ChefCrew:
    """Chef Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def chef_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["chef_agent"]
        )

    @task
    def cook_recipe(self) -> Task:
        return Task(
            config=self.tasks_config["cook_recipe"]
        )  # <-- Closing parenthesis fixed here

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
