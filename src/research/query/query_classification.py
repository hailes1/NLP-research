def classify_query(query, model="meta-llama/Llama-3.2-3B-Instruct"):
    """
    Classify a query into one of four categories: Factual, Analytical, Opinion, or Contextual.
    --Probably won't use this, for a bit: Might want to focus on the analytical query and generate an answer from the vector embedding. 
    
    Args:
        query (str): User query
        model (str): LLM model to use
        
    Returns:
        str: Query category
    """
    # Define the system prompt to guide the AI's classification
    system_prompt = """You are an expert at classifying questions. 
        Classify the given query into exactly one of these categories:
        - Factual: Queries seeking specific, verifiable information.
        - Analytical: Queries requiring comprehensive analysis or explanation.
        - Opinion: Queries about subjective matters or seeking diverse viewpoints.
        - Contextual: Queries that depend on user-specific context.

        Return ONLY the category name, without any explanation or additional text.
    """

    # Create the user prompt with the query to be classified
    user_prompt = f"Classify this query: {query}"
    
    # Generate the classification response from the AI model
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    
    # Extract and strip the category from the response
    category = response.choices[0].message.content.strip()
    
    # Define the list of valid categories
    valid_categories = ["Factual", "Analytical", "Opinion", "Contextual"]
    
    # Ensure the returned category is valid
    for valid in valid_categories:
        if valid in category:
            return valid
    
    # Default to "Factual" if classification fails
    return "Factual"