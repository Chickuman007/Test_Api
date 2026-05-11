import flask
import os
from flask import jsonify, request, Flask, render_template
from langchain_ollama import  ChatOllama
from langchain_groq import ChatGroq
from langchain.agents import create_agent



'''model = ChatOllama(model='llama3.2')'''

os.environ["GROQ_API_KEY"]="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"
model=ChatGroq(model="qwen/qwen3-32b")
app=Flask(__name__)


agent=create_agent(model=model,system_prompt="""You are an intelligent AI assistant.
Answer the question asked by user in generous way.
""")


def new_chatbot(query:str):
    global agent
    response=agent.invoke({"messages":[{"role":"user","content":query}]})
    final_answer = response["messages"][-1].content
    return final_answer


@app.route("/",methods=["POST","GET"])
def landing():
    return render_template("bot.html")


@app.route("/api/chatbot",methods=["POST","GET"])
def api_chatbot():
    if request.method=="POST":
        question = request.form.get("question")
    
        # JSON payload support
        if not question and request.is_json:
            data = request.get_json()
            question = data.get("question")
    
        if not question:
            return jsonify({
                "status": "error",
                "message": "No question provided"
            }), 400
    
        answer = new_chatbot(question)
    
        return jsonify({
            "status": "success",
            "answer": answer
        })





