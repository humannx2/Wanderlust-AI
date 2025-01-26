import streamlit as st
import requests
import json

# Set up the Streamlit page configuration
st.set_page_config(page_title="Wanderlust AI", page_icon=":guardsman:", layout="wide")

# Backend API URLs
API_BASE_URL = "http://127.0.0.1:5000"
API_URL_ACTIVITY = f"{API_BASE_URL}/generate_activity"
API_URL_QUEST = f"{API_BASE_URL}/quest"
API_URL_USER_REGISTER = f"{API_BASE_URL}/user/register"
API_URL_USER_PROFILE = f"{API_BASE_URL}/user/profile"

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "user_id" not in st.session_state:
    st.session_state.user_id = None


# --- Functions for API Interaction ---
def register_user(name, email):
    try:
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"name": name, "email": email})
        response = requests.post(API_URL_USER_REGISTER, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 201:
            return data
        else:
            st.error(data.get('error', "Registration failed"))
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_user_profile(user_id):
    try:
        response = requests.get(f"{API_URL_USER_PROFILE}/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch user profile")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def generate_activity(location, category, time):
    try:
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"location": location, "category": category, "time": time})
        response = requests.post(API_URL_ACTIVITY, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 200:
            return data['result']
        else:
            return "Error: " + data.get('error', "Unknown error")
    except Exception as e:
        return f"Error: {str(e)}"

def generate_quest(location, category, time):
    try:
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"location": location, "category": category, "time": time})
        response = requests.post(API_URL_QUEST, headers=headers, data=payload)
        data = response.json()
        if response.status_code == 200:
            return data['result']
        else:
            return "Error: " + data.get('error', "Unknown error")
    except Exception as e:
        return f"Error: {str(e)}"

def update_user_points(user_id, points):
    try:
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"points": points})
        response = requests.put(f"{API_URL_USER_PROFILE}/{user_id}/update_points", headers=headers, data=payload)
        if response.status_code == 200:
            return "Points updated successfully!"
        else:
            st.error("Failed to update points.")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def update_points():
    # Example: You can update the points with an API call or modify the session state directly.
    try:
        response = requests.post(f"{API_URL_USER_PROFILE}/update_points/{st.session_state.user_id}", 
                                 json={"points": 10})  # Assuming you add 10 points for now
        if response.status_code == 200:
            st.success("Points updated successfully!")
        else:
            st.error("Failed to update points.")
    except Exception as e:
        st.error(f"Error updating points: {str(e)}")

def verify_user(email):
    """
    Verifies the user during login using their email.
    """
    try:
        # Make a request to fetch user profile by email
        response = requests.get(f"{API_URL_USER_PROFILE}/email/{email}")

        # Debugging: Log the response status and content
        st.write(f"API Response Status: {response.status_code}")
        st.write(f"API Response Content: {response.text}")

        # Check if the request was successful
        if response.status_code == 200:
            user_data = response.json()  # Parse JSON response
            st.success("User verification successful!")
            return user_data
        elif response.status_code == 404:
            st.error("User not found. Please register first.")
            return None
        else:
            st.error(f"User verification failed: {response.status_code}. Please try again.")
            return None
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        st.error(f"Network error during verification: {str(e)}")
        return None
    except Exception as e:
        # Handle unexpected errors
        st.error(f"An unexpected error occurred: {str(e)}")
        return None


# --- Page Rendering Functions ---
def home_page():
    st.title("Wanderlust 🌍")
    st.subheader("Discover Unexpected Adventures")
    if not st.session_state.user_id:
        if st.button("Start Your Journey", key="start_journey"):
            st.session_state.current_page = "login"
    else:
        st.write(f"Welcome, {st.session_state.username}!")

def login_page():
    st.title("Login / Register")
    # Login Section (simplified for this example)
    st.subheader("Login")
    login_email = st.text_input("Email", key="login_email")
    if st.button("Login"):
        if login_email:
            user_data = verify_user(login_email)
            if user_data:
                st.session_state.user_id = user_data['id']
                st.session_state.current_page = "generate_activity"
                st.success(f"Welcome back, {user_data['name']}!")
            else:
                st.error("Login failed. Please check your email.")
        else:
            st.error("Please enter your email.")
    
    # Registration Section
    st.subheader("Register")
    new_name = st.text_input("Name", key="register_name")
    new_email = st.text_input("Email", key="register_email")
    
    if st.button("Register"):
        if new_name and new_email:
            user_data = register_user(new_name, new_email)
            if user_data:
                st.session_state.user_id = user_data['id']
                st.session_state.current_page = "profile"
                st.success(f"Welcome, {new_name}!")
        else:
            st.error("Please fill in all fields")

def generate_activity_page():
    st.title("Generate an Activity")
    location = st.text_input("Enter a Location", key="activity_location")
    category = st.selectbox("Select Category", ["Food", "Adventure", "Culture"], key="activity_category")
    time = st.text_input("Enter Time Estimate (e.g., 2 hours)", key="activity_time")

        # Tracking whether activity is generated
    if 'activity_generated' not in st.session_state:
        st.session_state.activity_generated = False

    if st.button("Generate Activity", key="activity_generate"):
        if location and category and time:
            result = generate_activity(location, category, time)
            if isinstance(result, list):
                st.subheader("Suggested Activities")
                for activity in result:
                    st.write(f"Activity: {activity['activity']}")
                    st.write(f"Description: {activity['description']}")
                    st.write(f"Time Estimate: {activity['time_estimate']}")
                    st.write("---")
                if st.button("Update Points", key="update_points_activity"):
                    points = 10  # Example points, you can modify as per your logic
                    update_response = update_user_points(st.session_state.user_id, points)
                    if update_response:
                        st.success(update_response)
            else:
                st.success(result)
        else:
            st.error("Please fill in all the fields.")
    if st.session_state.activity_generated:
        if st.button("Update Points", key="update_points_activity"):
            # Update points or trigger the relevant API call to update points
            update_points()  # Implement this function to handle point updates
            st.session_state.activity_generated = False  # Reset the state
            st.success("Points updated successfully!")

