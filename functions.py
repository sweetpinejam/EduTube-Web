# import streamlit as st
# from googleapiclient.discovery import build
# import google.generativeai as genai
# import sqlite3
# from yake import KeywordExtractor
# import cohere
#
# genai.configure(api_key=st.secrets["genai_api_key"])
#
# def generate_tags():
#     model = genai.GenerativeModel('gemini-1.5-pro')
#     tags_prompt = 'Generate random educational tags like this subject1, subject2, subject3, subject4 etc. just plain text. just a few of them. bring advanced and diverse subject'
#     response = model.generate_content(tags_prompt)
#     response = response.text.split(', ')
#     return response
#
# def create_query_gemini(keywords):
#     model = genai.GenerativeModel('gemini-1.5-pro')
#     tags_prompt = f'Generate a topic to search with these keywords {keywords}. Generate in simple plain text. No colon just texts. Make it creative.'
#     response = model.generate_content(tags_prompt)
#     return response.text
#
# def create_query_cohere(keywords):
#     api_key = st.secrets["cohere_api_key"]
#     co = cohere.Client(api_key)
#     prompt = f"Please create a question for YouTube in just a single sentence in plain text from these topics {keywords}. For education"
#     response = co.generate(
#         model="command-light",
#         prompt=prompt,
#         max_tokens=40,
#         temperature=0.8
#     )
#     return response.generations[0].text
#
# def create_query_parallel(keywords):
#     query = ''
#     try:
#         query = create_query_gemini(keywords)
#     except Exception:
#         try:
#             query = create_query_cohere(keywords)
#         except Exception:
#             st.error("Exceed LLMs APIs Limit. Please Wait for a minute.")
#     finally:
#         return query
#
# def search_videos(query, api_key=st.secrets["youtube_api_key"]):
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     search_response = youtube.search().list(
#         q=query,
#         part='snippet',
#         type='video',
#         maxResults=6
#     ).execute()
#     return search_response.get('items', [])
#
# def extract_keywords(query):
#     extractor = KeywordExtractor()
#     keywords = extractor.extract_keywords(query)
#     return [key[0] for key in keywords]
#
# def setup_database():
#     conn = sqlite3.connect('.venv/queries.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS queries (
#             id INTEGER PRIMARY KEY,
#             query TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# def save_query(query):
#     conn = sqlite3.connect('.venv/queries.db')
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO queries (query) VALUES (?)', (query,))
#     conn.commit()
#     conn.close()
#
# def get_last_query():
#     conn = sqlite3.connect('.venv/queries.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT query FROM queries ORDER BY id DESC LIMIT 1')
#     result = cursor.fetchone()
#     conn.close()
#     if result:
#         return result[0]
#     return ""
#
# def deep_search():
#     setup_database()
#
#     st.markdown(
#         """
#         <style>
#             .st-d6 {
#                 display: flex;
#                 align-items: center;
#                 border: 1px solid #ccc;
#                 border-radius: 5px;
#                 padding: 8px;
#                 margin: 10px 0;
#             }
#             .st-d7 {
#                 flex: 1;
#                 border: none;
#                 outline: none;
#                 padding: 0 8px;
#             }
#             .st-d8 {
#                 background-color: #ff0000;
#                 color: #fff;
#                 border: none;
#                 border-radius: 5px;
#                 padding: 8px;
#                 cursor: pointer;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Get the search query from the user
#     search_query = st.text_input("Search", "", key="search_input")
#
#     # Handle the search button click
#     if st.button("Search", key="search_button"):
#         save_query(search_query)
#
#     # Read the last query from the database
#     query = get_last_query()
#
#     # Define a function to process and display videos
#     def display_videos(query):
#         keywords = extract_keywords(query)
#         refined_query = create_query_parallel(keywords)
#         print(refined_query)
#         videos = search_videos(refined_query)
#         for video in videos:
#             video_title = video['snippet']['title']
#             video_id = video['id']['videoId']
#             video_url = f"https://www.youtube.com/watch?v={video_id}"
#             st.subheader(video_title)
#             st.video(video_url)
#         return refined_query
#
#     # Display videos for the initial search query
#     display_videos(query)
#
#     # Handle Filter 1 button click
#     if st.button('Apply Filter 1'):
#         refined_query1 = display_videos(query)
#         save_query(refined_query1)
#
#     # Handle Filter 2 button click
#     if st.button('Apply Filter 2'):
#         refined_query2 = display_videos(query)
#         save_query(refined_query2)
import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from yake import KeywordExtractor
import cohere

genai.configure(api_key=st.secrets["genai_api_key"])
tags = []
query = ''
def generate_tags():
    model = genai.GenerativeModel('gemini-1.5-pro')
    tags_prompt = 'Generate random educational tags like this subject1, subject2, subject3, subject4 etc. just plain text. just a few of them. bring advanced and diverse subject'
    response = model.generate_content(tags_prompt)
    response = response.text.split(', ')
    n_tags = []
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        tags_prompt = 'Generate random educational tags like this subject1, subject2, subject3, subject4 etc. just plain text. just a few of them. bring advanced and diverse subject'
        response = model.generate_content(tags_prompt)
        n_tags = response.text.split(', ')
    except Exception:
        try:
            api_key = st.secrets["cohere_api_key"]
            co = cohere.Client(api_key)
            prompt = "Generate random educational tags in horizontal sentence. just a few of them but diverse in subject. bring advanced and diverse subject. no comments"
            response = co.generate(
                model="command-nightly",
                prompt=prompt,
                max_tokens=50,
                temperature=0.8
            )
            response.generations[0].text.split(', ')
        except Exception:
            st.error("Exceed LLMs APIs Limit. Please Wait for a minute.")
    finally:
        return n_tags[:-1]

def create_query_gemini(keywords):
    model = genai.GenerativeModel('gemini-1.5-pro')
    tags_prompt = f'Generate a topic to search with these keywords {keywords}. Generate in simple plain text. No colon just texts. Make it creative.'
    response = model.generate_content(tags_prompt)
    return response.text

def create_query_cohere(keywords):
    api_key = st.secrets["cohere_api_key"]
    co = cohere.Client(api_key)
    prompt = f"Please create a question for YouTube in just a single sentence in plain text from these topics {keywords}. For education"
    response = co.generate(
        model="command-light",
        prompt=prompt,
        max_tokens=40,
        temperature=0.8
    )
    return response.generations[0].text

def create_query_parallel(keywords):
    n_query = ''
    try:
        n_query = create_query_gemini(keywords)
    except Exception:
        try:
            n_query = create_query_cohere(keywords)
        except Exception:
            st.error("Exceed LLMs APIs Limit. Please Wait for a minute.")
    finally:
        return n_query

def search_videos(query, api_key=st.secrets["youtube_api_key"]):
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=6
    ).execute()
    return search_response.get('items', [])

def extract_keywords(query):
    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(query)
    return [key[0] for key in keywords]

def show_videos(n_query):
    videos = search_videos(n_query)
    for video in videos:
        video_title = video['snippet']['title']
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        st.subheader(video_title)
        st.video(video_url)

def rephrase(n_query):
    keywords = extract_keywords(n_query)
    refined_query = create_query_parallel(keywords)
    return refined_query
def deep_search():
    global query
    st.markdown(
        """
        <style>
            .st-d6 {
                display: flex;
                align-items: center;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                margin: 10px 0;
            }
            .st-d7 {
                flex: 1;
                border: none;
                outline: none;
                padding: 0 8px;
            }
            .st-d8 {
                background-color: #ff0000;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 8px;
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Get the search query from the user
    search_query = st.text_input("Search", "", key="search_input")

    # Handle the search button click
    if st.button("Search", key="search_button"):
        query = search_query

    if query != '':
        refined_query1 = rephrase(query)
        refined_query2 = rephrase(query)

        # Handle Filter 1 button click
        show_videos(refined_query1)
        if st.button('Apply Filter 1'):
            query = refined_query1

        # Handle Filter 2 button click
        show_videos(refined_query2)
        if st.button('Apply Filter 2'):
            query = refined_query2
