from urllib.request import HTTPBasicAuthHandler
import requests


def get_clash_of_clans_stats(tag_name):
    """Fetch Clash of Clans player stats using API."""
    API_URL = f"https://api.clashofclans.com/v1/players/%23{tag_name}"
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU4ZDgzYjhlLWI3ZGQtNGEwMi05ZmY0LTkwZWE0MDkxMDRlOSIsImlhdCI6MTc0MTU5NDg5Nywic3ViIjoiZGV2ZWxvcGVyL2M2ZTA1ZmYzLTRiZTktYjIyYi1iYzZkLWQ4YTYzOTY0YWVmZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjQyLjEwNi4zOC43MCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.DD4BtSPZly2pr9_4M6JbDa_UoAk5VE_HiaFvMOeZ9geZnSegAqtuLmCgMUxyoe6dU26vqDEUUEHwQwmwIJv-qg"
    }

    response = requests.get(API_URL, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        return {
            "trophies": data.get("trophies", "N/A"),
            "townHallLevel": data.get("townHallLevel", "N/A"),
        }

    return {"error": "Failed to fetch stats"}


def get_brawl_stars_stats(tagName):
    print("Hello")
    API_URL = f"https://api.brawlstars.com/v1/players/%23{tagName}"
    headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM2NWNkZWUyLTUyNDAtNGJkMC04YjkyLTc1Y2U2YTk3ZjdhNyIsImlhdCI6MTc0MTU5NDk1Mywic3ViIjoiZGV2ZWxvcGVyL2VlNDAwZTlkLWZhNjctNWY1MC0wZjJkLWU1ZDAwMjdhOWRkZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDIuMTA2LjM4LjcwIl0sInR5cGUiOiJjbGllbnQifV19.vCiRu9o2A9x2ewN-2SEmTLucTntfQZWasIh2kV8xbE3GCquKH_UYtZwfxLaC_aEoCAHkZ72_rg8nZv926RoU8A"}
    response = requests.get(API_URL,headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        print(data.get("trophies", "N/A"))
        return {
           "trophies":data.get("trophies", "N/A"),
        }
    return None


def get_chess_com_stats(username):
    API_URL = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {
        "User-Agent": "ArenaConnect/1.0 (Contact: codeking1907@gmail.com)"
    }
    response = requests.get(API_URL, headers=headers)

    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        return {
            "rating": data.get("chess_rapid", {}).get("last", {}).get("rating", 0)
        }
    return {"error": f"Failed to fetch stats (status {response.status_code})"}

# Pending Will Complete it
def get_cod_stats(userId):
    API_URL = f"http://localhost:9022/api/{userId}"
    from requests.auth import HTTPBasicAuth
    response = requests.get(API_URL, auth=HTTPBasicAuth("Darshan", "Darshan@2604"))
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        return {
            "kd": data.get("kd", 0),
        }
    return None
