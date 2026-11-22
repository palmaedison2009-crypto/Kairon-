# Kairon

IA personal que corre **en local**, en tu celular, inspirada en OpenJarvis.

## Instalar (Android + Termux)

1. Instala Termux desde F-Droid.
2. Clona el repo y corre el instalador:

```bash
git clone https://github.com/TU_USUARIO/kairon.git
cd kairon
bash setup_termux.sh
```

3. Ejecuta:

```bash
python kairon.py
```

## Comandos

`/hora`, `/recordar texto`, `/memoria`, `/olvidar`, `/ayuda`, `/salir`

## Cambiar de modelo

```bash
ollama pull qwen2.5:3b
KAIRON_MODELO=qwen2.5:3b python kairon.py
```

## Hoja de ruta

- [x] Chat local con memoria simple
- [ ] Herramientas (clima, calendario, archivos)
- [ ] Agentes programados (resumen diario)
- [ ] Voz
