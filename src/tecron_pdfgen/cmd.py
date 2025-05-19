
import os
import argparse
from .gui import gui
from .main import main

def cmd():
    home=os.getenv('HOME')
    DATA_DIR=os.getenv('XDG_DATA_HOME', f"{home}/.local/share")+"/tecron_pdfgen"
    DOWNLOAD_DIR=os.getenv('XDG_DOWNLOAD_DIR', f"{home}/Downloads")+"/tecron_pdfgen"
    os.makedirs(DOWNLOAD_DIR,exist_ok=True)
    parser = argparse.ArgumentParser()
    default_DOMAIN=os.getenv('TECRON_DOMAIN', 'www.tecron.it')
    parser.add_argument('-d','--domain',type=str, help='Domain name', default=default_DOMAIN)
    default_PASSWORD_FILE=os.getenv('TECRON_PASSWORD_FILE', f"{DATA_DIR}/password.secret")
    parser.add_argument('-p','--password-file',type=str,help='Password file path', default=default_PASSWORD_FILE)
    default_DOWNLOAD_DIR=os.getenv('TECRON_DOWNLOAD_DIR', DOWNLOAD_DIR)
    parser.add_argument('-o','--download-dir',type=str, help='Output directory', default=os.getenv('OUTPUT_DIR', default_DOWNLOAD_DIR))
    parser.add_argument('-x','--output-targz', help='Output tar.gz containing single html and pdf',action='store_true')
    parser.add_argument('--gui', help='Start command gui mode',action='store_true')
    args = parser.parse_args()

    os.environ['TECRON_DOMAIN'] = args.domain
    os.environ['TECRON_PASSWORD_FILE'] = args.password_file
    os.environ['TECRON_DOWNLOAD_DIR'] = args.download_dir
  
    if args.output_targz:
        os.environ['TECRON_TARGZ']='1'
    
   
    if args.gui:
        gui()
    else:
        main()

if __name__ == "__main__":
    cmd()