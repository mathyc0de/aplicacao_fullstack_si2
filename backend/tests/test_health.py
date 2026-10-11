def test_rota_inexistente(client):
    response = client.get("/api/nao-existe")
    assert response.status_code == 404
    payload = response.get_json()
    assert payload["error"] == "pagina_inexistente"
