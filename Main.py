import pandas as pd
from User import *
from ytmusicapi import YTMusic
from funcionalidades import *  # Importa las funcionalidades
import os

# Inicializa la API de YTMusic con el archivo oauth.json
ytmusic = YTMusic("oauth.json")

# %%% CSV
try:
    bdd = pd.read_csv("users.csv", sep=',')
    print(bdd)
except FileNotFoundError:
    columns = ["userId", 'name', 'password', 'admin']
    bdd = pd.DataFrame(columns=columns)
    bdd.to_csv("users.csv", index=False, sep=',')

# Asegúrate de que las columnas 'name' y 'password' sean cadenas
bdd['name'] = bdd['name'].astype(str)
bdd['password'] = bdd['password'].astype(str)

# %%% Comienza el programa
print("Bienvenido a No ADS radio.")

try:
    while True:
        print("1. Iniciar sesión 2. Registrarse 3. Salir")
        welcome = input("").strip().lower()

        if welcome == "login" or welcome == "1":
            print("Iniciando sesión...")

            loginName = input("Ingresa tu nombre: ").strip().lower()
            loginPassword = input("Ingresa tu contraseña: ").strip().lower()

            user = bdd[(bdd['name'].str.strip().str.lower() == loginName) & (bdd['password'].str.strip() == loginPassword)]

            if not user.empty:
                print(f"¡Bienvenido de nuevo, {loginName}!")
                while True:
                    print("\nMenú:")
                    print("1. Buscar música")
                    print("2. Música descargada")
                    print("3. Detener música")
                    print("4. Saltar música")
                    print("5. Salir")
                    choice = input("Elige una opción: ").strip()

                    if choice == "1":
                        search_query = input("Ingresa el título de la canción o artista a buscar: ").strip()
                        results = ytmusic.search(search_query)

                        if results:
                            print("Resultados de búsqueda:")
                            for index, song in enumerate(results):
                                title = song.get('title', 'Sin título')
                                artist = ', '.join(artist['name'] for artist in song.get('artists', [{'name': 'Artista Desconocido'}]))
                                print(f"{index + 1}. {title} de {artist}")

                            song_choice = input("Ingresa el número de la canción para reproducir o agregar a la cola: ").strip()
                            if song_choice.isdigit() and 0 < int(song_choice) <= len(results):
                                selected_song = results[int(song_choice) - 1]
                                video_id = selected_song.get('videoId', None)
                                title = selected_song.get('title', 'Título Desconocido').replace('/', '-')  # Reemplaza barras para evitar problemas
                                if video_id:
                                    queue_song(video_id, title)  # Agrega la canción a la cola directamente
                                else:
                                    print("ID de video no encontrado para la canción seleccionada.")
                            else:
                                print("Elección inválida.")
                        else:
                            print("No se encontraron resultados.")

                    elif choice == "2":
                        search_saved_music()

                    elif choice == "3":
                        stop_music()

                    elif choice == "4":
                        skip_song()

                    elif choice == "5":
                        print("¡Hasta pronto!")
                        break  # Salir al menú principal

                    else:
                        print("Opción no válida.")

                break
            else:
                print("Credenciales inválidas. Por favor, inténtalo de nuevo.")

        elif welcome == "signup" or welcome == "2":
            print("Muy bien, vamos a crear una cuenta.")

            if not bdd.empty:
                lastUserId = int(bdd['userId'].max())
                newUserId = lastUserId + 1
            else:
                newUserId = 2

            newName = input("Ingresa tu nombre: ").strip().lower()
            newPassword = input("Ingresa tu contraseña: ").strip().lower()

            newUser = {
                'userId': newUserId,
                'name': newName,
                'password': newPassword,
                'admin': False
            }

            bdd = pd.concat([bdd, pd.DataFrame([newUser])], ignore_index=True)
            bdd.to_csv('users.csv', index=False, sep=',')
            print(f"El usuario {newName} ha sido creado con ID {newUserId}.")
            print("Regresando al menú principal...")

        elif welcome == "exit" or welcome == "3":
            print("Saliendo de No ADS radio. ¡Adiós!")
            break  

        else:
            print("Lo siento, no entiendo lo que dices.")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
finally:
    cleanup_current_song()  # Asegúrate de que la limpieza ocurra al salir

