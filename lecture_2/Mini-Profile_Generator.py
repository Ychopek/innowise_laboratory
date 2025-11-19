def generate_profile(age):
    """Generate a profile with given age."""
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Error: invalid age"


print("Welcome to profile generation program!")
user_name = input("Enter your name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_age = 2025 - birth_year
hobbies = []
while True:
    hobby = input("Enter your favourite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    hobbies.append(hobby)

life_stage = generate_profile(current_age)

user_profile = {
    "name" : user_name,
    "age" : current_age,
    "stage" : life_stage,
    "hobby" : hobbies
}
print("\nProfile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")
if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite hobbies ({len(hobbies)}):")
    for hobby in hobbies:
        print(f"- {hobby}")