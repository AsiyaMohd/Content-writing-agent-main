# import os
# import sys
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage
# from langgraph.graph import MessagesState, StateGraph, START, END
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Dynamic Path Setup to set the default path 
# current_file_path = os.path.abspath(__file__)
# project_root = os.path.abspath(os.path.join(current_file_path, "../.."))
# if project_root not in sys.path:
#     sys.path.append(project_root)

# from tools.search_tool import search_content
# from agents.prompts import social_prompt,email_prompt,sales_prompt,thought_prompt,blog_prompt,search_prompt,tone_prompt,web_copy_prompt

# class ContentState(MessagesState):
#     content_type:str
 
# llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# # llm = ChatOpenAI(model="gpt-4o-mini")

# tools = [search_content]
# llm_with_tools = llm.bind_tools(tools)

# #  Define Agent 1: Search Agent 
# search_agent_prompt = SystemMessage(content=search_prompt)
# def search_agent(state: ContentState):
#     print("--------------------------search agent state------------")
#     print(state)
#     return {"messages": [llm_with_tools.invoke([search_agent_prompt] + state["messages"])]}

# def orchestrator(state: ContentState):
#     return state

# #  Define Agent 2: Content Agent 
# blog_agent_prompt = SystemMessage(content=blog_prompt)
# def blog_agent(state: ContentState):
#     print("--------------------------blog agent state------------")
#     print(state["content_type"])
#     return {"messages": [llm.invoke([blog_agent_prompt] + state["messages"])]}


# thought_leadership_agent_prompt = SystemMessage(content=thought_prompt)
# def thought_leadership_agent(state: ContentState):
#     return {"messages": [llm.invoke([thought_leadership_agent_prompt] + state["messages"])]}

# web_copy_agent_prompt=SystemMessage(content=web_copy_prompt)
# def web_copy_agent(state: ContentState):
#     return {"messages":[llm.invoke([web_copy_agent_prompt]+state["messages"])]}
# email_sequence_agent_prompt = SystemMessage(content=email_prompt)

# def email_sequence_agent(state: ContentState):
#     return {"messages": [llm.invoke([email_sequence_agent_prompt] + state["messages"])]}


# social_post_agent_prompt = SystemMessage(content=social_prompt)
# def social_post_agent(state: ContentState):
#     return {"messages": [llm.invoke([social_post_agent_prompt] + state["messages"])]}


# sales_asset_agent_prompt = SystemMessage(content=sales_prompt)
# def sales_asset_agent(state: ContentState):
#     return {"messages": [llm.invoke([sales_asset_agent_prompt] + state["messages"])]}

# # Define Agent 3: Tuning Agent 

# def tune_agent(state: ContentState):
#     tune_agent_prompt = SystemMessage(content="content type"+state["content_type"]+tone_prompt)
    
#     return {"messages": [llm.invoke([tune_agent_prompt] + state["messages"])]}

# def orchestrator_condition(state: ContentState):
#     print("we got the content type as ",state["content_type"])
    
#     return state["content_type"]

# # --- Build Graph ---
# graph = StateGraph(ContentState)

# graph.add_node("search_agent", search_agent)
# graph.add_node("tools", ToolNode(tools))
# graph.add_node("orchestrator",orchestrator)
# graph.add_node("blog", blog_agent)

# graph.add_node("thought_leadership",thought_leadership_agent)
# graph.add_node("web_copy",web_copy_agent)
# graph.add_node("email_sequence",email_sequence_agent)
# graph.add_node("social_post",social_post_agent)
# graph.add_node("sales_asset",sales_asset_agent)

# graph.add_node("tune_agent", tune_agent)

# graph.add_edge(START,"search_agent")
# graph.add_conditional_edges(
#     "search_agent",
#     tools_condition,
#     {"tools": "tools", "__end__": "orchestrator"}
# )

# graph.add_edge("tools", "search_agent")

# graph.add_edge("search_agent","orchestrator")
# graph.add_conditional_edges(
#     "orchestrator",
#     orchestrator_condition,
#     {
#         "blog": "blog",
#         "thought_leadership": "thought_leadership",
#         "web_copy":"web_copy",
#         "email_sequence": "email_sequence",
#         "social_post": "social_post",
#         "sales_asset": "sales_asset",
#     }
# )

# graph.add_edge("blog", "tune_agent")
# graph.add_edge("thought_leadership", "tune_agent")
# graph.add_edge("web_copy","tune_agent")
# graph.add_edge("email_sequence", "tune_agent")
# graph.add_edge("social_post", "tune_agent")
# graph.add_edge("sales_asset", "tune_agent")

# graph.add_edge("tune_agent", END)

# #  Compile Agent 
# agent = graph.compile()
# agent







import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI

# Dynamic Path Setup to set the default path 
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from tools.search_tool import search_content
from agents.prompts import social_prompt,email_prompt,sales_prompt,thought_prompt,blog_prompt,search_prompt,tone_prompt,web_copy_prompt,research_prompt,blog_tone_prompt,thougth_tone_prompt,research_tone_prompt
from tools.search_tool import extract_urls_from_tool_messages
class ContentState(MessagesState):
    content_type:str
    input:str
    links:list[str]
    pdf:bool
    formdata:str
 
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# llm = ChatOpenAI(model="gpt-4o-mini")

