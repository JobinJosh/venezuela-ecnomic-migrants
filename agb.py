import random
import matplotlib.pyplot as plt
import streamlit as st

# Define the Person class
class Person:
    def __init__(self, age, gender, education, employment, income, social_status, relatives_abroad):
        self.age = age
        self.gender = gender
        self.education = education
        self.employment = employment
        self.income = income
        self.social_status = social_status
        self.relatives_abroad = relatives_abroad
        self.accommodation = None

    def choose_accommodation(self):
        """Determine housing based on income, education, and social status"""
        if self.income > 650:
            self.accommodation = random.choice(['Luxury Apartment', 'House'])
        elif 300 <= self.income <= 650:
            self.accommodation = 'Standard Apartment'
        elif self.income < 300 and self.social_status == 'Single':
            self.accommodation = random.choice(['Shared Housing', 'Public Housing'])
        elif self.social_status == 'Family' and self.income >= 300:
            self.accommodation = 'House'
        elif self.income < 300 and self.social_status == 'Family':
            self.accommodation = 'Public Housing'
        else:
            self.accommodation = 'Undefined'

# Define function to generate people and plot housing choices
def create_persons_and_plot(num_persons, education_probs, employment_probs, income_min, income_max, social_status_probs, relatives_abroad_prob):
    persons = []
    accommodation_counts = {key: 0 for key in ['Luxury Apartment', 'Standard Apartment', 'Shared Housing', 'House', 'Public Housing', 'Undefined']}

    for _ in range(num_persons):
        age = random.choices(['15-24', '25-34', '35-44', '45-54', '55+'], [0.48, 0.333, 0.194, 0.099, 0.087])[0]
        gender = random.choices(['Female', 'Male'], [0.496, 0.504])[0]
        education = random.choices(['No education', 'Primary', 'Secondary', 'Higher'], education_probs)[0]
        employment = random.choices(['Employed', 'Unemployed'], employment_probs)[0]
        income = random.randint(income_min, income_max)  # Random income within the range
        social_status = random.choices(['Single', 'Family'], social_status_probs)[0]
        relatives_abroad = random.choices(['Yes', 'No'], [relatives_abroad_prob, 1 - relatives_abroad_prob])[0]

        person = Person(age, gender, education, employment, income, social_status, relatives_abroad)
        person.choose_accommodation()
        accommodation_counts[person.accommodation] += 1
        persons.append(person)

    # Plot the accommodation distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(accommodation_counts.keys(), accommodation_counts.values(), color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel('Number of People')
    ax.set_title(f'Accommodation Choices of {num_persons} People')

    # Add text annotations
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig)
    return persons, accommodation_counts

# Function to plot resource usage
def plot_resource_usage(resource, usage_counts, labels):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, usage_counts, color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel(f'{resource} Usage')
    ax.set_title(f'{resource} Usage by Accommodation Type')

    # Add text annotations
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig)

# Function to calculate total resource usage
def calculate_resource_usage(persons):
    accommodation_needs = {
        'Luxury Apartment': {'water': 130, 'electricity': 1.54, 'land': 65},
        'House': {'water': 130, 'electricity': 1.54, 'land': 55},
        'Standard Apartment': {'water': 130, 'electricity': 1.54, 'land': 46},
        'Shared Housing': {'water': 130, 'electricity': 1.54, 'land': 37},
        'Public Housing': {'water': 130, 'electricity': 1.54, 'land': 28},
        'Undefined': {'water': 0, 'electricity': 0, 'land': 0},
    }

    accommodation_water = {key: 0 for key in accommodation_needs}
    accommodation_electricity = {key: 0 for key in accommodation_needs}
    accommodation_land = {key: 0 for key in accommodation_needs}

    for person in persons:
        needs = accommodation_needs[person.accommodation]
        accommodation_water[person.accommodation] += needs['water']
        accommodation_electricity[person.accommodation] += needs['electricity']
        accommodation_land[person.accommodation] += needs['land']

    return accommodation_water, accommodation_electricity, accommodation_land

# Streamlit UI
st.title('Economic Migrants')
st.subheader('Venezuelan Migrants in Colombia')

num_persons = st.number_input('Number of Persons', min_value=1, step=1, value=10000)
income_min = st.number_input('Minimum Salary (Us Dollar)', min_value=0, value=300)
income_max = st.number_input('Maximum Salary (Us Dollar)', min_value=0, value=650)

education_probs = [
    st.slider('No Education Probability', 0.0, 1.0, 0.03),
    st.slider('Primary Education Probability', 0.0, 1.0, 0.26),
    st.slider('Secondary Education Probability', 0.0, 1.0, 0.53),
    st.slider('Higher Education Probability', 0.0, 1.0, 0.18)
]

employment_probs = [
    st.slider('Employed Probability', 0.0, 1.0, 0.5),
    st.slider('Unemployed Probability', 0.0, 1.0, 0.5)
]

social_status_probs = [
    st.slider('Single Probability', 0.0, 1.0, 0.51),
    st.slider('Family Probability', 0.0, 1.0, 0.49)
]

relatives_abroad_prob = st.slider('Relatives Abroad Probability', 0.0, 1.0, 0.18)

if st.button('Run Model'):
    persons, accommodation_counts = create_persons_and_plot(num_persons, education_probs, employment_probs, income_min, income_max, social_status_probs, relatives_abroad_prob)
    accommodation_water, accommodation_electricity, accommodation_land = calculate_resource_usage(persons)

    # Display graphical representations
    plot_resource_usage('Water (liters)', list(accommodation_water.values()), list(accommodation_water.keys()))
    plot_resource_usage('Electricity (kWh)', list(accommodation_electricity.values()), list(accommodation_electricity.keys()))
    plot_resource_usage('Land (sqkm)', list(accommodation_land.values()), list(accommodation_land.keys()))

    # Show total resource usage
    st.write(f"Total Water Usage: {sum(accommodation_water.values()):.2f} liters per day")
    st.write(f"Total Electricity Usage: {sum(accommodation_electricity.values()):.2f} kWh per day")
    st.write(f"Total Land Required: {sum(accommodation_land.values()):.2f} sqkm")
