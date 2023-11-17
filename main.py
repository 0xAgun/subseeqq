import requests, re, argparse, datetime, csv
from datetime import timedelta
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn
from rich import box



parser = argparse.ArgumentParser(description="Subdomain extracttor from c99.nl")
parser.add_argument('-d', '--domain', metavar='', required=True, help="Enter the url to scan")
parser.add_argument('-o', '--output', metavar='', required=False, help="Enter the filename to save the output")
parser.add_argument('-c', '--csv', metavar='', required=False, help="save the output to csv format including ip address")
args = parser.parse_args()



table = Table( style="bold green")
table.add_column("Subdomain", style="bold cyan", justify="center")
table.add_column("Ips", style="#5882FA", justify="center")
table2 = Table()
table2.add_column("Total Subdomain Found", style="bold cyan", justify="center")



def banner():
    note = '''
        ,_._._._._._._._._|__________________________________________________________,
        |_|_|_|_|_|_|_|_|_|_________________________________________________________/
                          !     
                                █▀ █░█ █▄▄ █▀ █▀▀ █▀▀ █▀█ █▀█
                                ▄█ █▄█ █▄█ ▄█ ██▄ ██▄ ▀▀█ ▀▀█


    '''
    markdown = Markdown(note, style="red")
    console = Console()
    console.print(Panel(markdown, title="Subdomain extracttor from c99.nl", subtitle="Author [0xAgun]", box=box.HEAVY, style="blue"))



def func(soup, ff):
    for link in soup.find_all("a"):
        if "href" in link.attrs:
            temp = link.attrs["href"].replace("//", "")
            if temp.startswith("subdomainfinder")  or temp.startswith("https") or temp.startswith("/whois") or temp.startswith("/cdn-cgi") or temp.startswith("/overview"):
                pass
            else:
                if temp.startswith("/"):
                    temp = temp[7:]
                    ff.append(temp)
                else:
                    ff.append(temp)

def main(url, headers):
    with Progress(SpinnerColumn()) as progress:
        task = progress.add_task("[cyan]Loading URL...", total=1, start=False)
        progress.start_task(task)
        current = datetime.datetime.now().strftime("%Y-%m-%d")
        req = requests.get("https://subdomainfinder.c99.nl/scans/"+current+"/"+url, headers=headers)
        find = True
        contunter = 0
        if "https://subdomainfinder.c99.nl/scans/"+current+"/"+url in req.text:
            soup = BeautifulSoup(req.text, "html.parser")
            ff = []
            func(soup, ff)
            progress.update(task, advance=1, completed=True, description="[cyan]URL Loaded")
        else:
            while find:
                if contunter == 30:
                    print("Tried 1 month No subdomain found")
                    exit()
                contunter += 1
                currents = datetime.datetime.now()
                final = currents - timedelta(days=contunter) 
                req = requests.get("https://subdomainfinder.c99.nl/scans/"+final.strftime("%Y-%m-%d")+"/"+url)
                if "https://subdomainfinder.c99.nl/scans/"+final.strftime("%Y-%m-%d")+"/"+url in req.text:
                    find = False
                    soup = BeautifulSoup(req.text, "html.parser")
                    ff = []
                    func(soup, ff)
                    progress.update(task, advance=1)
                

    count = 0            
    for x in range(1, len(ff) -1, 2):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip1 = re.findall(ip_pattern, ff[x])
        ip2 = re.findall(ip_pattern, ff[x+1])
        if ip1 and ip2:
            pass
        else:
            try:
                # print(ff[x], ff[x+1])
                count += 1
                # print(ff[x])
                table.add_row(f"{ff[x]} \n", f"{ff[x+1]} \n")
                if args.output:
                    with open(args.output, "a") as f:
                        f.write(ff[x] + "\n")
                if args.csv:
                    with open(args.csv, "a") as f:
                        writer = csv.writer(f)
                        writer.writerow([ff[x], ff[x+1]])
                        
            except Exception as e:
                print(e)
    table2.add_row(f"{count}")
    console = Console()
    console.print(table, table2)
    



if __name__ == "__main__":
    if args.csv:
        with open(args.csv, "a") as f:
            writer = csv.writer(f)
            writer.writerow(['Subdomain', 'Ip Address'])

    if args.domain:
        url = args.domain
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        banner()
        main(url, headers)

    


