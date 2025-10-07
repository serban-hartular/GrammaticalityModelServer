from llama_cpp import Llama

def get_response(text : str, llm: Llama) -> str:
    prompt = [{'role':'user', 'content':text}]
    output = llm.create_chat_completion(messages=prompt)
    try:
        out_str = output['choices'][0]['message']['content']
    except:
        out_str = str(output)
    return out_str

