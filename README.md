# Baking Wishes Inventory Manager

## Project Overview
Baking Wishes Inventory Manager is a multi-page Streamlit web application designed to help a bakery manage inventory, sales, restocking, and low-stock alerts. The app supports two user roles: bakery owner and bakery employee.

## Features
- User registration and login
- Logout functionality
- Owner and employee role-based dashboards
- Inventory create, read, update, and delete functionality
- Sales logging
- Low-stock flagging
- JSON data persistence
- AI inventory assistant using OpenAI
- Test accounts with sample data

## Technologies Used
- Python
- Streamlit
- JSON
- OpenAI API
- Object-Oriented Programming

## File Structure
- `App.py` - main Streamlit app and page routing
- `data_manager.py` - JSON loading and saving through the DataManager class
- `services.py` - inventory business logic through the InventoryService class
- `ai_assistant.py` - OpenAI chatbot logic through the AIChatAssistant class
- `users.json` - sample user accounts
- `inventory.json` - sample inventory data
- `sales.json` - sample sales records
- `flags.json` - sample low-stock alerts

## Test Accounts

Owner Account:
- Email: owner@bakery.com
- Password: owner123

Employee Account:
- Email: employee@bakery.com
- Password: employee123

## How to Run
```bash
pip install -r requirements.txt
streamlit run App.py