import requests
import csv
import os
from github import Github

# GitHub 配置
github_token = os.getenv("MY_GITHUB_TOKEN")
repo_name = "jzhou9096/jilianip"  # 替换为你的 GitHub 仓库路径
file_path = "yxip.txt"  # 存储 IP 列表的文件路径
commit_message = "Update bestcf IP list"

# API 地址
csv_url = "https://ipdb.030101.xyz/bestcf/api/bestcf.csv"
custom_suffix = "可变"  # 可自定义后缀
limit_count = 10  # 限制提取前 5 个 IP，改成 10 以提取 10 个

def download_csv(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_ips(csv_content):
    ips = []
    reader = csv.reader(csv_content.splitlines())
    for row in reader:
        if row and row[0].count('.') == 3:  # 简单检查 IPv4 地址格式
            ips.append(f"{row[0]}#{custom_suffix}")
        if len(ips) >= limit_count:  # 达到限制数量后停止
            break
    return ips

def upload_to_github(token, repo_name, file_path, content, commit_message):
    g = Github(token)
    repo = g.get_repo(repo_name)
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file.path, commit_message, content, file.sha)
    except:
        repo.create_file(file_path, commit_message, content)

def main():
    csv_content = download_csv(csv_url)
    ip_list = extract_ips(csv_content)
    file_content = "\n".join(ip_list)
    upload_to_github(github_token, repo_name, file_path, file_content, commit_message)
    print("Upload completed.")

if __name__ == "__main__":
    main()
