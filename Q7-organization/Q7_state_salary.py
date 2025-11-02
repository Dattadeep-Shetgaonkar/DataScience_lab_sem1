# Define Employee class
class Employee:
    def __init__(self, name, gender, location, salary):
        self.name = name
        self.gender = gender.lower()
        self.location = location
        self.salary = int(salary)

# Define State class
class State:
    def __init__(self, name):
        self.name = name
        self.employeeList = []

    def add_employee(self, employee):
        self.employeeList.append(employee)

    def total_salary(self):
        total = 0
        for emp in self.employeeList:
            total = total + emp.salary
        return total

# Define Organization class
class Organization:
    def __init__(self):
        self.states = {}

    def add_employee(self, employee):
        loc = employee.location
        if loc not in self.states:
            self.states[loc] = State(loc)
        self.states[loc].add_employee(employee)

    def total_salary_by_state(self):
        result = {}
        for state_name in self.states:
            result[state_name] = self.states[state_name].total_salary()
        return result

    def gender_based_salary(self):
        male_salary = 0
        female_salary = 0
        for state_name in self.states:
            state = self.states[state_name]
            for emp in state.employeeList:
                if emp.gender == "male":
                    male_salary = male_salary + emp.salary
                elif emp.gender == "female":
                    female_salary = female_salary + emp.salary
        return {"male salary": male_salary, "female salary": female_salary}

# Function to write employees sorted by state to a file
def write_sorted_employees_flat(org, filename):
    all_employees = []

    # Collect all employees from all states
    for state_name in org.states:
        state = org.states[state_name]
        for emp in state.employeeList:
            all_employees.append(emp)

    # Sort employees by their location (state name)
    for i in range(len(all_employees)):
        for j in range(i + 1, len(all_employees)):
            if all_employees[i].location > all_employees[j].location:
                temp = all_employees[i]
                all_employees[i] = all_employees[j]
                all_employees[j] = temp

    # Write to file
    file = open('./employee.txt', "w")
    file.write("name,location,gender,age")
    file.write("\n")
    for emp in all_employees:
        line = emp.name + "," + emp.location + "," + emp.gender + "," + str(emp.salary) + "\n"
        file.write(line)
    file.close()

# === Main program starts here ===

# Read employee data from file
file = open(r"C:\Users\shetg\OneDrive\Desktop\Data Science\Q7-organization\employee.txt", "r")
records = file.read().strip().split("\n")
file.close()

org = Organization()

# Skip header row, start from 1
for i in range(1, len(records)):
    if records[i].strip() == "":
        continue
    parts = records[i].split(",")
    name = parts[0].strip()
    gender = parts[1].strip()
    location = parts[2].strip()
    salary = parts[3].strip()

    emp = Employee(name, gender, location, salary)
    org.add_employee(emp)

# Print total salary by state
print("Total Salary by State:")
totals = org.total_salary_by_state()
for state_name in totals:
    print(state_name + ":", totals[state_name])

# Print gender based salary
print("\nGender-wise Salary Distribution:")
gender_salaries = org.gender_based_salary()
print(gender_salaries)

# Print total states and list of states
print("\nTotal States in Organization:", len(org.states))
print("States Present in Organization:")
for state_name in org.states:
    print("-", state_name)


# Write sorted employees to new file
write_sorted_employees_flat(org, "sorted_employees_flat.csv")
print("\nEmployee records saved to 'sorted_employees_flat.csv' sorted by state.")