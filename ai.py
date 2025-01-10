from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from nltk.chat.util import Chat, reflections

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


car_models = {
    'A4': {
        'name': 'AUDI A4',
        'speed': '240 km/h',
        'tyres': 'Radial',
        'airbags': '6',
        'seatbelts': 'Yes',
        'air_conditioners': 'Automatic Climate Control',
        'music_system': 'Bang & Olufsen Sound System',
        'price': '$60,000',
        'image': 'A4.jpg'
    },
    'Audi_Q4_e-tron': {
        'name': 'Q4 e-tron',
        'speed': '250 km/h',
        'tyres': 'Radial',
        'airbags': '6',
        'seatbelts': 'Yes',
        'air_conditioners': 'Automatic Climate Control',
        'music_system': 'Bose Surround Sound System',
        'price': '$50,000',
        'image': 'Audi_Q4_e-tron.jpg'
    },
    'e-tron_GT': {
        'name': 'e-tron_GT',
        'speed': '220 km/h',
        'tyres': 'Radial',
        'airbags': '6',
        'seatbelts': 'Yes',
        'air_conditioners': 'Automatic Climate Control',
        'music_system': 'JBL Sound System',
        'price': '$55,000',
        'image': 'e-tron_GT audi model.png'
    },
    'Q6_e-tron': {
        'name': 'Q6 e-tron',
        'speed': '230 km/h',
        'tyres': 'Radial',
        'airbags': '6',
        'seatbelts': 'Yes',
        'air_conditioners': 'Manual',
        'music_system': 'Sony Sound System',
        'price': '$45,000',
        'image': 'Q6_e-tron audi model.png'
    },
    'Q8_e-tron': {
        'name': 'Q8 e-tron',
        'speed': '260 km/h',
        'tyres': 'All-Season',
        'airbags': '8',
        'seatbelts': 'Yes',
        'air_conditioners': 'Dual-Zone Automatic Climate Control',
        'music_system': 'Harman Kardon Sound System',
        'price': '$70,000',
        'image': 'Q8_e-tron audi model.jpg'
    }
}



pairs = [
    [r"my name is (.*)", ["Hello %1, How can I help you today?",]],
    [r"hi|hello|hey", ["Hello, How can I help you today?", "Hi there, How can I assist you?"]],
    [r"what car models do you have?", ["We have Model 1, Model 2, Model 3, Model 4, and Model 5. Which one are you interested in?"]],
    [r"tell me about (model1|model2|model3|model4|model5)", ["%(name)s is a great choice! Here are the details:\nSpeed: %(speed)s\nTyres: %(tyres)s\nAirbags: %(airbags)s\nSeatbelts: %(seatbelts)s\nAir Conditioners: %(air_conditioners)s\nMusic System: %(music_system)s\nPrice: %(price)s"]],
    [r"I want to (rent|hire|borrow|lease) a car", ["Sure, I can help you with that. Which model would you like to rent?"]],
    [r"I want to (buy|purchase) a car", ["Great! Which model are you interested in buying?"]],
    [r"how (fast|speedy|quick) (is|are) (model1|model2|model3|model4|model5)", ["%(name)s has a top speed of %(speed)s."]],
    [r"what (type|kind) of (tyres|tires) (does|do) (model1|model2|model3|model4|model5) (use|have)", ["%(name)s uses %(tyres)s tyres."]],
    [r"how many (airbags|safety bags) (does|do) (model1|model2|model3|model4|model5) (have|come with)", ["%(name)s is equipped with %(airbags)s airbags."]],
    [r"do (model1|model2|model3|model4|model5) (have|come with) (seatbelts|belts)", ["Yes, %(name)s comes with seatbelts."]],
    [r"what (type|kind) of (air conditioners|AC) (does|do) (model1|model2|model3|model4|model5) (have|come with)", ["%(name)s has %(air_conditioners)s air conditioners."]],
    [r"what (music system|audio system) (does|do) (model1|model2|model3|model4|model5) (have|come with)", ["%(name)s comes with %(music_system)s."]],
    [r"what (is|are) the (price|cost) (of|for) (model1|model2|model3|model4|model5)", ["The price of %(name)s is %(price)s."]],
    [r"thank you|thanks", ["You're welcome! If you have any more questions, feel free to ask."]],
    [r"bye|goodbye", ["Goodbye! Have a great day!", "Bye! Take care!"]],
]

