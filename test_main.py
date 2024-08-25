import unittest
from fastapi.testclient import TestClient
from main import app, expenses
from datetime import datetime

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        expenses.clear()
        print("Setup: Cleared expenses")

    def test_add_expense(self):
        response = self.client.post("/add_expense", json={
            "date": datetime.now().isoformat(),
            "category": "Food",
            "amount": 20.5,
            "description": "Lunch at ABC Cafe"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Expense added successfully"})

    def test_view_expenses(self):
        # First, add an expense
        self.client.post("/add_expense", json={
            "date": datetime.now().isoformat(),
            "category": "Food",
            "amount": 20.5,
            "description": "Lunch at ABC Cafe"
        })
        
        # Then, view all expenses
        response = self.client.get("/view_expenses")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_view_expenses_by_category(self):
        # First, add an expense
        self.client.post("/add_expense", json={
            "date": datetime.now().isoformat(),
            "category": "Food",
            "amount": 20.5,
            "description": "Lunch at ABC Cafe"
        })
        
        # Then, view expenses by category
        response = self.client.get("/view_expenses_by_category?category=Food")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

        # Test non-existent category
        response = self.client.get("/view_expenses_by_category?category=NonExistent")
        self.assertEqual(response.status_code, 404)

    def test_view_total_expenses(self):
        print("Initial expenses:", expenses)
        # First, add some expenses
        self.client.post("/add_expense", json={
            "date": datetime.now().isoformat(),
            "category": "Food",
            "amount": 20.5,
            "description": "Lunch at ABC Cafe"
        })
        self.client.post("/add_expense", json={
            "date": datetime.now().isoformat(),
            "category": "Transport",
            "amount": 15.0,
            "description": "Bus fare"
        })

        print("Expenses after adding:", expenses)

        # Then, view total expenses
        response = self.client.get("/view_total_expenses")
        self.assertEqual(response.status_code, 200)
        print("Total expenses response:", response.json())
        self.assertEqual(response.json(), {"total_amount": 35.5})

if __name__ == "__main__":
    unittest.main()
