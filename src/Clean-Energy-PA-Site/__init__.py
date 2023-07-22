print("Vlad Testing Source")
import os 

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_parser_path = os.path.abspath(os.path.join(path, "web_parser")) 
import sys 
print("Vlad Testing Source", path)
print("Vlad Testing Source", web_parser_path)

sys.path.append(path)
sys.path.append(web_parser_path)
print("Printing sys path", sys.path)
