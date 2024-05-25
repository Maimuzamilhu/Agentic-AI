# Build AI Agents with OpenAI's Assistant API - Quick Streamlit Tutorial

https://www.toolify.ai/gpts/build-ai-agents-with-openais-assistant-api-quick-streamlit-tutorial-48395 

https://www.youtube.com/watch?v=tLeqCDKgEDU



from openai.types.beta import Assistant

assistant: Assistant = Client.beta.assistants.create(
  name= "Travel Agent by Muzzamil" ,
  instructions="You are a Helpull travel assistant that can write and execute code , and has access to digital map to display information",
  model="gpt-3.5-turbo-1106",
  tools=[ {
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
},{
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