from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

my_bot = ChatBot(name="WeatherBot", read_only=True,
                 logic_adapters=["chatterbot.logic.MathematicalEvaluation", "chatterbot.logic.BestMatch"]
                 )


small_talk = [
    ["Hi", "Hey there!"],
    ["What is your name?", "My name is WeatherBot"],
    ["How are you?", "I'm great! How are you?"],
    ["Can you help me find the weather?", "Sure I'd love to help!"],
    ["How are you doing?", "I'm feeling very sunny today"],
    ["What do you do?", "I'm here to help you with the weather!"],
    ["I need some help", "Sure! I'm here to help!"]
]

weather_talk = [
    ["Which cities are in my itinerary?",
     "These are the cities you will be visiting: Corfe Castle, The Cotswolds", "Cambridge", "Bristol", "Oxford",
     "Norwich", "Stonehenge", "Watergate Bay", "Birmingham"],
    ["What's the weather like today", "The weather for city is going to be.."],
    ["Will it rain tomorrow?", "Looks like its.."],
    ["How windy is it outside", "Its looking .."],
    ["How windy is it in city", "It looking .."],
    ["What about  in this city?", "In city your looking at"],
    ["What about tomorrow?", "Tomorrow the weather will be.."],
    ["Are there any storms expected in city", "Taking a look there should.."],
    ["What is the weather outlook for the next week?", "This is the weather for the next 7 days"],
    ["What is the weather outlook for the next week in city?", "This is the weather for the next 7 days"],
    ["Can you tell me what the UV index will be for city", "The UV index for city will be.."],
    ["Which cities can you find the weather for?",
     "These are the cities you will be visiting: Corfe Castle, The Cotswolds", "Cambridge", "Bristol", "Oxford",
     "Norwich", "Stonehenge", "Watergate Bay", "Birmingham"]

]

list_trainer = ListTrainer(my_bot)

for sublist in small_talk + weather_talk:
    list_trainer.train(sublist)

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')

print(my_bot.get_response("Hi"))
print(my_bot.get_response("How are you"))
print(my_bot.get_response("What is your name"))

while True:
    try:
        bot_input = input("You: ")
        bot_response = my_bot.get_response(bot_input)
        print(f"{my_bot.name}: {bot_response}")
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
