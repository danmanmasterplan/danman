from ddgs import DDGS


def web_search(query):
    try:
        results = DDGS().text(query, max_results=10)
        search_results = []
        for result in results:
            search_results.append({
                "title": result.get("title", "No title"),
                "body": result.get("body", "No body"),
                "url": result.get("href", result.get("url", "No url")),
            })
        return search_results
    except Exception as error:
        print("Search error:", error)
        return []