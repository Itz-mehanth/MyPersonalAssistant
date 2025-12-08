import requests
from bs4 import BeautifulSoup

def get_user_details(rank):
    url = f"https://leetcode.com/contest/globalranking/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Find the user by rank in the leaderboard table
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[0].text.strip() == str(rank):
            username = cols[1].text.strip()
            score = cols[2].text.strip()
            return {"rank": rank, "username": username, "score": score}
    return None

rank = 50  # Example rank
print(get_user_details(rank))