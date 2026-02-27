import requests, os, re, bs4, sys, json, time, random, subprocess, logging, base64, uuid
from time import sleep
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
ses = requests.Session()

COLORS = ["yellow", "magenta", "green", "red"]

ua_random = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.58 Mobile Safari/537.36'

def banner():
    grid = '''[bold magenta]
   ██████╗██╗  ██╗ █████╗ ██████╗ ███████╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝
╚█████╗ ███████║███████║██████╔╝█████╗
 ╚═══██╗██╔══██║██╔══██║██╔══██╗██╔══╝
  ██████╔╝██║  ██║██║  ██║██║  ██║███████╗
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝'''

    console.print(Panel(grid, style="bold blue", width=70, subtitle="[bold yellow]Facebook Auto Share Tool"), justify="center")

def menu_logo():
    os.system("clear" if os.name == "posix" else "cls")
    banner()

def login():
    # Force remove old session files before logging in
    if os.path.exists("token.txt"): os.remove("token.txt")
    if os.path.exists("cookie.txt"): os.remove("cookie.txt")
    
    menu_logo()
    
    status_info = "[bold cyan]TAKE COOKIES FROM KIWI BROWSER."
    console.print(Panel(status_info, title='[bold cyan]Modified by ray', style="magenta", width=70))
    
    cookie = console.input("[bold cyan] └──> [bold magenta]Enter Cookie :")
    
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
            "referer": "https://www.facebook.com/",
            "host": "business.facebook.com",
            "origin": "https://business.facebook.com",
            "upgrade-insecure-requests": "1",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "content-type": "text/html; charset=utf-8",
            "cookie": cookie
        }
        
        data = ses.get("https://business.facebook.com/business_locations", headers=headers)
        
        find_token = re.search("(EAAG\w+)", data.text)
        token = find_token.group(1)
        
        with open("token.txt", "w") as f: f.write(token)
        with open("cookie.txt", "w") as f: f.write(cookie)
        
        console.print(Panel("Login Successful! Access Token Saved.", style="bold green", width=45))
        time.sleep(2)
        start_sharing()
        
    except Exception:
        if os.path.exists("token.txt"): os.remove("token.txt")
        if os.path.exists("cookie.txt"): os.remove("cookie.txt")
        
        console.print(Panel("Invalid Cookie! Please try again.", title="[bold red]Error", style="red", width=45))
        time.sleep(2)
        login()
                
def start_sharing():
    try:
        if not os.path.exists("token.txt") or not os.path.exists("cookie.txt"):
            login()
            return
            
        token = open("token.txt","r").read()
        cok = open("cookie.txt","r").read()
        cookie = {"cookie":cok}
        
        menu_logo()
        
        user_data = ses.get(f"https://b-graph.facebook.com/me?fields=name,id&access_token={token}", cookies=cookie).json()
        name = user_data.get("name", "Unknown User")
        uid = user_data.get("id", "Unknown ID")
        
        info_panel = f"[bold white]Account Name : [bold green]{name}\n[bold white]Account ID   : [bold green]{uid}"
        console.print(Panel(info_panel, title="[bold yellow]User Session", style="cyan", width=70))

        console.print("[bold cyan] ┌─[[bold white]Post Link[/bold cyan]]")
        link = console.input("[bold cyan] └──> : ")
        
        console.print("[bold cyan] ┌─[[bold white]Share Limit[/bold cyan]]")
        amount = int(console.input("[bold cyan] └──> : "))

        console.print("[bold cyan] ┌─[[bold white]Share Delay (Seconds)[/bold cyan]]")
        delay_time = int(console.input("[bold cyan] └──> : "))

        console.print(Panel(f"[bold green]Starting process for {amount} shares...", style="bold white", width=70))
        
        count = 0
        for i in range(amount):
            count += 1
            response = ses.post(f"https://b-graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}", cookies=cookie).json()
            
            if "id" in response:
                raw_id = response.get("id")
                post_id = raw_id.split('_')[-1] if '_' in raw_id else raw_id
                
                console.print(f"[bold cyan] [[bold green]{count}[/bold cyan]] [bold white]Successfully shared! Post ID: [bold cyan]{post_id}")
                time.sleep(delay_time) 
            else:
                err_msg = response.get("error", {}).get("message", "Sharing blocked or Cookie expired.")
                console.print(Panel(f"{err_msg}", title="[bold red]Failed", style="red", width=70))
                break
                
    except Exception as e:
        console.print(Panel(f"Error: {str(e)}", style="bold red", width=70))
        time.sleep(2)
        login()
        

if __name__ == "__main__":
    login()