def chatbot_response(text):
    chat = Chat(pairs, reflections)
    response = chat.respond(text)

    
    if "hi" in text.lower() or "hello" in text.lower() or "hey" in text.lower():
        return {'response': "Hello, How can I help you today?", 'car_info': None}

    if "goodbye" in text.lower() or "bye" in text.lower():
        return {'response': "Goodbye! Have a great day!", 'car_info': None}

    
    if "car models" in text.lower() or "available cars" in text.lower():
        car_list = ', '.join([model_data['name'] for model_data in car_models.values()])
        response = f"We have the following car models: {car_list}. Let me know which model you're interested in."
        return {'response': response, 'car_info': None}

    
    car_info = None
    for model_key, model_data in car_models.items():
        if model_data['name'].lower() in text.lower():
            response = f"Here are the details for the {model_data['name']}:"
            car_info = model_data
            car_info['image_url'] = url_for('static', filename=model_key + '.jpg')
            break
    
    if car_info:
        return {
            'response': response,
            'car_info': car_info,
            'html_content': render_template_string('''
                <br><img src="{{ car_info.image_url }}" alt="{{ car_info.name }}" style="width: 100px; height: auto;">
                <p>Name: {{ car_info.name }}</p>
                <p>Speed: {{ car_info.speed }}</p>
                <p>Tyres: {{ car_info.tyres }}</p>
                <p>Airbags: {{ car_info.airbags }}</p>
                <p>Seatbelts: {{ car_info.seatbelts }}</p>
                <p>Air Conditioners: {{ car_info.air_conditioners }}</p>
                <p>Music System: {{ car_info.music_system }}</p>
                <p>Price: {{ car_info.price }}</p>
            ''', car_info=car_info)
        }
    else:
        return {'response': "Sorry, I don't have information on that car model.", 'car_info': None}

