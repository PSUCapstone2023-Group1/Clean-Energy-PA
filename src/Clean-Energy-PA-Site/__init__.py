import os 
import sys 

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_parser_path = os.path.abspath(os.path.join(path, "web_parser")) 

if path not in sys.path:     
    sys.path.append(path) 
    
if web_parser_path not in sys.path:
    sys.path.append(web_parser_path) 