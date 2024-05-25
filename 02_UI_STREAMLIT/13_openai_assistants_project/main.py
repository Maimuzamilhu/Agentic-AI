import streamlit as st
import plotly.graph_objects as go
import json
from openai import OpenAI
import time
from openai.types.beta import Assistant
client : OpenAI = OpenAI()




st.set_page_config(
    page_title="Wanderlust",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

assistant_id = st.secrets["OPENAI_ASSISTANT_ID"]

st.title("Muzzamil's Map")

if "map" not in st.session_state:
    st.session_state["map"]= {
        "latitude": 39.949610,
        "longitude" : -75.150282,
        "zoom"    : 16,
    }

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

if "assistant" not in st.session_state:
    st.session_state["assistant"] = client.beta.assistants.retrieve()
    st.session_state["thread"] = client.beta.threads.create()
    st.session_state["run"] = None


with st.sidebar:
    st.header("Debug")
    st.write(st.session_state.to_dict())


left_col , right_col = st.columns(2)

with left_col:
    st.subheader("Conversation")
    for role, message in st.session_state["conversation_state"]:
            with st.chat_message(role):
                st.write(message)

with right_col:
    fig = go.Figure(go.Scattermapbox())
    fig.update_layout(
        mapbox = dict(
            accesstoken = st.secrets["MapBox_Access"], 
            center = go.layout.mapbox.Center(
                lat=st.session_state["map"]["latitude"],
                lon=st.session_state["map"]["longitude"],
            ),
            zoom = st.session_state["map"]["zoom"],
        ),
        margin = dict(l=0, r=0, t=0, b = 0),
    )
    st.plotly_chart(
    
        fig,
        config = {"displayModeBar" : False},
        use_container_width=  True,
        key = "plotly",
    )


def update_map(latitude, longitude, zoom):
    
    st.session_state["map"] = {
        "latitude":latitude,
        "longitude" : longitude,
        "zoom" : zoom
    }
    return "map updated"


def on_text_input():
    client.beta.threads.messages.create(
        thread_id=st.session_state["thread"].id,
        role="user",
        content = st.session_state["input_user_msg"],
    )
    st.session_state["run"] = client.beta.threads.runs.create(
        thread_id=st.session_state["thread"].id,
        assistant_id=st.session_state["assistant"].id,
    )
    completed = False

    while not completed:
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state["thread"].id,
            run_id=st.session_state["run"].id,
        )
    if run.status == "completed":
        completed = True
    
    if run.status == "requires_action":
        tools_output = []
        for tool_cool in run.required_action.submit_tool_outputs.tool_calls:
            f = tool_cool.function
            f_name = f.name
            f_args =  json.loads(f.arguments)

            tool_result = tool_to_function[f_name](**f_args)
            tools_output.append(
                {
                    "tool_cool_id" : tool_cool.id,
                    "output" : tool_result,
                }
            )
        
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=st.session_state["thread"].id,
            run_id= st.session_state["run"].id,
            tool_outputs= tools_output
        )


    else:
        time.sleep(0.1)

    st.session_state["conversation"] = [
        (m.role , m.content[0].text.values)
        for m in client.beta.threads.messages.list(st.session_state["thread"].id).data 

    ]

st.chat_input(
    placeholder="Ask your Question Here :",
    key="input_user_msg",
    on_submit=on_text_input,
)

tool_to_function = {
    "update_map" : update_map,
}



# Create an instance of the Assistant class
assistant = client.beta.assistants.create(
    instructions="You are a helpful travel assistant that can write and execute code, and has access to a digital map to display information",
    name= "Gpt Map by Muzzamil",
    model="gpt-3.5-turbo-1106",
    tools=[
        {
            "name": "update_map",
            "description": "Update map to center on a particular location",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location to center the map on"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location to center the map on"
                    },
                    "zoom": {
                        "type": "integer",
                        "description": "Zoom level of the map"
                    }
                },
                "required": ["longitude", "latitude", "zoom"]
            }
        },
        {
            "name": "add_markers",
            "description": "Add list of markers to the map",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of longitude of the location to each marker"
                    },
                    "latitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of latitude of the location to each marker"
                    },
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of text to display on the location of each marker"
                    }
                },
                "required": ["longitudes", "latitudes", "labels"]
            }
        }
    ]
)

