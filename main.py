import gradio as gr
import pokepy
from openai import OpenAI
import json

OpenAI.api_key = "OPENAI API key"

client = OpenAI()


class Logic(): 

    def AskAI(Pokemon1,Pokemon2):


        Question = f"{Pokemon1} and {Pokemon2}"

        response = client.chat.completions.create(
          model="gpt-4",
          messages=[
                {"role": "system", "content": 'You are a Pokemon Expert. You will be given 2 Pokemon at equal level and using your vast knowledge of Pokemon. You will tell who will most likely win in a 1v1 battle and why. Give a concise answer. Answer with a python dictionary with the exact keys "Winner"  and "Reasoning"'},
                {"role": "user", "content": Question},
                
            ]
        )

        return response.choices[0].message.content


    def PokemonID(Input):

        client = pokepy.V2Client()
        Pokemon = client.get_pokemon(str(Input.lower()))
        Result = int(Pokemon[0].id)
        
        if Result <= 9:
            return "00" + str(Result)
        elif Result <= 99:
            return "0" + str(Result)
        else: 
            return Result


def result(Pokemon1,Pokemon2):
    Data = Logic.AskAI(Pokemon1,Pokemon2)
    DictData = json.loads(Data)

    Winner = DictData["Winner"]
    Reasoning = DictData["Reasoning"]

    pokemon_id = Logic.PokemonID(Winner)


    return (f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokemon_id}.png",Reasoning,)


with open("AllPokemon.txt","r+") as f:
    PokeList = f.readlines()
    

app = gr.Interface(
    fn=result,
    inputs=[gr.Dropdown(PokeList,label="First Pokemon"), gr.Dropdown(PokeList,label="Second Pokemon")],
    outputs= [gr.Image(label="Winner:"), gr.Textbox(label="Reasoning:")],
    title="Pokemon Battler"
)


app.launch(share=True)
# app.launch()










