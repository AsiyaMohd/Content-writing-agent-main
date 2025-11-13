from flask import Flask, render_template, request, jsonify,stream_with_context,Response
from agents.research_agent import agent   # import your LangGraph agent
from langchain_core.messages import HumanMessage,AIMessage
import json
#Chang
from tools.pdf_extractor import pdfdata

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        uploaded_pdf = request.files.get("file")
        # metadata_str = request.form.get("metadata")
        # data = json.loads(metadata_str)
        user_input = request.form.get("query","")
        user_input2 = request.form.get("content_type","")
        word_count = request.form.get("wordCount", "") # From slider
        print(word_count)
        print(type(word_count))
        file_data=""
        file=""
        if uploaded_pdf:
             file_data=pdfdata(uploaded_pdf)
        if not user_input:
            return jsonify({"error": "No query provided"}), 400
        initial_state={}
        if file_data:
            initial_state = {
                          "messages": [HumanMessage(content=user_input)],
                          "content_type": user_input2,
                          "input": [user_input],
                          "links":[],
                          "pdf":True,
                          "formdata":file_data,
                          "wordCount": word_count 
                        }
        else:

            initial_state = {
                          "messages": [HumanMessage(content=user_input)],
                          "content_type": user_input2,
                          "input": [user_input],
                          "links":[],
                          "pdf":False,
                          "formdata":file_data,
                          "wordCount": word_count
                        }
        result = agent.invoke(initial_state)
       
        output_text = "No response generated."
       
        if "messages" in result and result["messages"]:
 
            link = result["links"]
            print("----------------------------------------")
           
            for msg in reversed(result["messages"]):
               
                if hasattr(msg, 'content') and msg.content and not isinstance(msg, (HumanMessage)):
                   
                    if isinstance(msg.content, list):
               
                        output_text = "\n\n---\n\n".join(msg.content)
                    else:
                       
                        output_text = str(msg.content)
                   
                    break
            if isinstance(link,list):
                output_links = "\n\n---\n\n".join(link)
                output_links = output_links[:-1]
                print(len(output_links))
            else:
                output_links = str(link)
                output_links = output_links[:-1]
                print(len(output_links))
 
      
     
        return jsonify({"response": output_text,"links":output_links})
                
                   
           

    except Exception as e:
        return jsonify({"error": str(e)}), 501


if __name__ == '__main__':
    app.run(debug=True)