import sys
import os 
sys.path.append('.')
sys.path.append('./tests')

path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.abspath(os.path.join(path, "test")) 
sys.path.append(path)
sys.path.append(test_path)