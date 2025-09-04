import streamlit as st
from openai import OpenAI, AuthenticationError, APIConnectionError

# Show title and description.
st.title("Tony D's Lab 2")
st.write(
    "Upload a document below and ask a question about it – GPT will answer!"
)

# Sidebar for summary format options
summary_format = st.sidebar.radio(
    "Choose Summary Format:",
    options=[
        "Summarize in 100 words",
        "Summarize in 2 paragraphs",
        "Summarize in 5 bullet points",
    ]
)

# Sidebar for model selection
use_advanced_model = st.sidebar.checkbox("Use GPT-4o (Advanced)")
model_choice = "gpt-4o" if use_advanced_model else "gpt-5-mini"  
#IN RESPONSE to 2D: mini is the default because it is significantly cheaper to run, that way if people keep running for fun it costs me less money. 5 nano will fill fit the use case

# Get OpenAI API key from secrets
openai_api_key = st.secrets["API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    try: 
        # Create an OpenAI client.
        client = OpenAI(api_key=openai_api_key)

        # Test API key with a lightweight call
        client.models.list()

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        # User question
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )

        if uploaded_file and question:
            document = uploaded_file.read().decode()

            # Add selected summary format to the prompt
            format_instruction = ""
            if summary_format == "Summarize in 100 words":
                format_instruction = "Please summarize the document in approximately 100 words."
            elif summary_format == "Summarize in 2 paragraphs":
                format_instruction = "Please summarize the document in 2 well-connected paragraphs."
            elif summary_format == "Summarize in 5 bullet points":
                format_instruction = "Please summarize the document using 5 bullet points."

            full_prompt = (
                f"Here's a document:\n{document}\n\n"
                f"---\n\n{question}\n\n"
                f"{format_instruction}"
            )

            messages = [{"role": "user", "content": full_prompt}]

            # Call OpenAI API
            stream = client.chat.completions.create(
                model=model_choice,
                messages=messages,
                stream=True,
            )

            # Display response in the app
            st.write_stream(stream)

    except AuthenticationError:
        st.error("Invalid OpenAI API key. Please check and try again.")
    except APIConnectionError:
        st.error("Network error: Unable to connect to OpenAI servers.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
