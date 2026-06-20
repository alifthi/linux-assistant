import json
from linux_assistant.models.system_prompts import system_prompts
class config:
    
    def __init__(self):
        self.config = None
        self._config_path = "linux_assistant/config.json"
        self._load_config()
        self.system_prompt = system_prompts
                
    def _load_config(self):
        '''Load config file'''
        with open(self._config_path) as file:
            self.config = json.load(file)
        
    def _save_config(self):
        pass
    
    def _show_model_details(self):
        pass
    
    def _change_model(self):
        pass
    
    def _change_system_prompt(self):
        pass
    
    def get_system_prompt(self):
        return self.system_prompt[f"{self.get_repo_id()}/{self.get_model_name()}"]
    
    def get_repo_id(self):
        return self.config['in_use_model']["repo_id"]
    
    def get_model_name(self):
        return self.config['in_use_model']["generator"]