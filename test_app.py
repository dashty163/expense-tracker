from fastapi.testclient import TestClient

from app_final import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": 'ok'}

def test_root():
    response = client.get('/')

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Expense Tracker API'
    assert "app_name" in data
    
def test_version():
    response = client.get('/version')
    
    assert response.status_code == 200
    assert response.json() == {"version":"0.1.0"}
    
def test_add_expences():
    new_expense_data = {
            "title": 'cofe',
            "amount": '400',
            "category": 'food'}
    response = client.post('/expenses', json=new_expense_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data['title'] == 'cofe'
    assert data['amount'] == '400'
    assert data['category'] == 'food'
    assert 'id' in data
    
    
def test_filter_by_category():
    client.post("/expenses", json={"title": "apple", "amount": 50.0, "category": "food"})
    client.post("/expenses", json={"title": "bus",   "amount": 30.0, "category": "transport"})

    response = client.get('/expenses', params = {'category' : 'food'})
    data = response.json()
    
    for e in data:
        assert e['category'] == 'food'
    
def test_get_id():
    created = client.post("/expenses", json={
        "title": "taxi", "amount": 300.0, "category": "transport"
    }).json()
    expense_id = created["id"]

    
    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["title"] == "taxi"

