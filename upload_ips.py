import os
from github import Github

# 获取 GitHub Token（使用自定义 secret）
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")  # 获取环境变量

if GITHUB_TOKEN is None:
    print("Error: MY_GITHUB_TOKEN is not set.")
    exit(1)

REPO_NAME = "jzhou9096/jilianip"  # 替换为你的仓库
FILE_PATH = "FLJAPI.txt"  # 替换为文件路径（如 data.txt）
WEBPAGE_URL = "https://tqyb.jzhou9096.workers.dev"  # 替换为目标网页 URL

def fetch_webpage_content(url):
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def write_to_github(content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        file = repo.get_contents(FILE_PATH)
        repo.update_file(FILE_PATH, "Updated content", content, file.sha, branch="main")
        print("File updated successfully on GitHub.")
    except Exception as e:
        print(f"Error writing to GitHub: {e}")

def main():
    print("Fetching webpage content...")
    content = fetch_webpage_content(WEBPAGE_URL)
    if content:
        print("Writing content to GitHub...")
        write_to_github(content)

if __name__ == "__main__":
    main()
