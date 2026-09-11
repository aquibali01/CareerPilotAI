import requests

def fetch_github_user_data(username: str) -> dict:
    """
    Fetches public repositories, top languages, and README snippets for a given GitHub username.
    """
    if not username:
        return {"error": "Username is empty", "repos": []}

    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"GitHub user not found or API error (Status {response.status_code})", "repos": []}
        
        repos_data = response.json()
        
        parsed_repos = []
        all_languages = set()

        for repo in repos_data[:15]:  # Process top 15 updated repos
            if repo.get("fork"):
                continue  # Skip forks to check original work
            
            repo_name = repo.get("name")
            lang = repo.get("language")
            if lang:
                all_languages.add(lang)

            parsed_repos.append({
                "name": repo_name,
                "description": repo.get("description", ""),
                "language": lang,
                "stars": repo.get("stargazers_count", 0),
                "topics": repo.get("topics", [])
            })

        return {
            "username": username,
            "total_repos_analyzed": len(parsed_repos),
            "detected_languages": list(all_languages),
            "repos": parsed_repos
        }

    except Exception as e:
        print(f"Error fetching GitHub data: {e}")
        return {"error": str(e), "repos": []}