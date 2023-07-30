import toml
from packaging import version
import re

def get_evaluation_values():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    table = re.search(r"(?<=## Evaluation\n\n)[\s\S]*",content).group(0)
    
    pattern = r"\|(\s*[\w\s]+)\s*\|\s*\*\*(\d+\.\d+)\%\*\*\s*\|"
    matches = re.findall(pattern, table)
  
    evaluation_values = {module.strip(): float(value) for module, value in matches}

    return evaluation_values


def define_env(env):
    env.variables.pretrained_models="https://github.com/roshan-research/hazm#pretrained-models"
    env.variables.lemmatizer_evaluation_value = get_evaluation_values()["Lemmatizer"]
    env.variables.posTagger_evaluation_value =  get_evaluation_values()["POSTagger"]
    env.variables.dependency_parser_evaluation_value = get_evaluation_values()["DependencyParser"]
    env.variables.chunker_evaluation_value =  get_evaluation_values()["Chunker"]
    

    @env.filter
    def to_persian_numeral(number):    
        english_to_persian = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
        return ''.join(english_to_persian.get(digit, digit) for digit in str(number))

    @env.macro
    def needed_python_version():       
        with open('pyproject.toml', 'r') as f:
            toml_data = toml.load(f)
       
        python_reqs = toml_data.get('tool', {}).get('poetry', {}).get('dependencies', {}).get('python', '')

        versions = [version.parse(c.split('>=')[1]) for c in python_reqs.split(',') if c.startswith('>=')]
        min_version = "+"+str(min(versions)) if versions else ''       

        return min_version
    
    @env.macro
    def hazm_code_example():
        with open("README.md", 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        pattern = r"(?<=## Usage\n\n)```python[\s\S]*```"    

        return re.search(pattern, markdown_content).group(0)    
    
