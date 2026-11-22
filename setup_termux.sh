#!/data/data/com.termux/files/usr/bin/bash
# Instala todo lo necesario para correr Kairon en Termux (Android).
set -e
pkg update -y && pkg upgrade -y
pkg install -y python git ollama
nohup ollama serve > ollama.log 2>&1 &
sleep 5
ollama pull qwen2.5:1.5b
echo "Listo. Ejecuta: python kairon.py"
