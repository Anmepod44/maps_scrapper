import json
import random

# Load the JSON data
file_path = '/mnt/data/kenyan_meals_numbers_costs_500.json'
with open(file_path, 'r') as file:
    data = json.load(file)

def meal_planner():
    # Collect user preferences via CLI
    try:
        budget = int(input("Enter your budget (max cost per meal in Ksh): "))
        meal_types = input("Enter preferred meal types (comma-separated, e.g., Breakfast, Snack): ").split(",")
        dietary_restrictions = input("Enter dietary restrictions (comma-separated, e.g., Dairy Free, Gluten Free): ").split(",")
        max_calories = int(input("Enter maximum calories per meal: "))
        difficulty = input("Enter preferred cooking difficulty (Easy, Medium, Hard): ")

        # Clean inputs
        meal_types = [meal.strip() for meal in meal_types]
        dietary_restrictions = [restriction.strip() for restriction in dietary_restrictions]

        # Filter meals based on user preferences
        filtered_meals = [
            meal for meal in data
            if meal.get("Cost") and int(meal["Cost"].replace("Ksh ", "")) <= budget
            and meal.get("Meal Type") in meal_types
            and all(tag in meal.get("Dietary Tags", []) for tag in dietary_restrictions)
            and meal.get("Calories") and meal["Calories"] <= max_calories
            and meal.get("Difficulty") == difficulty
        ]
        
        # Randomly select three meals from the filtered list
        recommended_meals = random.sample(filtered_meals, min(len(filtered_meals), 3))
        
        # Display the recommendations
        if recommended_meals:
            print("\nHere are your meal recommendations:\n")
            for meal in recommended_meals:
                print(f"Name: {meal['Kenyan Name']}")
                print(f"Type: {meal['Meal Type']}")
                print(f"Calories: {meal['Calories']} kcal")
                print(f"Cost: {meal['Cost']}")
                print(f"Difficulty: {meal['Difficulty']}")
                print(f"Dietary Tags: {', '.join(meal.get('Dietary Tags', []))}")
                print(f"Ingredients: {', '.join(meal['Ingredients'])}")
                print("-" * 50)
        else:
            print("\nNo meals match your preferences. Try adjusting your criteria.")
    except ValueError:
        print("\nInvalid input. Please ensure numerical inputs for budget and calories.")

if __name__ == "__main__":
    meal_planner()