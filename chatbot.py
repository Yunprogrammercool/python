from flask import Flask, request, render_template
import openai
import requests

app = Flask(__name__)

# Set up your OpenAI API credentials
openai.api_key = "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"

# Define the prompt for the chatbot
prompt = "Hi, I'm a chatbot. What can I help you with?"

# Define the function to send a request to the web API
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=YOUR_API_KEY_HERE&units=metric"
    response = requests.get(url)
    data = response.json()
    return "The temperature in " + city + " is " + str(data["main"]["temp"]) + " degrees Celsius."

# Define the function to scrape data from a website
def get_wikipedia_summary(topic):
    url = "https://en.wikipedia.org/wiki/" + topic.replace(" ", "_")
    response = requests.get(url)
    if response.status_code == 200:
        start = response.text.find("<p>")
        end = response.text.find("</p>")
        summary = response.text[start:end]
        summary = summary.replace("<sup>", "").replace("</sup>", "")
        return summary
    else:
        return "Sorry, I couldn't find any information on that topic."

# Define the function to send a request to the OpenAI API
def ask_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message

# Define the route to the chatbot page
@app.route('/', methods=['GET', 'POST'])
def chatbot():
    global prompt
    if request.method == 'POST':
        user_input = request.form['message']
        prompt += "\nUser: " + user_input
        response = ask_openai(prompt)
        chatbot_response = "Chatbot: " + response + "<br>"

        # Check if the user is asking for the weather
        if "what is the weather in" in user_input.lower():
            city = user_input.split()[-1]
            weather = get_weather(city)
            chatbot_response += "Chatbot: " + weather + "<br>"
            prompt += "\nChatbot: " + weather

        # Check if the user is asking for a Wikipedia summary
        elif "what is" in user_input.lower():
            topic = user_input.split("what is ")[-1]
            summary = get_wikipedia_summary(topic)
            chatbot_response += "Chatbot: " + summary + "<br>"
            prompt += "\nChatbot: " + summary

        return render_template('chatbot.html', chatbot_response=chatbot_response)
    else:
        return render_template('chatbot.html', chatbot_response="")

if __name__ == '__main__':
    app.run(debug=True)
