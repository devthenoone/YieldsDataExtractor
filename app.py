import requests
import streamlit as st
import json

def fetch_pdl_profile(api_key, first_name=None, last_name=None, company=None, email=None, **kwargs):
    # API endpoint
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    
    # Add API key to parameters
    params = {"api_key": api_key}
    
    # Add first_name, last_name, and company to params if provided
    if first_name and last_name:
        params["first_name"] = first_name
        params["last_name"] = last_name
    
    if company:
        params["company"] = company
    
    # Add email as an identifier if provided
    if email:
        params["email"] = email

    # Make the API request
    response = requests.get(url, params=params)
    
    # Handle API response
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 200:
            return data.get('data')
        else:
            raise Exception("No profile data found.")
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Streamlit Input Fields
st.title("Profile Fetcher")

# User input fields for first name, last name, company, and optional email
first_name = st.text_input("First Name", "Syed Muhammad Shabbar")
last_name = st.text_input("Last Name", "Ali Naqvi")
company = st.text_input("Company", "GMS Global Marketing Services")
email = st.text_input("Email (Optional)", "")

# Button to trigger profile fetch
if st.button("Fetch Profile"):
    if first_name and last_name and company:
        try:
            # Replace with your actual API key
            api_key = "93d1e5ee4e660777f4b308fb68a562b2c976664f719e7770b5eebeed4aa44c4c"
            
            # Fetch the profile
            profile = fetch_pdl_profile(
                api_key=api_key,
                first_name=first_name,
                last_name=last_name,
                company=company,
                email=email
            )
            
            if profile:
                # Step 1: Convert single quotes to double quotes and parse as JSON
                try:
                    # Step 2: Display neatly
                    st.subheader("Profile Information")
                    st.json({
                        "Full Name": profile.get("full_name"),
                        "Gender": profile.get("sex"),
                        "Job Title": profile.get("job_title"),
                        "Company": profile.get("job_company_name"),
                        "Company Website": profile.get("job_company_website"),
                        "Location": profile.get("job_company_location_name")
                    })

                    st.subheader("LinkedIn")
                    st.markdown(f"[{profile.get('linkedin_username')}]({profile.get('linkedin_url')})")

                    st.subheader("Skills")
                    st.write(profile.get("skills"))

                    st.subheader("Experience")
                    for exp in profile.get("experience", []):
                        with st.expander(exp['title']['name']):
                            st.write("Company:", exp['company']['name'])
                            st.write("Start Date:", exp['start_date'])
                            st.write("End Date:", exp['end_date'] or "Present")
                            st.write("Location:", ', '.join(exp.get("location_names", [])))
                except Exception as e:
                    st.error(f"Error loading data: {e}")
            else:
                st.error("Profile not found.")
        except Exception as e:
            st.error(f"Error fetching profile: {e}")
    else:
        st.error("Please enter all the required fields.")
