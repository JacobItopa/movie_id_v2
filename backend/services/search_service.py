import os
from tavily import TavilyClient

async def search_movie_links(title: str, year: str) -> list[dict]:
    """
    Searches Tavily for where to stream or watch the identified movie.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
         raise ValueError("TAVILY_API_KEY is missing")

    client = TavilyClient(api_key=tavily_key)
    query = f"Where to watch stream '{title}' movie {year} official links Netflix Amazon Hulu Max Apple TV"
    
    print(f"Searching Tavily: {query}")
    try:
        # We perform a basic search and extract top results
        response = client.search(query=query, search_depth="basic", max_results=5)
        
        links = []
        for result in response.get("results", []):
            links.append({
                 "title": result.get("title", ""),
                 "url": result.get("url", ""),
                 "content": result.get("content", "")
            })
            
        return links
    except Exception as e:
        print(f"Error searching Tavily: {e}")
        return []
