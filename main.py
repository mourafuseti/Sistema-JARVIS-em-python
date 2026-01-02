import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
from google import genai
import os
import winsound  # Biblioteca para o som de bipe

# ==========================================
# CONFIGURAÇÃO
# ==========================================
API_KEY = "SUA_CHAVE_AQUI" 
client = genai.Client(api_key=API_KEY)
engine = pyttsx3.init()

# Ajuste de Voz
engine.setProperty('rate', 180)

def sinal_sonoro():
    """ Toca um bipe rápido (Frequência, Duração) """
    winsound.Beep(1000, 150) # 1000Hz por 150ms

def falar(texto):
    print(f"Jarvis: {texto}")
    engine.say(texto)
    engine.runAndWait()

def gravar_e_ouvir():
    fs = 44100  
    segundos = 4 
    arquivo_temp = 'temp_audio.wav'
    
    if os.path.exists(arquivo_temp):
        os.remove(arquivo_temp)

    # Toca o bipe antes de começar a ouvir
    sinal_sonoro()
    print("\n--- [Escutando...] ---")
    
    gravacao = sd.rec(int(segundos * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait() 
    
    audio_int16 = (gravacao * 32767).astype(np.int16)
    write(arquivo_temp, fs, audio_int16) 

    reconhecedor = sr.Recognizer()
    try:
        with sr.AudioFile(arquivo_temp) as source:
            audio = reconhecedor.record(source)
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"Você: {texto}")
            return texto.lower()
    except:
        return ""

# --- LOOP PRINCIPAL ---
falar("Sistemas online, senhor. Aguardando comandos.")

while True:
    comando = gravar_e_ouvir()
    
    if comando:
        if "desligar" in comando or "encerrar" in comando:
            falar("Desligando, senhor. Até a próxima.")
            break
        
        try:
            # Usando gemini-2.0-flash (Mais moderno e evita erro 404)
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=f"Responda como o Jarvis: {comando}"
            )
            falar(response.text)
        except Exception as e:
            print(f"Erro: {e}")
            falar("Tive um erro no processador central.")