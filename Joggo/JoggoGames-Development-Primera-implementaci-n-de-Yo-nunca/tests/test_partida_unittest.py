# test_partida_unittest.py

import unittest
import httpx
import asyncio

class TestPartidaFlow(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """
        Configuración que se ejecuta antes de cada prueba asíncrona.
        """
        self.base_url = "http://localhost:8000"
        self.client = httpx.AsyncClient(base_url=self.base_url)
    
    async def asyncTearDown(self):
        """
        Limpieza que se ejecuta después de cada prueba asíncrona.
        """
        await self.client.aclose()
    
    async def test_full_flow(self):
        """
        Prueba completa del flujo de juego:
        Registro de usuarios, creación de partida, unión, inicio, envío de frases,
        respuestas y obtención de resultados finales.
        """
        try:
            # Registrar el bar
            response = await self.client.post("/register", json={
                "nombre": "Bar XYZ",
                "tipo": "bar"
            })
            self.assertEqual(response.status_code, 200, f"Registro del bar falló: {response.text}")
            bar_token = response.json()["access_token"]
            print("Bar Registrado con Token:", bar_token)
        except Exception as e:
            self.fail(f"Excepción al registrar el bar: {e}")

        try:
            # Registrar Jugador 1: Alice
            response = await self.client.post("/register", json={
                "nombre": "Alice",
                "tipo": "jugador"
            })
            self.assertEqual(response.status_code, 200, f"Registro de Alice falló: {response.text}")
            alice_token = response.json()["access_token"]
            print("Alice Registrada con Token:", alice_token)
        except Exception as e:
            self.fail(f"Excepción al registrar a Alice: {e}")

        try:
            # Registrar Jugador 2: Bob
            response = await self.client.post("/register", json={
                "nombre": "Bob",
                "tipo": "jugador"
            })
            self.assertEqual(response.status_code, 200, f"Registro de Bob falló: {response.text}")
            bob_token = response.json()["access_token"]
            print("Bob Registrado con Token:", bob_token)
        except Exception as e:
            self.fail(f"Excepción al registrar a Bob: {e}")

        try:
            # Crear una partida enviando 'juego' en el cuerpo JSON
            response = await self.client.post("/partida/", json={
                "juego": "Yo Nunca"
            }, headers={
                "Authorization": f"Bearer {bar_token}"
            })
            self.assertEqual(response.status_code, 200, f"Creación de partida falló: {response.text}")
            partida = response.json()
            partida_id = partida["id"]
            print("Partida Creada:", partida)
        except Exception as e:
            self.fail(f"Excepción al crear la partida: {e}")

        try:
            # Alice se une a la partida
            response = await self.client.post(f"/unirse/{partida_id}", headers={
                "Authorization": f"Bearer {alice_token}"
            })
            self.assertEqual(response.status_code, 200, f"Alice no pudo unirse a la partida: {response.text}")
            print("Alice se Unió a la Partida:", response.json())
        except Exception as e:
            self.fail(f"Excepción al unir a Alice a la partida: {e}")

        try:
            # Bob se une a la partida
            response = await self.client.post(f"/unirse/{partida_id}", headers={
                "Authorization": f"Bearer {bob_token}"
            })
            self.assertEqual(response.status_code, 200, f"Bob no pudo unirse a la partida: {response.text}")
            print("Bob se Unió a la Partida:", response.json())
        except Exception as e:
            self.fail(f"Excepción al unir a Bob a la partida: {e}")

        try:
            # Iniciar la partida
            response = await self.client.post(f"/partida/{partida_id}/iniciar", headers={
                "Authorization": f"Bearer {bar_token}"
            })
            self.assertEqual(response.status_code, 200, f"Inicio de partida falló: {response.text}")
            print("Partida Iniciada:", response.json())
        except Exception as e:
            self.fail(f"Excepción al iniciar la partida: {e}")

        try:
            # Alice envía una frase
            response = await self.client.post(f"/partida/{partida_id}/frase", json={
                "texto": "Yo nunca he viajado al extranjero."
            }, headers={
                "Authorization": f"Bearer {alice_token}"
            })
            self.assertEqual(response.status_code, 200, f"Alice no pudo enviar una frase: {response.text}")
            frase_alice = response.json()
            print("Frase de Alice Enviada:", frase_alice)
        except Exception as e:
            self.fail(f"Excepción al enviar la frase de Alice: {e}")

        try:
            # Bob envía una frase
            response = await self.client.post(f"/partida/{partida_id}/frase", json={
                "texto": "Yo nunca he hecho paracaidismo."
            }, headers={
                "Authorization": f"Bearer {bob_token}"
            })
            self.assertEqual(response.status_code, 200, f"Bob no pudo enviar una frase: {response.text}")
            frase_bob = response.json()
            print("Frase de Bob Enviada:", frase_bob)
        except Exception as e:
            self.fail(f"Excepción al enviar la frase de Bob: {e}")

        try:
            # Obtener la primera frase actual (Frase de Alice)
            response = await self.client.get(f"/partida/{partida_id}/frase_actual", headers={
                "Authorization": f"Bearer {bar_token}"
            })
            self.assertEqual(response.status_code, 200, f"Obtención de frase actual falló: {response.text}")
            frase_actual = response.json()
            print("Frase Actual:", frase_actual)
        except Exception as e:
            self.fail(f"Excepción al obtener la frase actual: {e}")

        try:
            # Alice responde a la frase actual
            response = await self.client.post(f"/partida/{partida_id}/frase/{frase_actual['id']}/respuesta", json={
                "hecho": False
            }, headers={
                "Authorization": f"Bearer {alice_token}"
            })
            self.assertEqual(response.status_code, 200, f"Alice no pudo responder a la frase: {response.text}")
            respuesta_alice = response.json()
            print("Respuesta de Alice:", respuesta_alice)
        except Exception as e:
            self.fail(f"Excepción al enviar la respuesta de Alice: {e}")

        try:
            # Bob responde a la frase actual
            response = await self.client.post(f"/partida/{partida_id}/frase/{frase_actual['id']}/respuesta", json={
                "hecho": True
            }, headers={
                "Authorization": f"Bearer {bob_token}"
            })
            self.assertEqual(response.status_code, 200, f"Bob no pudo responder a la frase: {response.text}")
            respuesta_bob = response.json()
            print("Respuesta de Bob:", respuesta_bob)
        except Exception as e:
            self.fail(f"Excepción al enviar la respuesta de Bob: {e}")

        try:
            # Obtener la segunda frase actual (Frase de Bob)
            response = await self.client.get(f"/partida/{partida_id}/frase_actual", headers={
                "Authorization": f"Bearer {bar_token}"
            })
            self.assertEqual(response.status_code, 200, f"Obtención de segunda frase actual falló: {response.text}")
            frase_actual = response.json()
            print("Segunda Frase Actual:", frase_actual)
        except Exception as e:
            self.fail(f"Excepción al obtener la segunda frase actual: {e}")

        try:
            # Alice responde a la segunda frase actual
            response = await self.client.post(f"/partida/{partida_id}/frase/{frase_actual['id']}/respuesta", json={
                "hecho": True
            }, headers={
                "Authorization": f"Bearer {alice_token}"
            })
            self.assertEqual(response.status_code, 200, f"Alice no pudo responder a la segunda frase: {response.text}")
            respuesta_alice_2 = response.json()
            print("Respuesta de Alice a la Segunda Frase:", respuesta_alice_2)
        except Exception as e:
            self.fail(f"Excepción al enviar la segunda respuesta de Alice: {e}")

        try:
            # Bob responde a la segunda frase actual
            response = await self.client.post(f"/partida/{partida_id}/frase/{frase_actual['id']}/respuesta", json={
                "hecho": False
            }, headers={
                "Authorization": f"Bearer {bob_token}"
            })
            self.assertEqual(response.status_code, 200, f"Bob no pudo responder a la segunda frase: {response.text}")
            respuesta_bob_2 = response.json()
            print("Respuesta de Bob a la Segunda Frase:", respuesta_bob_2)
        except Exception as e:
            self.fail(f"Excepción al enviar la segunda respuesta de Bob: {e}")

if __name__ == "__main__":
    unittest.main()