# HTML template with embedded CSS and JavaScript
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audi Car Models</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: url('{{ url_for('static', filename='audi.gif') }}') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        .navbar {
            position: fixed;
            top: 0;
            width: 1230px;
            background-color: black;
            color: #fff;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar h1 {
            margin: 0;
        }
        .navbar ul {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
        }
        .navbar ul li {
            margin-left: 10px;
        }
        .navbar ul li a {
            color: #fff;
            text-decoration: none;
        }
        .container {
            text-align: center;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.4);
            margin: 20px auto;
            width: 90%;
            border-radius: 5px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .car-model {
            margin: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            flex: 1 1 300px;
            max-width: 300px;
        }
        .car-model img {
            width: 100%;
            height: auto;
        }
        .car-model h3 {
            margin: 10px 0 5px;
        }
        .chatbot-container {
            display: none;
            color: white;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            padding: 20px;
            width: 300px;
            height: 400px;
            overflow-y: scroll;
            position: fixed;
            bottom: 80px;
            right: 20px;
            text-align: center;
            z-index: 1000;
        }
        .chatbot-messages {
            color: Black;
            height: 70%;
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
            background-color:white;
            background-image: url('{{ url_for('static', filename='robot.jpg') }}');
            background-size:100px 100px; /* Adjust size as needed */
            background-repeat: no-repeat;
            background-position: center;
        }
        .chatbot-input {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
        }
        .chatbot-toggle {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            z-index: 1001;
        }
        .back-button {
            margin-top: 10px;
            padding: 10px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .highlight {
        background-color: rgba(255, 255, 255, 0.2); /* Light highlight color */
        border-radius: 5px;
        padding: 5px;
    }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>A U D I </h1>
        <ul>
            <li><a href="{{ url_for('index') }}">Home</a></li>
            <li><a href="{{ url_for('chatbot') }}">Search</a></li>
            <li><a href="{{ url_for('logout') }}">Contact</a></li>
        </ul>
    </div>
    <div class="container">
    {% for model_key, model in car_models.items() %}
    <div class="car-model">
        <img src="{{ url_for('static', filename=model.image) }}" alt="{{ model.name }}">
        <h3>{{ model.name }}</h3>
        <p>Speed: {{ model.speed }}</p>
        <p>Price: {{ model.price }}</p>
        <form action="{{ url_for('model_details', model_key=model_key) }}" method="get">
            <button type="submit" class="details-button" data-model="{{ model_key }}">Details</button>
        </form>
    </div>
    {% endfor %}
</div>

    <div class="chatbot-container" id="chatbot-container">
        <div class="chatbot-messages" id="chatbot-messages"></div>
        <input type="text" class="chatbot-input" id="chatbot-input" placeholder="Type a message...">
        <button class="back-button" id="back-button" onclick="toggleChatbot()">Close</button>
    </div>
    <button class="chatbot-toggle" onclick="toggleChatbot()">💬</button>

    <script>
        const toggleChatbot = () => {
            const chatbotContainer = document.getElementById('chatbot-container');
            chatbotContainer.style.display = chatbotContainer.style.display === 'none' ? 'block' : 'none';
        };

        const sendMessage = (message) => {
    const messagesContainer = document.getElementById('chatbot-messages');
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.innerText = 'You: ' + message;
    messagesContainer.appendChild(userMessage);

    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('bot-message');

        // Inject HTML content
        if (data.html_content) {
            botMessage.innerHTML = 'Bot: ' + data.response + data.html_content;
        } else {
            botMessage.innerHTML = 'Bot: ' + data.response;
        }

        messagesContainer.appendChild(botMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Remove highlight after 1 second
        setTimeout(() => {
            botMessage.classList.remove('highlight');
        }, 1000);

        // Speech synthesis for bot response
        const utterance = new SpeechSynthesisUtterance(data.response);
        window.speechSynthesis.speak(utterance);
    })
    .catch(error => console.error('Error:', error));
};

// Handle Enter key press
document.getElementById('chatbot-input').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const inputField = event.target;
        const message = inputField.value;
        inputField.value = '';
        sendMessage(message);
    }
});


        // Speech recognition for chatbot input
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = (event) => {
            const message = event.results[0][0].transcript;
            sendMessage(message);
        };
        recognition.onend = () => recognition.start();
        recognition.start();

        // Adding speech synthesis for details button
        document.querySelectorAll('.details-button').forEach(button => {
            button.addEventListener('click', (event) => {
                event.preventDefault();
                const modelKey = event.target.getAttribute('data-model');
                fetch(`/details/${modelKey}`)
                .then(response => response.json())
                .then(data => {
                    const details = `
                        Name: ${data.name}
                        Speed: ${data.speed}
                        Tyres: ${data.tyres}
                        Airbags: ${data.airbags}
                        Seatbelts: ${data.seatbelts}
                        Air Conditioners: ${data.air_conditioners}
                        Music System: ${data.music_system}
                        Price: ${data.price}
                    `;
                    const utterance = new SpeechSynthesisUtterance(details);
                    window.speechSynthesis.speak(utterance);
                })
                .catch(error => console.error('Error:', error));
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template, car_models=car_models)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.json['message']
        response_data = chatbot_response(user_message)
        return jsonify(response_data)
    return render_template_string(html_template, car_models=car_models)


@app.route('/details/<model_key>', methods=['GET'])
def model_details(model_key):
    if model_key in car_models:
        return jsonify(car_models[model_key])
    return jsonify({'error': 'Model not found'}), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