def quest_page():
    st.title("Generate a Quest")
    location = st.text_input("Enter a Location", key="quest_location")
    category = st.selectbox("Select Category", ["Food", "Adventure", "Culture"], key="quest_category")
    time = st.text_input("Enter Time Estimate (e.g., 3 hours)", key="quest_time")

    # Tracking whether quest is generated
    if 'quest_generated' not in st.session_state:
        st.session_state.quest_generated = False

    # Handle quest generation
    if st.button("Generate Quest", key="quest_generate"):
        if location and category and time:
            result = generate_quest(location, category, time)
            if isinstance(result, list):
                st.subheader("Suggested Quest")
                for activity in result:
                    st.write(f"Activity: {activity['activity']}")
                    st.write(f"Description: {activity['description']}")
                    st.write(f"Time Estimate: {activity['time_estimate']}")
                    st.write("---")
                
                # Mark quest as generated and show the update points button
                st.session_state.quest_generated = True
                st.success("Quest generated successfully!")            
            else:
                st.success(result)
        else:
            st.error("Please fill in all the fields.")
    # Show "Update Points" button only after the quest is generated
    if st.session_state.quest_generated:
        if st.button("Update Points", key="update_points_quest"):
            points = 15  # Example points, adjust as necessary
            update_response = update_user_points(st.session_state.user_id, points)
            if update_response:
                st.success(update_response)
                # Reset the state after updating points
                st.session_state.quest_generated = False  # Reset quest state
            else:
                st.error("Failed to update points.")


# Update points function (from earlier example)
def update_points():
    try:
        response = requests.post(f"{API_URL_USER_PROFILE}/update_points/{st.session_state.user_id}", 
                                 json={"points": 10})  # Update with the desired points increment
        if response.status_code == 200:
            st.success("Points updated successfully!")
        else:
            st.error("Failed to update points.")
    except Exception as e:
        st.error(f"Error updating points: {str(e)}")

# Profile page function
def profile_page():
    if not st.session_state.user_id:
        st.warning("Please login first")
        return

    # Fetch user profile data
    profile = get_user_profile(st.session_state.user_id)
    
    if profile:
        st.title(f"Profile: {profile['name']}")
        
        # Points Section
        st.subheader("Points")
        st.metric(label="Total Points", value=profile['points'])  # Display updated points
        
        # Add button to update points
        if st.button("Update Points"):
            update_points()  # Call the update function

            # Re-fetch profile data to display updated points (re-render page)
            profile = get_user_profile(st.session_state.user_id)
            st.experimental_rerun()  # Trigger a page refresh

        # Badges Section
        st.subheader("Badges")
        if profile['badges']:
            cols = st.columns(len(profile['badges']))
            for i, badge in enumerate(profile['badges']):
                cols[i].metric(label="🏆", value=badge)
        else:
            st.write("No badges earned yet")
        
        # Completed Activities
        st.subheader("Completed Activities")
        if profile['completed_activities']:
            for activity in profile['completed_activities']:
                st.write(f"🌟 {activity['name']} (Completed on {activity['completion_date']})")
        else:
            st.write("No activities completed yet")
        
        # Completed Quests
        st.subheader("Completed Quests")
        if profile['completed_quests']:
            for quest in profile['completed_quests']:
                st.write(f"🏅 {quest['title']} (Completed on {quest['completion_date']})")
        else:
            st.write("No quests completed yet")

def community_page():
    st.title("Community")
    st.write("Join the community of adventurers and share your experiences!")
    st.write("Discuss your favorite activities, share photos, and connect with like-minded explorers.")

def challenges_page():
    st.title("Challenges")
    st.write("Participate in challenges to earn more points and achievements!")
    st.write("1. Complete a 5-hour adventure in the city")
    st.write("2. Share your favorite outdoor activity on social media")
    st.write("3. Explore hidden gems in your city")

# --- Sidebar Navigation ---
st.sidebar.title("Menu")
if not st.session_state.user_id:
    if st.sidebar.button("Login / Register", key="nav_login"):
        st.session_state.current_page = "login"
else:
    if st.sidebar.button("Activity", key="generate_activity"):
        st.session_state.current_page = "generate_activity"
    if st.sidebar.button("Quest", key="nav_quest"):
        st.session_state.current_page = "quest"
    if st.sidebar.button("Profile", key="nav_profile"):
        st.session_state.current_page = "profile"
    if st.sidebar.button("Community", key="nav_community"):
        st.session_state.current_page = "community"
    if st.sidebar.button("Challenges", key="nav_challenges"):
        st.session_state.current_page = "challenges"
    if st.sidebar.button("Logout", key="nav_logout"):
        st.session_state.user_id = None
        st.session_state.current_page = "home"

# --- Render the Selected Page ---
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "login": 
    login_page()
elif st.session_state.current_page == "generate_activity":
    generate_activity_page()
elif st.session_state.current_page == "quest":
    quest_page()
elif st.session_state.current_page == "profile":
    profile_page()
elif st.session_state.current_page == "community":
    community_page()
elif st.session_state.current_page == "challenges":
    challenges_page()
