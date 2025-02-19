import streamlit as st
import os
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# Streamlit UI
st.title("🛫 Travel Planning Chatbot")
st.write("Enter your OpenAI API key below to start chatting with the travel bot.")

# User input for API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Store the API key in session state
if api_key:
    st.session_state["OPENAI_API_KEY"] = api_key

# Check if API key is provided
if "OPENAI_API_KEY" in st.session_state:
    # Use the stored API key
    os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]

    # Initialize LLM with the user-provided API key
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    # Memory for individual user chat
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

    memory = st.session_state.memory

    # Sample Travel Plans
    plans = [
        {
            "plan name": "Gujarat Tour",
            "place": "Gujarat",
            "days": "10 days",
            "itinerary": [
                {"day": 1, "location": "Ahmedabad", "activities": ["Sabarmati Ashram", "Akshardham Temple", "Law Garden Market"]},
                {"day": 2, "location": "Ahmedabad - Gir National Park", "activities": ["Drive to Gir", "Safari in Gir National Park"]},
                {"day": 3, "location": "Gir - Somnath", "activities": ["Somnath Temple", "Triveni Sangam"]},
                {"day": 4, "location": "Dwarka", "activities": ["Dwarkadhish Temple", "Nageshwar Jyotirlinga", "Bet Dwarka"]},
                {"day": 5, "location": "Bhuj", "activities": ["Aina Mahal", "Prag Mahal", "Kutch Museum"]},
                {"day": 6, "location": "Rann of Kutch", "activities": ["White Desert Safari", "Cultural Night"]},
                {"day": 7, "location": "Vadodara", "activities": ["Laxmi Vilas Palace", "Champaner-Pavagadh Archaeological Park"]},
                {"day": 8, "location": "Statue of Unity", "activities": ["Viewing Gallery", "Laser Show"]},
                {"day": 9, "location": "Saputara", "activities": ["Sunset Point", "Gira Waterfalls"]},
                {"day": 10, "location": "Return to Ahmedabad", "activities": ["Shopping & Departure"]}
            ],
            "meals": ["Breakfast and Dinner included", "Lunch on your own"],
            "accommodation": "3-star or 4-star hotels",
            "transportation": "Private AC Vehicle & Domestic Flights (if needed)",
            "total_price": "INR 50,000 - 70,000 per person"
        },
        {
            "plan name": "Kerala Tour",
            "place": "Kerala",
            "days": "7 days",
            "itinerary": [
                {"day": 1, "location": "Kochi", "activities": ["Chinese Fishing Nets", "Fort Kochi", "Jew Town"]},
                {"day": 2, "location": "Munnar", "activities": ["Tea Gardens", "Mattupetty Dam", "Echo Point"]},
                {"day": 3, "location": "Munnar - Thekkady", "activities": ["Periyar Wildlife Sanctuary", "Boat Ride"]},
                {"day": 4, "location": "Thekkady - Alleppey", "activities": ["Houseboat Stay", "Backwater Cruise"]},
                {"day": 5, "location": "Kovalam", "activities": ["Beach Visit", "Lighthouse Beach"]},
                {"day": 6, "location": "Kanyakumari", "activities": ["Vivekananda Rock", "Sunset Point"]},
                {"day": 7, "location": "Return to Kochi", "activities": ["Shopping & Departure"]}
            ],
            "meals": ["Breakfast and Dinner included", "Lunch on your own"],
            "accommodation": "Houseboat & 3-star hotels",
            "transportation": "Private AC Vehicle & Domestic Flights",
            "total_price": "INR 40,000 - 60,000 per person"
        },
        {
            "plan name": "Manali Tour",
            "place": "Manali",
            "days": "6 days",
            "itinerary": [
                {"day": 1, "location": "Delhi - Manali (Overnight Journey)", "activities": ["Board Volvo Bus/Private Taxi"]},
                {"day": 2, "location": "Manali", "activities": ["Hadimba Temple", "Mall Road", "Vashisht Hot Springs"]},
                {"day": 3, "location": "Solang Valley", "activities": ["Skiing", "Paragliding", "Cable Car Ride"]},
                {"day": 4, "location": "Rohtang Pass (if open)", "activities": ["Snow Activities", "Photography"]},
                {"day": 5, "location": "Kullu & Naggar", "activities": ["Rafting", "Naggar Castle"]},
                {"day": 6, "location": "Manali - Delhi", "activities": ["Departure via Volvo Bus or Flight"]}
            ],
            "meals": ["Breakfast and Dinner included", "Lunch on your own"],
            "accommodation": "3-star hotels & camps",
            "transportation": "Volvo Bus/Private Taxi & Flights (if needed)",
            "total_price": "INR 25,000 - 40,000 per person"
        },
        {
            "plan name": "Goa Tour",
            "place": "Goa",
            "days": "5 days",
            "itinerary": [
                {"day": 1, "location": "Arrival in Goa", "activities": ["Baga Beach", "Anjuna Beach", "Nightlife"]},
                {"day": 2, "location": "North Goa", "activities": ["Aguada Fort", "Chapora Fort", "Water Sports"]},
                {"day": 3, "location": "South Goa", "activities": ["Dudhsagar Waterfalls", "Colva Beach", "Basilica of Bom Jesus"]},
                {"day": 4, "location": "Island Tour", "activities": ["Grand Island", "Dolphin Watching"]},
                {"day": 5, "location": "Shopping & Departure", "activities": ["Souvenir Shopping at Panjim Market"]}
            ],
            "meals": ["Breakfast included", "Lunch & Dinner on your own"],
            "accommodation": "Beach Resorts & 4-star hotels",
            "transportation": "Rental Bikes/Cars & Domestic Flights",
            "total_price": "INR 30,000 - 50,000 per person"
        }
    ]

    # Define Functions for the Agent's Tools
    def plan_suggestions(query):
        return plans

    def specific_plan_details(query):
        for plan in plans:
            if plan["plan name"].lower() in query.lower():
                return plan
        return "Please specify a valid plan name."

    # Tools for the LangChain Agent
    tools = [
        Tool(name="Plan Suggestions", func=plan_suggestions, description="Suggest travel plans."),
        Tool(name="Specific Plan Details", func=specific_plan_details, description="Get details of a travel plan."),
    ]

    # Initialize LangChain Agent
    agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=True)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Ask me about travel plans...")

    if user_input:
        # Display User Message
        st.chat_message("user").markdown(user_input)

        # Generate Response
        response = agent.run(user_input)

        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Store messages
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your OpenAI API key to start chatting.")