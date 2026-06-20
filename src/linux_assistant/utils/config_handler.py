import json

class config:
    
    def __init__(self):
        self.config = None
        self._config_path = "linux_assistant/config.json"
        self._load_config()
        self.system_prompt = ""
        
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