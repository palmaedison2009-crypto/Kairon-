#!/usr/bin/env python3
"""Kairon: IA personal local (estilo OpenJarvis).
Habla con un modelo que corre en tu propio celular via Ollama.
Sin dependencias: solo Python estandar."""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime

URL = os.environ.get("KAIRON_URL", "http://localhost:11434")
MODELO = os.environ.get("KAIRON_MODELO", "qwen2.5:1.5b")
AQUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MEMORIA = os.path.join(AQUI, "memoria.json")
MAX_HISTORIAL = 20

BASE = (
    "Eres Kairon, un asistente personal que corre en local en el celular "
    "de tu usuario. Responde en español, de forma breve y clara."
)


def cargar_memoria():
    try:
        with open(ARCHIVO_MEMORIA, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_memoria(notas):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)


def prompt_sistema(notas):
    if not notas:
        return BASE
    lista = "\n".join(f"- {n}" for n in notas)
    return f"{BASE}\nCosas que el usuario te pidio recordar:\n{lista}"


def chatear(mensajes):
    cuerpo = json.dumps(
        {"model": MODELO, "messages": mensajes, "stream": True}
    ).encode()
    req = urllib.request.Request(
        f"{URL}/api/chat",
        data=cuerpo,
        headers={"Content-Type": "application/json"},
    )
    respuesta = ""
    with urllib.request.urlopen(req, timeout=600) as r:
        for linea in r:
            if not linea.strip():
                continue
            trozo = json.loads(linea)
            texto = trozo.get("message", {}).get("content", "")
            print(texto, end="", flush=True)
            respuesta += texto
            if trozo.get("done"):
                break
    print()
    return respuesta


AYUDA = """Comandos:
  /hora            hora y fecha actuales
  /recordar texto  guarda una nota en la memoria de Kairon
  /memoria         muestra lo que recuerda
  /olvidar         borra la memoria
  /ayuda           muestra esto
  /salir           termina"""


def main():
    notas = cargar_memoria()
    historial = []
    print(f"Kairon listo (modelo: {MODELO}). Escribe /ayuda para ver comandos.")
    while True:
        try:
            entrada = input("\ntu> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break
        if not entrada:
            continue

        if entrada == "/salir":
            print("Hasta luego.")
            break
        if entrada == "/ayuda":
            print(AYUDA)
            continue
        if entrada == "/hora":
            print(datetime.now().strftime("%A %d/%m/%Y, %H:%M"))
            continue
        if entrada.startswith("/recordar"):
            texto = entrada[len("/recordar"):].strip()
            if texto:
                notas.append(texto)
                guardar_memoria(notas)
                print("Guardado.")
            else:
                print("Uso: /recordar lo que quieras que recuerde")
            continue
        if entrada == "/memoria":
            print("\n".join(f"- {n}" for n in notas) or "(vacia)")
            continue
        if entrada == "/olvidar":
            notas = []
            guardar_memoria(notas)
            print("Memoria borrada.")
            continue

        historial.append({"role": "user", "content": entrada})
        historial = historial[-MAX_HISTORIAL:]
        mensajes = [{"role": "system", "content": prompt_sistema(notas)}] + historial
        print("kairon> ", end="", flush=True)
        try:
            respuesta = chatear(mensajes)
        except urllib.error.URLError:
            print(
                "\nNo me conecto a Ollama. Inicialo con:\n"
                "  ollama serve > ollama.log 2>&1 &"
            )
            historial.pop()
            continue
        historial.append({"role": "assistant", "content": respuesta})


if __name__ == "__main__":
    main()
