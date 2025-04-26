import requests
import streamlit as st

# Function to fetch profile from People Data Labs API
def fetch_pdl_profile(api_key, **kwargs):
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    
    params = {"api_key": api_key}
    params.update(kwargs)

    # Validation Rules
    identifiers = ['profile', 'email', 'phone', 'email_hash', 'lid', 'pdl_id']
    name_fields = ['first_name', 'last_name', 'name']
    additional_fields = ['company', 'school', 'location', 'street_address', 'locality', 'region', 'country', 'postal_code', 'birth_date']

    has_identifier = any(field in kwargs for field in identifiers)
    has_name_info = ('name' in kwargs) or ('first_name' in kwargs and 'last_name' in kwargs)
    has_additional_info = any(field in kwargs for field in additional_fields)

    if not (has_identifier or (has_name_info and has_additional_info)):
        raise ValueError(
            "You must provide either an identifier "
            "(profile, email, phone, email_hash, lid, pdl_id) "
            "OR (first_name and last_name OR name) AND an additional field "
            "(company, school, location, etc.)."
        )

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 200:
            return data.get('data')
        else:
            return None
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# --- Streamlit App ---

# Set your API key and query details
api_key = "93d1e5ee4e660777f4b308fb68a562b2c976664f719e7770b5eebeed4aa44c4c"

# Fetch the profile
profile = fetch_pdl_profile(
    api_key=api_key,
    first_name="Syed Muhammad Shabbar",
    last_name="Ali Naqvi",
    company="GMS Global Marketing Services"
)

# Now display the profile data in Streamlit
if profile:
    st.title("Profile Information")
    
    st.subheader("Basic Info")
    st.json({
        "Full Name": profile.get("full_name"),
        "Gender": profile.get("sex"),
        "Job Title": profile.get("job_title"),
        "Company": profile.get("job_company_name"),
        "Company Website": profile.get("job_company_website"),
        "Location": profile.get("job_company_location_name")
    })

    st.subheader("LinkedIn")
    linkedin_url = profile.get('linkedin_url')
    linkedin_username = profile.get('linkedin_username')
    if linkedin_url:
        st.markdown(f"[{linkedin_username}]({linkedin_url})")

    st.subheader("Skills")
    skills = profile.get("skills")
    if skills:
        st.write(skills)
    else:
        st.write("No skills listed.")

    st.subheader("Experience")
    experience = profile.get("experience", [])
    if experience:
        for exp in experience:
            with st.expander(exp['title']['name'] if exp.get('title') else "No Title"):
                st.write("Company:", exp['company']['name'] if exp.get('company') else "N/A")
                st.write("Start Date:", exp.get('start_date', 'N/A'))
                st.write("End Date:", exp.get('end_date', 'Present'))
                st.write("Location:", ', '.join(exp.get("location_names", [])) if exp.get("location_names") else "N/A")
    else:
        st.write("No experience listed.")
else:
    st.error("Profile not found.")