tools = [search_content]
llm_with_tools = llm.bind_tools(tools)
    
#  Define Agent 1: Search Agent 
search_agent_prompt = SystemMessage(content=search_prompt)
def search_agent(state: ContentState):
    print("--------------------------search agent state------------")
    # print(state)
    return {"messages": [llm_with_tools.invoke([search_agent_prompt] + state["messages"]+state["input"])]}

def orchestrator(state: ContentState):
    state["links"]=extract_urls_from_tool_messages(state)
    print("--------------orchestator---------------------")
    # print(state)
    return state

#  Define Agent 2: Content Agent 
def blog_agent(state: ContentState):
    print("--------------------------blog agent state------------")
    if state["pdf"]:
        blog_agent_prompt = SystemMessage(content=blog_prompt+"use this as a content:"+state["formdata"])
        print("---------------pdf")
        return {"messages": [llm.invoke([blog_agent_prompt] + state["input"])]}
    else:
        blog_agent_prompt = SystemMessage(content=blog_prompt)
        return {"messages": [llm.invoke([blog_agent_prompt] + state["messages"] + state["input"])]}



def thought_leadership_agent(state: ContentState):
    if state["pdf"]:
        thought_leadership_agent_prompt = SystemMessage(content=thought_prompt+"use this as content"+state["formdata"])
        return {"messages": [llm.invoke([thought_leadership_agent_prompt]+state["input"])]}
    else:
        thought_leadership_agent_prompt = SystemMessage(content=thought_prompt)
        return {"messages": [llm.invoke([thought_leadership_agent_prompt] + state["messages"] +state["input"])]}
    

def research_paper_agent(state: ContentState):
    if state["pdf"]:
        research_paper_prompt = SystemMessage(content=research_prompt+"use this pdf data as contnent"+state["formdata"])
        return {"messages": [llm.invoke([research_paper_prompt] + state["input"])]}
    else:
        research_paper_prompt = SystemMessage(content=research_prompt)
        return {"messages": [llm.invoke([research_paper_prompt] + state["messages"])]}

# Define Agent 3: Tuning Agent 
def tune_agent(state: ContentState):
    tune_agent_prompt=""
    if state["content_type"]=="blog":
        print("got the blog tone")
        tune_agent_prompt = SystemMessage(content="content type"+state["content_type"]+blog_tone_prompt)
    elif state["content_type"]=="thought_leadership":
        print("got the thought tone")
        tune_agent_prompt = SystemMessage(content="content type"+state["content_type"]+thougth_tone_prompt)
    elif state["content_type"]=="research_paper":
        print("got the research tone")
        tune_agent_prompt = SystemMessage(content="content type"+state["content_type"]+research_tone_prompt)
    print("=------------------tune agent-----------------")
    return {"messages": [llm.invoke([tune_agent_prompt] + state["messages"])]}
    

def orchestrator_condition(state: ContentState):
    # print("we got the content type as ",state["content_type"])
    
    return state["content_type"]

def state_check(state: ContentState):
    print("---------initial state-----------------")
    return state
 
def decide_flow(state: ContentState):
    if state["formdata"]:
        return "form_agent"
    return "search_agent"
 
def form_agent(state: ContentState):
    print("-------------form agent--------------")
    print(state["formdata"])
    return state

# --- Build Graph ---
graph = StateGraph(ContentState)

graph.add_node("state_check",state_check)
graph.add_node("form_agent",form_agent)
graph.add_node("search_agent", search_agent)
graph.add_node("tools", ToolNode(tools))
graph.add_node("orchestrator",orchestrator)
graph.add_node("blog", blog_agent)

graph.add_node("thought_leadership",thought_leadership_agent)
graph.add_node("research_paper", research_paper_agent)
graph.add_node("tune_agent", tune_agent)

graph.add_edge(START, "state_check")

graph.add_conditional_edges(
    "state_check",
    decide_flow,
    {
        "search_agent":"search_agent",
        "form_agent":"form_agent"
    }
)
 
graph.add_edge("form_agent", "orchestrator")
 
graph.add_conditional_edges(
    "search_agent",
    tools_condition,
    {
       
        "tools": "tools",
       
        "__end__": "orchestrator"
    }
)
 
graph.add_edge("tools", "search_agent")
 
 
# Orchestrator routes to the correct content agent
graph.add_conditional_edges(
    "orchestrator",
    orchestrator_condition,
    {
        "blog": "blog",
        "thought_leadership": "thought_leadership",
        "research_paper": "research_paper"
    }
)
 
# All content agents lead to the tune_agent
for node in [
    "blog", "thought_leadership", "research_paper"
]:
    graph.add_edge(node, "tune_agent")
 
# Tuning is the final step
graph.add_edge("tune_agent", END)
 
#  Compile Agent 
agent = graph.compile()
agent







 