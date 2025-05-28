def geminiStoryGenerator(apiKey, prompt, geminiModel="gemini-2.0-flash"):
    """
    This function generates a story about Gemini.
    """
    from google import genai

    client = genai.Client(api_key=apiKey)

    response = client.models.generate_content(
        model=geminiModel, contents=prompt
    )
    return(response.text)

def openAIStoryGenerator():
    """
    This function generates a story about OpenAI.
    """
    story = (
        "OpenAI is an artificial intelligence research organization that aims to ensure "
        "that artificial general intelligence (AGI) benefits all of humanity. Founded in "
        "December 2015, OpenAI conducts research in various fields of AI, including "
        "natural language processing, robotics, and machine learning. The organization "
        "is known for its commitment to safety and ethical considerations in AI development."
    )
    return story

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

