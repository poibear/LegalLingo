import os
import openai
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.default_headers = {"OpenAI-Beta": "assistants=v2"}

client = OpenAI()

tax_assistant = client.beta.assistants.create(
    instructions="You are a tax advisor that provides low-income communities layman explanations for tax forms. Start with the broad summary of a tax document that the user asks for, before diving into the specifics of each field and what they mean in layman terms. You are not to prompt the user for extra clarification or questions, rather just performing explanations. Only write information you get from your sources; don't make anything up. If you don't know, say that you don't know.",
    name="Tax Assistant",
    model="gpt-4o"
)

def getTaxDescription(form_name: str):
    thread = client.beta.threads.create()
    
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"What is {form_name} from the IRS?"
    )

    # keep asking for a response until we get it
    while True:
        response = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=tax_assistant.id,
            instructions="Start with a three-sentence summary of the tax form, followed by an in-depth analysis of each field in the form in layman terms."
        )
        
        if response.status == "completed":
            break
        else:
            continue
    
    # get summary text of tax doc
    summary = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    
    return summary.data[0].content[0].text.value

def getTaxForm(form_name: str):
    elements = form_name.split()
    file_name = elements[0][0] + elements[1]
    
    pdf = requests.get(f"https://www.irs.gov/pub/irs-pdf/{file_name}.pdf")
    