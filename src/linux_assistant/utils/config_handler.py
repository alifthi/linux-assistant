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
        '''Save config file'''
        with open(self._config_path, 'w') as file:
            json.dump(self.config, file, indent=4)
    
    def _show_model_details(self):
        pass
    
    def change_model(self, selected_model):
        '''Change the model in use and put the old model in to_use_models list'''
        if selected_model == self.config['in_use_model']['generator']:
            return False
        for model in self.config['to_use_models']:
            if model['generator'] == selected_model:
                old_model = self.config['in_use_model']
                self.config['in_use_model'] = model
                self.config['to_use_models'].remove(model)
                self.config['to_use_models'].append(old_model)
                break
        self._save_config()
        return True
    def _change_system_prompt(self):
        pass
    
    def get_system_prompt(self):
        '''Get system prompt for current model'''
        return self.system_prompt[f"{self.get_repo_id()}/{self.get_model_name()}"]
    
    def get_repo_id(self):
        ''''Get repo id for current model'''
        return self.config['in_use_model']["repo_id"]
    
    def get_model_name(self):
        '''Get model name for current model'''
        return self.config['in_use_model']["generator"]
    
    def get_models_list(self):
        '''Get the list of available models'''
        models = [self.config['in_use_model']['generator']]
        for model in self.config['to_use_models']:
            models.append(model['generator'])
        return models