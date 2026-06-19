from llama_cpp import Llama, LlamaRAMCache
from huggingface_hub import hf_hub_download
from linux_assistant.models.config import SYSTEM_PROMPT, SHOW_THINKS,\
                                        REPO_ID, GENERATION_MODEL
from linux_assistant.utils.dicts import AgentState
from rich.progress import Progress, SpinnerColumn, TextColumn

class model_nodes:
    def __init__(self):
        self.model = self.build_model()
        self.cache = LlamaRAMCache(capacity_bytes=512 << 20)
        self.model.set_cache(self.cache)
    def call_model(self, state: AgentState) -> AgentState:
        ''' A node to call model '''
        if len(state['messages']) == 1:
            system_message = {'role':'system', 'content': SYSTEM_PROMPT} 
            state['messages'] = [system_message] + state['messages']
        
        stream = self.model.create_chat_completion(
                messages=state['messages'],
                temperature=0.7,
                top_p=0.95,
                min_p=0.05,        
                top_k=40,    
                stream=True,
            )
        is_think_generated = False
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=not SHOW_THINKS,) as prog:
            task = prog.add_task("Thinking...", total=None)
            response_content = ""
            for chunk in stream:
                chunk = chunk["choices"][0]["delta"].get("content", "")
                response_content += chunk
                if SHOW_THINKS:
                    prog.update(task, description=response_content, end = '', flush = True)
                if chunk == '</think>':
                    is_think_generated = True
                    break
        tmp = True
        dont_show = False
        for chunk in stream:     
            chunk = chunk["choices"][0]["delta"].get("content", "")
            response_content += chunk
            if (is_think_generated and (chunk == 'shell' or chunk == 'search' or chunk == '```')) or dont_show:
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
    @staticmethod
    def build_model():
        ''' A function to define the LM '''
        model_path = hf_hub_download(repo_id=REPO_ID, filename=GENERATION_MODEL, local_dir="./model")
        return Llama(
            model_path=model_path,
            n_ctx=2**14,                    
            n_gpu_layers=10,               
            chat_format='qwen',
            verbose=False,
        )