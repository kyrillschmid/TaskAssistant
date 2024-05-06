import streamlit as st

import base64

# Page 1: Introduction
def page_intro():

    image_path = 'src/task_assistant/image.png'
    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode()
    header_html = f"""
    <style>
    .header-image {{
        width: 100px; height: 100px; border-radius: 50%; border: 2px solid #fff;
    }}
    </style>
    <img src="data:image/jpeg;base64,{encoded_image}" class="header-image">
    """
    st.markdown(header_html, unsafe_allow_html=True)

    st.header("ChatGPT and now?")
    st.write("- (Non-technical) people might have problems to identify the possibilties of current AI technology")
    st.write("- Technology is changing rapidly - moving target")
    st.write("- We can offer LABs to identify opportunities to use AI effectively in your work")


# Page 2: Concerns
def page_concerns():
    st.title("Privacy Concerns with LMS")
    st.header("Concerns")
    st.write("There are several privacy concerns associated with using LMS, including:")
    st.write("- Data collection: LMS platforms often collect large amounts of user data, including personal information.")
    st.write("- Data security: The security of this data is a significant concern, as breaches can lead to sensitive information being compromised.")
    st.write("- Tracking: LMS may track user behavior, such as how much time a student spends on each activity or assessment.")
    st.write("- Third-party access: Some LMS platforms may share data with third-party services, raising questions about data ownership and privacy.")

# Page 3: Mitigation
def page_mitigation():
    st.title("Privacy Concerns with LMS")
    st.header("Mitigation Strategies")
    st.write("To address these concerns, various mitigation strategies can be implemented, including:")
    st.write("- User consent: Users should be informed about what data is collected and how it will be used, and given the opportunity to consent.")
    st.write("- Data encryption: Data collected by LMS platforms should be encrypted to protect it from unauthorized access.")
    st.write("- Anonymization: Where possible, personal data should be anonymized to protect user privacy.")
    st.write("- Compliance with regulations: LMS platforms should comply with relevant privacy regulations, such as GDPR or CCPA.")

# Main function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Concerns", "Mitigation"])

    if page == "Introduction":
        page_intro()
    elif page == "Concerns":
        page_concerns()
    elif page == "Mitigation":
        page_mitigation()

if __name__ == "__main__":
    main()
