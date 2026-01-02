import tkinter as tk
from tkinter import scrolledtext
import threading
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
from google import genai
import os
import winsound
import time

# ==========================================
# CONFIGURAÇÃO - COLOQUE SUA CHAVE AQUI
# ==========================================
API_KEY = "COLOQUE SUA CHAVE AQUI" 
# ==========================================

client = genai.Client(api_key=API_KEY)
engine = pyttsx3.init()
engine.setProperty('rate', 180)

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S. - Protocolo de Interface")
        self.root.geometry("550x650")
        self.root.configure(bg="#0f172a")

        # Título Estilizado
        self.label = tk.Label(root, text="J.A.R.V.I.S.", font=("Orbitron", 28, "bold"), fg="#38bdf8", bg="#0f172a")
        self.label.pack(pady=20)

        # Chat Log
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=22, bg="#1e293b", fg="white", font=("Consolas", 10), bd=0)
        self.chat_area.pack(pady=10, padx=20)

        # Status do Sistema
        self.status_frame = tk.Frame(root, bg="#0f172a")
        self.status_frame.pack(pady=5)
        
        self.status_indicator = tk.Label(self.status_frame, text="●", fg="#22c55e", bg="#0f172a", font=("Arial", 12))
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(self.status_frame, text="SISTEMA ONLINE", fg="#22c55e", bg="#0f172a", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Botão de Ativação
        self.btn_ouvir = tk.Button(root, text="ATIVAR MICROFONE", command=self.start_listening_thread, 
                                  bg="#38bdf8", fg="black", font=("Arial", 12, "bold"), 
                                  activebackground="#0ea5e9", width=25, height=2, bd=0)
        self.btn_ouvir.pack(pady=20)

    def log(self, sender, message):
        """ Adiciona mensagens visualmente na interface """
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.see(tk.END)

    def falar(self, texto):
        """ Mostra o texto no chat e fala através do pyttsx3 """
        self.log("JARVIS", texto)
        engine.say(texto)
        engine.runAndWait()

    def gravar_e_ouvir(self):
        """ Faz a gravação e converte para texto """
        fs = 44100  
        segundos = 4 
        arquivo_temp = 'temp_audio.wav'
        
        if os.path.exists(arquivo_temp):
            os.remove(arquivo_temp)

        # Altera interface para estado de escuta
        self.status_label.config(text="ESCUTANDO...", fg="#ef4444")
        self.status_indicator.config(fg="#ef4444")
        winsound.Beep(1000, 150) # Som de início
        
        try:
            gravacao = sd.rec(int(segundos * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait() 
            
            audio_int16 = (gravacao * 32767).astype(np.int16)
            write(arquivo_temp, fs, audio_int16) 
            
            self.status_label.config(text="PROCESSANDO VOZ...", fg="#eab308")
            self.status_indicator.config(fg="#eab308")

            reconhecedor = sr.Recognizer()
            with sr.AudioFile(arquivo_temp) as source:
                audio = reconhecedor.record(source)
                texto = reconhecedor.recognize_google(audio, language='pt-BR')
                self.log("VOCÊ", texto)
                return texto.lower()
        except Exception:
            self.log("SISTEMA", "Nenhum áudio detectado.")
            return ""

    def processar_ia(self):
        """ Lógica da IA em Thread separada para não travar a janela """
        comando = self.gravar_e_ouvir()
        
        if comando:
            if "desligar" in comando:
                self.falar("Desligando sistemas, senhor.")
                self.root.quit()
                return

            try:
                # Usando 1.5-flash para maior compatibilidade de cota
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=f"Responda como o Jarvis: {comando}"
                )
                self.falar(response.text)
            except Exception as e:
                # Tratamento para erro de Cota Excedida (429)
                if "429" in str(e):
                    msg = "Senhor, excedemos o limite de requisições gratuitas. Aguarde um minuto."
                    self.log("AVISO", msg)
                    engine.say(msg)
                    engine.runAndWait()
                else:
                    self.log("ERRO", f"Falha na API: {str(e)}")
        
        # Volta ao estado normal
        self.status_label.config(text="AGUARDANDO COMANDO", fg="#22c55e")
        self.status_indicator.config(fg="#22c55e")

    def start_listening_thread(self):
        """ Cria e inicia a thread para processar o áudio """
        threading.Thread(target=self.processar_ia, daemon=True).start()

# Execução do Aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisApp(root)
    # Saudação inicial
    threading.Thread(target=lambda: app.falar("Interface carregada. Protocolos ativos, senhor."), daemon=True).start()
    root.mainloop()