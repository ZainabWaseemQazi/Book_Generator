from openai import OpenAI
from app.config import OPENAPI_API_KEY

client=OpenAI(api_key=OPENAPI_API_KEY)


def summarize_search_content(search_content):
    prompt = f"""
    Summarize this research content in short bullet points.

    Content:
    {search_content}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content

def generate_outline(title, notes, research_summary):
    prompt = f"""Generate a concise book outline with the title '{title}' 

                 Editor notes: {notes}
                 Use only the following sources when answering: {research_summary}"""
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()    

def regenerate_outline(old_outline, notes,  research_summary):

    prompt = f"""Improve this outline according to notes

                 Exixting outline: {old_outline}

                 Editor notes: {notes}
                 Use only the following sources when answering: {research_summary}"""
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_chapter(title, chapter_title, research_summary, context=""):
    prompt=f"""
        Book title: {title}

        previous chapter context: {context}

        Write chapter: {chapter_title}

        Use only the following sources when answering: {research_summary}

        Keep it around 100 words """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def regenerate_chapter(old_chapter, notes, research_summary, context=""):
    prompt=f"""
        previous chapter context: {context}

        Editor notes: {notes}

        Improve this chapter: {old_chapter}

        Use only the following sources when answering: {research_summary}

        Keep it around 100 words
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_summary(chapter_text,):
    prompt=f"""
        Summarize this chapter in 2-3 sentences: {chapter_text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()