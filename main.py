import discord
from discord.ext import commands
import random
import os
from model import get_class
import requests
import pyttsx3
from googletrans import Translator

translator = Translator()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def get_weather(ciudad: str):
    link = f"https://wttr.in/{ciudad}?format=%C+%t"
    res = requests.get(link)
    if res.status_code == 200:
        return res.text.strip()
    else:
        return "No se pudo obtener informacion"

# Clima


@bot.command()
async def clima(ctx, *, ciudad: str = ""):
    info = get_weather(ciudad)
    x = "El clima en", ciudad, "es:", info
    await ctx.send(x)
    speak(x)

# Speek


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Dato random


async def fact(idioma):
    link = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    res = requests.get(link)
    if res.status_code == 200:
        contenido = res.json()
        contenido = contenido.get("text", "Not found")
        contenido = f"¿Did you know that {contenido}?"
        contenido = await translator.translate(contenido, src="en", dest=idioma)
        return f"{contenido.text}"
    else:
        return ("No se pudo entregar informacion")

# Arreglar


@bot.command()
async def dato(ctx, idioma="es"):
    info = await fact(idioma)
    await ctx.send(info)
    speak(info)
# Hola


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

# Heh


@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

# Sumar


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# Joined


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

# Meme


@bot.command()
async def mem(ctx):
    imagenes = os.listdir("Images")
    img_name = random.choice(imagenes)
    with open(f'Images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

# Flor


@bot.command()
async def flor(ctx):
    flores = os.listdir("flores")
    img_name = random.choice(flores)
    with open(f'flores/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

# Chocolate


@bot.command()
async def choco(ctx):
    chocolates = os.listdir("chocolates")
    img_name = random.choice(chocolates)
    with open(f'flores/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

# Informacion


@bot.command()
async def info(ctx):
    await ctx.send("""Hola! Prueba los siguientes comandos:
                   -heh: Has reir al bot
                   -add: Sumar dos números entre si
                   -mem: Manda un meme aleatorio
                   -flor: Manda una imagen aleatoria de una flor
                   -clasificar: Si envías una imagen de un dibujo con este comando,
                   clasifica el estilo y manda ejemplos.
                   -Clima: Pon "$clima" y el nombre de un pais/ciudad para averiguar su clima
                   -Dato: Usa el comando para generar un dato aleatorio""")


@bot.command()
async def dado(ctx):
    cara = random.randint(1, 6)
    await ctx.send(f'Salió el número {cara} 🎲')


@bot.command()
async def clasificar(ctx):
    if ctx.message.attachments:
        for archivo in ctx.message.attachments:
            nombre = archivo.filename
            url = archivo.url
            await archivo.save(nombre)
            await ctx.send(f"Archivo guardado en {nombre}")
            try:
                class_name = get_class("keras_model.h5", "labels.txt", nombre)
                if class_name == "Realista":
                    await ctx.send("""Tu dibujo es de estilo realista,
                    es decir que intenta imitar la realidad.
                    Se detallan mucho las sombras, texturas y las luces.
                    Acá va un ejemplo de un diujo de este estilo:""")
                    Reales = os.listdir("Reales")
                    img_name = random.choice(Reales)
                    with open(f'Reales/{img_name}', 'rb') as f:
                        picture = discord.File(f)
                    await ctx.send(file=picture)

                elif class_name == "Abatracto":
                    await ctx.send("""Tu dibujo es de estilo abstracto. El
                    arte abstracto busca trasmitir emociones, y generalmente
                    no siguen ningun orden o patron definido.
                    Acá va un ejemplo de un diujo de este estilo:""")
                    Abatracto = os.listdir("Abatracto")
                    img_name2 = random.choice(Abatracto)
                    with open(f'Abatracto/{img_name2}', 'rb') as f:
                        picture2 = discord.File(f)
                    await ctx.send(file=picture2)

                elif class_name == "Comic":
                    await ctx.send("""Tu dibujo es de estilo de comic. Este
                    estilo de dibujo se caracteriza por tener líneas claras,
                    colores vivos y escenas que cuentan una historia de manera
                    visual. Acá va un ejemplo de un diujo de este estilo:""")
                    Comic = os.listdir("Comic")
                    img_name = random.choice(Comic)
                    with open(f'Comic/{img_name}', 'rb') as f:
                        picture = discord.File(f)
                    await ctx.send(file=picture)

                elif class_name == "Pixel Art":
                    await ctx.send("""Tu dibujo es de estilo pixel art. El
                    Pixel Art es un estilo que utiliza pequeños bloques de
                    colores para construir imágenes. Este estilo de dibujo se
                    usa generalment en juegos retro. Acá va un ejemplo de
                    un diujo de este estilo:""")
                    Pixel = os.listdir("Pixel Art")
                    img_name = random.choice(Pixel)
                    with open(f'Pixel Art/{img_name}', 'rb') as f:
                        picture = discord.File(f)
                    await ctx.send(file=picture)

            except:
                await ctx.send("ERROR")
    else:
        await ctx.send("No hay archivos adjuntos en el mensaje")

bot.run("TOKEN")
