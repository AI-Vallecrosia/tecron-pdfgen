import os
import warnings as warn
import re
import datetime as dt
import tarfile as tar
import shutil as sh
from io import BytesIO
import requests as rq
import bs4
import PyPDF2 as pypdf
import  playwright.sync_api as plw

def init(s,config):
    OUTPUT_TARGZ=config["OUTPUT_TARGZ"]
    TARGZ_DIR=config["TARGZ_DIR"]
    if OUTPUT_TARGZ:
        os.makedirs(TARGZ_DIR, exist_ok=True)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Referer": config["URL_ROOT"]+"Intestazione.htm",
        "DNT": "1",
        "Host": config["DOMAIN"],
        "Pragma": "no-cache",
        "Priority": "u=4",
        "Sec-Fetch-Dest": "frame",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0"
    }
    r=s.get(config["URL_ROOT"]+"AreaRiservataFornitori.asp",timeout=10,headers=headers)
    r.raise_for_status()
    with open(config["PASSWORD_FILE"],"r",encoding='utf8') as f:
        password=f.read().strip()
    if password is None or password == "":
        raise Exception("Empty password not allowed")
    query_payload=f"TerminalID=&CodiceInternetTecnico={password}&Citta=&Pv=&StatoIntervento=Da+Eseguire&Esercente=&Gruppo=E"
    headers.update(
        {
            "Origin": config["URL"],
            "Referer": config["URL_ROOT"]+"AreaRiservataFornitori.asp",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    r=s.post(config["URL_ROOT"]+"AreaRiservataFornitori.asp",data=query_payload,timeout=10,headers=headers)
    r.raise_for_status()
    if int(r.headers["content-length"]) <= config["EMPTY_DATA_LENGTH"]:
        warn.warn("Empty data returned, Can be a wrong password...")
    soup = bs4.BeautifulSoup(r.text,features='html.parser')
    soup=soup.body.find_all("table")[-1]
    soup=soup.find_all("a")
    links=[l for l in map(lambda x: x.get('href'),soup) if "VerbaleInterventoSCELTA" in l ]
    IDs=[ID.group(1) for ID in map(config["REGEX_ID"].search,links)]
    return IDs

def PDF_from_id(s,page,ID,config):
    TARGZ_DIR=config["TARGZ_DIR"]
    URL_ROOT=config["URL_ROOT"]
    OUTPUT_TARGZ=config["OUTPUT_TARGZ"]
    file_name=f"{ID}"
    r=s.get(URL_ROOT+"VerbaleInterventoFornitore.asp",params={"id": ID},timeout=10)
    r.raise_for_status()
    soup=bs4.BeautifulSoup(r.text,features='html.parser')
    html_string=soup.prettify()
    page.set_content(html_string)
    curr_doc=page.pdf(format="A4")
    
    if OUTPUT_TARGZ:
        file_path=f"{TARGZ_DIR}/{file_name}"
        with open(f"{file_path}.html","w",encoding='utf-8') as f:
            f.write(html_string)
        with open(f"{file_path}.pdf","wb") as f:
            f.write(curr_doc)
    return BytesIO(curr_doc)

def end(merger,config):
    DOWNLOAD_DIR=config["DOWNLOAD_DIR"]
    pdf_name=config["PDF_NAME"]
    TARGZ_DIR=config["TARGZ_DIR"]
    OUTPUT_TARGZ=config["OUTPUT_TARGZ"]
    merger.write(f"{DOWNLOAD_DIR}/{pdf_name}.pdf")
    if OUTPUT_TARGZ:
        with tar.open(f"{TARGZ_DIR}.tar.gz","w:gz") as t:
            t.add(TARGZ_DIR,arcname=os.path.basename(TARGZ_DIR))
        sh.rmtree(TARGZ_DIR)

def main(prog=None):
    today=dt.datetime.now().strftime("%y%m%d")
    DOMAIN=os.getenv("TECRON_DOMAIN")
    config={
        "DOMAIN": DOMAIN,
        "TARGZ_NAME": f"{today}",
        "PDF_NAME": f"{today}",
        "EMPTY_DATA_LENGTH": 5500,
        "REGEX_ID": re.compile("id=([0-9]+)"),
        "DOWNLOAD_DIR": os.getenv("TECRON_DOWNLOAD_DIR"),
        "TARGZ_DIR": os.getenv("TECRON_DOWNLOAD_DIR")+f"/{today}",
        "OUTPUT_TARGZ": os.getenv("TECRON_TARGZ") is not None,
        "PASSWORD_FILE": os.getenv("TECRON_PASSWORD_FILE"),
        "URL": f"https://{DOMAIN}",
        "URL_ROOT": f"https://{DOMAIN}/"
    }
    merger=pypdf.PdfMerger()
    with rq.Session() as s:
        IDs=init(s,config)
        nIDs=len(IDs)
        with plw.sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            for ID in IDs:
                if prog is not None:
                    prog.step(1.0/nIDs)
                merger.append(PDF_from_id(s,page,ID,config))
            browser.close()
    end(merger,config)


