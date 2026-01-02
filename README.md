```markdown
# 🎙️ J.A.R.V.I.S. - Assistente Virtual com Python & Gemini

Este é um projeto de assistente virtual inspirado no Jarvis do Homem de Ferro. Ele utiliza reconhecimento de voz, síntese de fala e a inteligência artificial do Google Gemini para interagir com o usuário através de uma interface gráfica moderna feita em Tkinter.



## ✨ Funcionalidades

* **Reconhecimento de Voz:** Escuta comandos em português através do microfone.
* **Inteligência Artificial:** Processa perguntas e gera respostas inteligentes usando o modelo Gemini 1.5 Flash.
* **Voz Própria:** Responde verbalmente ao usuário.
* **Interface Gráfica (GUI):** Janela interativa que exibe o log da conversa e o status do sistema.
* **Sinais Sonoros:** Bipes que indicam o momento exato de falar.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **IA:** Google Generative AI (Gemini API)
* **Interface:** Tkinter
* **Voz (STT/TTS):** SpeechRecognition, Pyttsx3, SoundDevice

## 🚀 Como Instalar

1.  **Clone o repositório ou baixe os arquivos.**
2.  **Instale as dependências necessárias:**

```powershell
pip install sounddevice numpy scipy speechrecognition pyttsx3 google-genai

```

3. **Obtenha sua API Key do Gemini:**
* Acesse o [Google AI Studio](https://aistudio.google.com/).
* Gere uma nova chave e cole-a no arquivo `main.py` na variável `API_KEY`.



## 💻 Como Usar

1. Execute o script principal:
```powershell
python main.py

```


2. Aguarde a saudação do Jarvis.
3. Clique no botão **"ATIVAR MICROFONE"**.
4. Após o sinal sonoro (bipe), faça sua pergunta ou dê um comando.
5. Diga **"Jarvis, desligar"** ou clique para fechar a janela quando terminar.

## ⚠️ Observações sobre a Cota (Erro 429)

Como este projeto utiliza a versão gratuita da API do Gemini, existe um limite de requisições por minuto. Caso receba um aviso de "Cota Excedida", aguarde cerca de 60 segundos antes de tentar novamente.

---

Desenvolvido por [Leonardo de moura fuseti] - 2026 🚀

```

---

