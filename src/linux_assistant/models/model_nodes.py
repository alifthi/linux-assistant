import json
from llama_cpp import Llama, LlamaRAMCache
from huggingface_hub import hf_hub_download
from linux_assistant.utils.dicts import AgentState
from rich.progress import Progress, SpinnerColumn, TextColumn
from linux_assistant.utils.config_handler import config
class model_nodes:
    def __init__(self, model_config: config):
        self.config = model_config
        self.model = self.build_model()
        self.cache = LlamaRAMCache(capacity_bytes=512 << 20)
        self.model.set_cache(self.cache)
    
    def get_codes(self, stream, response_content):
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=not self.config.config['show_thinking'],) as prog:
            task = prog.add_task("💻 Code generation....", total=None)
            for chunk in stream:
                chunk = chunk["choices"][0]["delta"].get("content", "")
                response_content += chunk
                if chunk == '```':
                    break
        return response_content
             
    def call_model(self, state: AgentState) -> AgentState:
        ''' A node to call model '''
        if len(state['messages']) == 1:
            system_message = {'role':'system', 'content': self.config.get_system_prompt()} 
            state['messages'] = [system_message] + state['messages']
        

        is_think_generated = False
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=not self.config.config['show_thinking'],) as prog:
            
            task = prog.add_task("Thinking...", total=None)
            
            stream = self.model.create_chat_completion(
                    messages=state['messages'],
                    temperature=0.7,
                    top_p=0.95,
                    min_p=0.05,        
                    top_k=40,    
                    stream=True,
                )            
            response_content = ""
            for chunk in stream:
                chunk = chunk["choices"][0]["delta"].get("content", "")
                response_content += chunk
                if self.config.config['show_thinking']:
                    prog.update(task, description=response_content, end = '', flush = True)
                if chunk == '</think>':
                    is_think_generated = True
                    continue
                if is_think_generated and not (chunk == 'shell' or chunk == 'search' or chunk == '```'):
                    break
                    
        tmp = True
        dont_show = False
        for chunk in stream:     
            chunk = chunk["choices"][0]["delta"].get("content", "")
            response_content += chunk
            if (is_think_generated and (chunk == 'shell' or chunk == 'search' or chunk == '```')) or dont_show:
                response_content = self.get_codes(stream, response_content)
                dont_show = True
                continue
            if tmp:
                if chunk == '\n\n': 
                    continue
                tmp = False
                state['logger'].print_text(' ➜ ', color = 'yellow')
            state['logger'].print_text(chunk, color='white') 
        print('\n')
        state['messages'].append({'role':'assistant', 'content': response_content})
        return state
    def build_model(self):
        ''' A function to define the LM '''
        model_path = hf_hub_download(repo_id=self.config.get_repo_id(),
                                    filename=self.config.get_model_name(),
                                    local_dir="./model")
        model = Llama(
            model_path=model_path,
            n_ctx=2**15,                    
            n_gpu_layers=10,               
            chat_format='qwen',
            verbose=False,
        )
        cache = LlamaRAMCache()
        model.set_cache(cache)
        
        return model