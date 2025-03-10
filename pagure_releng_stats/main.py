import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import datetime

# Pagure Releng Repository URL
REPO_URL = "https://pagure.io/releng/issues"
API_URL = "https://pagure.io/api/0/releng/issues"

def fetch_issues():
    issues = []
    page = 1
    while True:
        response = requests.get(API_URL, params={"page": page, "per_page": 100})  # Fetch 100 issues per request
        if response.status_code == 200:
            data = response.json().get("issues", [])
            if not data:
                break  # Stop when no more issues are returned
            issues.extend(data)
            page += 1
        else:
            break  # Stop fetching if there's an error
    return issues

# Call the function and print the total fetched issues
issues = fetch_issues()
print("Fetched total issues:", len(issues))  # Debugging statement

# Process Issues Data
open_issues = [issue for issue in issues if issue["status"] == "Open"]
closed_issues = [issue for issue in issues if issue["status"] == "Closed"]
print("Open Issues:", len(open_issues))  # Debugging statement
print("Closed Issues:", len(closed_issues))  # Debugging statement

# Weekly Opened vs Closed Issues
week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
def filter_by_week(issue):
    print("Raw date_created:", issue["date_created"])  # Debugging statement
    try:
        updated = datetime.datetime.fromtimestamp(int(issue["date_created"]))  # Ensure conversion to int
        print("Converted timestamp to datetime:", updated)  # Debugging statement
        return updated >= week_ago
    except ValueError as e:
        print("Error converting timestamp:", e)  # Debugging statement
        return False

weekly_opened = len([issue for issue in open_issues if filter_by_week(issue)])
weekly_closed = len([issue for issue in closed_issues if filter_by_week(issue)])
print("Weekly Opened:", weekly_opened)  # Debugging statement
print("Weekly Closed:", weekly_closed)  # Debugging statement

# Tag Analysis
all_tags = [tag for issue in issues for tag in issue.get("tags", [])]
tag_counts = Counter(all_tags)
print("Tag Counts:", tag_counts)  # Debugging statement

# Assigning Story Points
story_points = {"high-trouble": 5, "medium-trouble": 3, "low-trouble": 1,
                "high-gain": 5, "medium-gain": 3, "low-gain": 1}
issue_points = []
for issue in issues:
    points = sum(story_points.get(tag, 0) for tag in issue.get("tags", []))
    issue_points.append({"id": issue["id"], "title": issue["title"], "points": points})
print("Issue Story Points:", issue_points[:5])  # Debugging statement

# Handling Unassigned Tickets
for issue in open_issues:
    if not issue.get("assignee", None):
        issue["assignee"] = "Samyak (releng user)"

# Data Visualization
# 1. Open vs Closed Issues
plt.figure(figsize=(6,6))
plt.bar(["Open", "Closed"], [len(open_issues), len(closed_issues)], color=["red", "green"])
plt.title("Open vs Closed Issues")
plt.ylabel("Number of Issues")
plt.show(block=True)  # Ensures the window stays open

# 2. Weekly Opened vs Closed Issues
plt.figure(figsize=(6,6))
plt.bar(["Opened This Week", "Closed This Week"], [weekly_opened, weekly_closed], color=["blue", "orange"])
plt.title("Weekly Opened vs Closed Issues")
plt.ylabel("Number of Issues")
plt.show(block=True)  # Ensures the window stays open

# 3. Tags Distribution
plt.figure(figsize=(8,6))
plt.bar(tag_counts.keys(), tag_counts.values(), color="purple")
plt.xticks(rotation=45, ha="right")
plt.title("Issue Tags Distribution")
plt.ylabel("Number of Issues")
plt.show(block=True)  # Ensures the window stays open

# 4. Story Points Distribution
df_points = pd.DataFrame(issue_points)
print(df_points)  # Display the DataFrame in the console
df_points.to_csv("issue_story_points.csv", index=False)  # Save as CSV file
print("Issue Story Points saved to issue_story_points.csv")
