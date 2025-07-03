import time
def geminiStoryGenerator(apiKey, prompt, geminiModel="gemini-2.0-flash", max_retries=5, backoff=2):
    """
    This function generates a story about Gemini.
    """
    from google import genai

    client = genai.Client(api_key=apiKey)


    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=geminiModel,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(backoff ** attempt)  # Exponential backoff
            else:
                raise  # Re-raise after final failure

def openAIStoryGenerator(apiKey, prompt, model="gpt-4o", use_web: bool = True):
    from openai import OpenAI
    import os

    client = OpenAI(api_key=apiKey)

    payload = {"model": model, "input": prompt}
    if use_web:
        payload["tools"] = [{"type": "web_search_preview"}]
    resp = client.responses.create(**payload)
    return resp.output_text




def deepSeekStoryGenerator():
    """
    This function generates a story about DeepSeek.
    """
    story = (
        "DeepSeek is a cutting-edge technology company that specializes in deep learning "
        "and artificial intelligence solutions. Founded by a team of experts in the field, "
        "DeepSeek focuses on developing innovative algorithms and models that can analyze "
        "large datasets and extract valuable insights. The company's mission is to empower "
        "businesses with AI-driven tools that enhance decision-making and drive growth."
    )
    return story

