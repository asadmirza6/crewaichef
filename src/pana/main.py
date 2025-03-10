from crewai.flow import Flow, listen, start
from litellm import completion
from pana.crews.pana_crew.chef_crew import ChefCrew
from dotenv import load_dotenv, find_dotenv

_: bool = load_dotenv(find_dotenv())

class Chef(Flow):

    @start()
    def get_user_dish(self):
        while True:
            dish_name = input("Enter a dish name (or type 'exit' to quit): ").strip()
            if dish_name.lower() == "exit":
                print("Exiting...")
                break  # Loop se bahar nikalne ke liye

            self.state["dish"] = dish_name
            self.generate_recipe()

    def generate_recipe(self):
        print(f"Generating recipe for {self.state['dish']}")
        result = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{
                "role": "user",
                "content": f"Generate a unique and delicious recipe for {self.state['dish']}."
            }]
        )
        self.state["recipe"] = result["choices"][0]["message"]["content"]
        print(self.state["recipe"])
        
        self.refine_recipe()

    def refine_recipe(self):
        print("Refining recipe with ChefCrew")
        result = (
            ChefCrew()
            .crew()
            .kickoff(inputs={"dish": self.state["recipe"]})
        )

        print("Final recipe:", result.raw)
        self.state["final_dish"] = result.raw

        self.save()

    def save(self):
        print("Saving the final recipe to dish.md")
        with open("dish.md", "w") as f:
            f.write(self.state["final_dish"])
        print("Recipe saved!\n")


def kickoff():
    obj = Chef()
    obj.kickoff()

   


