import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(
    page_title="Baking Wishes Inventory Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# file paths 
USERS_FILE = Path("users.json")
INVENTORY_FILE = Path("inventory.json")
SALES_FILE = Path("sales.json")
FLAGS_FILE = Path("flags.json")

# Data 
DEFAULT_USERS = [
    {
        "user_id": "100",
        "name": "Bakery Owner",
        "email": "owner@bakery.com",
        "password": "owner123",
        "role": "owner"
    },
    {
        "user_id": "101",
        "name": "Bakery Employee",
        "email": "employee@bakery.com",
        "password": "employee123",
        "role": "employee"
    }
]

DEFAULT_INVENTORY = [
    {"item_id": 1, "name": "Donut", "unit_price": 2.50, "stock": 60},
    {"item_id": 2, "name": "Croissant", "unit_price": 3.00, "stock": 30},
    {"item_id": 3, "name": "Muffin", "unit_price": 4.50, "stock": 50},
    {"item_id": 4, "name": "Cookie", "unit_price": 2.75, "stock": 100},
    {"item_id": 5, "name": "Pie", "unit_price": 10.00, "stock": 20},
    {"item_id": 6, "name": "Brownie", "unit_price": 3.50, "stock": 50}
]

DEFAULT_SALES = []
DEFAULT_FLAGS = []

# data functions
def load_json_file(path, default_data):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
            return default_data
    except:
        return default_data

def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

users = load_json_file(USERS_FILE, DEFAULT_USERS)
inventory = load_json_file(INVENTORY_FILE, DEFAULT_INVENTORY)
sales = load_json_file(SALES_FILE, DEFAULT_SALES)
flags = load_json_file(FLAGS_FILE, DEFAULT_FLAGS)

# Session state 
def initialize_session_state():
    defaults = {
        "page": "login",
        "logged_in": False,
        "user_id": None,
        "name": "",
        "role": None,
        "messages": [
            {
                "role": "assistant",
                "content": "Hi! I can help you with your baking inventory questions."
            }
        ]
    }

    for key in defaults:
        if key not in st.session_state:
            st.session_state[key] = defaults[key]

initialize_session_state()

#cleaning 
def clean_text(text):
    return text.strip()

def valid_email(email):
    email = email.strip()
    return "@" in email and "." in email and " " not in email

def go_to_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()

def logout():
    st.session_state["logged_in"] = False
    st.session_state["user_id"] = None
    st.session_state["name"] = ""
    st.session_state["role"] = None
    st.session_state["page"] = "login"
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi! I can help you with your baking inventory questions."
        }
    ]
    st.rerun()

def require_role(allowed_roles):
    if not st.session_state["logged_in"]:
        st.error("Please log in first.")
        st.stop()

    if st.session_state["role"] not in allowed_roles:
        st.error("You do not have permission to access this page.")
        st.stop()

def show_page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()

def show_empty_message(message):
    st.info(message)

def get_next_item_id():
    if len(inventory) == 0:
        return 1
    return max(item["item_id"] for item in inventory) + 1

def get_item_by_name(item_name):
    for item in inventory:
        if item["name"] == item_name:
            return item
    return None

def get_item_names():
    return [item["name"] for item in inventory]

def get_low_stock_items():
    return [item for item in inventory if item["stock"] < 5]

def get_inventory_value():
    total = 0
    for item in inventory:
        total += item["unit_price"] * item["stock"]
    return total

#inventory table
def inventory_table_data():
    rows = []
    for item in inventory:
        rows.append({
            "Item ID": item["item_id"],
            "Item Name": item["name"],
            "Unit Price": f"${item['unit_price']:.2f}",
            "Stock": item["stock"]
        })
    return rows

def low_stock_table_data():
    rows = []
    for item in get_low_stock_items():
        rows.append({
            "Item ID": item["item_id"],
            "Item Name": item["name"],
            "Unit Price": f"${item['unit_price']:.2f}",
            "Stock": item["stock"]
        })
    return rows

def sales_table_data():
    rows = []
    for sale in sales:
        item_name = "Unknown"
        for item in inventory:
            if item["item_id"] == sale["item_id"]:
                item_name = item["name"]
                break

        rows.append({
            "Sale ID": sale["sale_id"],
            "Item Name": item_name,
            "Employee ID": sale["employee_id"],
            "Quantity": sale["quantity"],
            "Total": f"${sale['total']:.2f}",
            "Sale Date": sale["sale_date"]
        })
    return rows

def flags_table_data():
    rows = []
    for flag in flags:
        item_name = "Unknown"
        for item in inventory:
            if item["item_id"] == flag["item_id"]:
                item_name = item["name"]
                break

        rows.append({
            "Flag ID": flag["flag_id"],
            "Item Name": item_name,
            "Employee ID": flag["employee_id"],
            "Message": flag["message"],
            "Date Flagged": flag["date_flagged"]
        })
    return rows

#wrapping 
def save_users_data():
    return save_json_file(USERS_FILE, users)

def save_inventory_data():
    return save_json_file(INVENTORY_FILE, inventory)

def save_sales_data():
    return save_json_file(SALES_FILE, sales)

def save_flags_data():
    return save_json_file(FLAGS_FILE, flags)

#helpers
def render_inventory_table():
    if len(inventory) == 0:
        show_empty_message("No inventory items found.")
    else:
        st.dataframe(inventory_table_data(), use_container_width=True, hide_index=True)

def render_sales_table():
    if len(sales) == 0:
        show_empty_message("No sales have been logged yet.")
    else:
        st.dataframe(sales_table_data(), use_container_width=True, hide_index=True)

def render_flags_table():
    if len(flags) == 0:
        show_empty_message("No low stock alerts yet.")
    else:
        st.dataframe(flags_table_data(), use_container_width=True, hide_index=True)

#the sidebar 
def render_sidebar():
    with st.sidebar:
        st.title("Baking Wishes")
        st.caption("Inventory Manager")
        st.divider()

        if not st.session_state["logged_in"]:
            st.info("Please log in or register to continue.")

            if st.button("Login", key="sidebar_login_btn", use_container_width=True, type="primary"):
                go_to_page("login")

            if st.button("Register", key="sidebar_register_btn", use_container_width=True):
                go_to_page("register")

        else:
            st.success(f"Logged in as {st.session_state['name']}")
            st.caption(f"Role: {st.session_state['role'].title()}")
            st.divider()

            if st.session_state["role"] == "owner":
                if st.button("Owner Dashboard", key="sidebar_owner_dashboard_btn", use_container_width=True):
                    go_to_page("owner_dashboard")

                if st.button("Manage Inventory", key="sidebar_manage_inventory_btn", use_container_width=True):
                    go_to_page("manage_inventory")

                if st.button("Restock Inventory", key="sidebar_restock_inventory_btn", use_container_width=True):
                    go_to_page("restock_inventory")

                if st.button("Sales Records", key="sidebar_sales_records_btn", use_container_width=True):
                    go_to_page("sales_records")

                if st.button("Low Stock Alerts", key="sidebar_low_stock_alerts_btn", use_container_width=True):
                    go_to_page("low_stock_alerts")

            elif st.session_state["role"] == "employee":
                if st.button("Employee Dashboard", key="sidebar_employee_dashboard_btn", use_container_width=True):
                    go_to_page("employee_dashboard")

                if st.button("View Catalog", key="sidebar_view_catalog_btn", use_container_width=True):
                    go_to_page("view_catalog")

                if st.button("Log Sales", key="sidebar_log_sales_btn", use_container_width=True):
                    go_to_page("log_sales")

                if st.button("Flag Low Stock", key="sidebar_flag_low_stock_btn", use_container_width=True):
                    go_to_page("flag_low_stock")

                if st.button("Chatbot", key="sidebar_chatbot_btn", use_container_width=True):
                    go_to_page("chatbot")

            st.divider()

            if st.button("Logout", key="sidebar_logout_btn", use_container_width=True):
                logout()

render_sidebar()

#making the pages work 
def render_login_page():
    show_page_header("Bakery Inventory Login", "Log in to access your bakery dashboard.")

    left, center, right = st.columns([1, 2, 1])

    with center:
        email = st.text_input("Email", key="login_email_input")
        password = st.text_input("Password", type="password", key="login_password_input")

        if st.button("Login Now", key="login_submit_btn", use_container_width=True, type="primary"):
            email = clean_text(email)
            password = clean_text(password)

            if email == "" or password == "":
                st.warning("Please enter both email and password.")
                return

            found_user = None
            for user in users:
                if user["email"].lower() == email.lower() and user["password"] == password:
                    found_user = user
                    break

            if found_user is None:
                st.error("Invalid email or password.")
                return

            st.session_state["logged_in"] = True
            st.session_state["user_id"] = found_user["user_id"]
            st.session_state["name"] = found_user["name"]
            st.session_state["role"] = found_user["role"]

            st.success("Login successful!")
            time.sleep(0.6)

            if found_user["role"] == "owner":
                go_to_page("owner_dashboard")
            else:
                go_to_page("employee_dashboard")

def render_register_page():
    show_page_header("Register New Account", "Create a new bakery owner or employee account.")

    left, center, right = st.columns([1, 2, 1])

    with center:
        name = st.text_input("Full Name", key="register_name_input")
        email = st.text_input("Email Address", key="register_email_input")
        password = st.text_input("Create Password", type="password", key="register_password_input")
        role = st.selectbox("Select Role", ["owner", "employee"], key="register_role_select")

        if st.button("Create Account", key="register_submit_btn", use_container_width=True, type="primary"):
            name = clean_text(name)
            email = clean_text(email)
            password = clean_text(password)

            if name == "" or email == "" or password == "":
                st.warning("Please fill in all fields.")
                return

            if not valid_email(email):
                st.error("Please enter a valid email address.")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters long.")
                return

            for user in users:
                if user["email"].lower() == email.lower():
                    st.error("That email is already registered.")
                    return

            users.append({
                "user_id": str(uuid.uuid4()),
                "name": name,
                "email": email,
                "password": password,
                "role": role
            })

            if save_users_data():
                st.success("Account created successfully!")
                time.sleep(0.6)
                go_to_page("login")
            else:
                st.error("There was a problem saving the account.")

def render_owner_dashboard():
    require_role(["owner"])
    show_page_header("Owner Dashboard", "View bakery inventory activity and important alerts.")

    low_items = get_low_stock_items()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", len(inventory))
    col2.metric("Low Stock Items", len(low_items))
    col3.metric("Low Stock Flags", len(flags))
    col4.metric("Inventory Value", f"${get_inventory_value():.2f}")

    st.markdown("### Inventory Overview")
    render_inventory_table()

    st.markdown("### Low Stock Summary")
    if len(low_items) == 0:
        st.success("No items are currently low on stock.")
    else:
        st.dataframe(low_stock_table_data(), use_container_width=True, hide_index=True)

def render_manage_inventory():
    require_role(["owner"])
    show_page_header("Manage Bakery Inventory", "Add, update, or delete bakery items.")

    tab1, tab2, tab3 = st.tabs(["Add Item", "Update Price", "Delete Item"])

    with tab1:
        st.markdown("### Add New Item")
        item_name = st.text_input("Item Name", key="add_item_name_input")
        unit_price = st.number_input("Unit Price", min_value=0.0, step=0.25, key="add_item_price_input")
        stock = st.number_input("Starting Stock", min_value=0, step=1, key="add_item_stock_input")

        if st.button("Add New Item", key="add_item_submit_btn", use_container_width=True, type="primary"):
            item_name = clean_text(item_name)

            if item_name == "":
                st.warning("Please enter an item name.")
                return

            for item in inventory:
                if item["name"].lower() == item_name.lower():
                    st.error("That item already exists.")
                    return

            inventory.append({
                "item_id": get_next_item_id(),
                "name": item_name,
                "unit_price": unit_price,
                "stock": stock
            })

            if save_inventory_data():
                st.success("New bakery item added successfully!")
                time.sleep(0.6)
                st.rerun()
            else:
                st.error("There was a problem saving inventory data.")

    with tab2:
        st.markdown("### Update Item Price")

        if len(inventory) == 0:
            show_empty_message("No items available.")
        else:
            selected_name = st.selectbox(
                "Choose Item to Update Price",
                options=get_item_names(),
                key="update_price_item_select"
            )

            selected_item = get_item_by_name(selected_name)

            new_price = st.number_input(
                "New Price",
                min_value=0.0,
                step=0.25,
                key="update_price_value_input"
            )

            if st.button("Update Price", key="update_price_submit_btn", use_container_width=True, type="primary"):
                if selected_item is None:
                    st.error("Selected item was not found.")
                    return

                selected_item["unit_price"] = new_price

                if save_inventory_data():
                    st.success("Price updated successfully!")
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error("There was a problem saving inventory data.")

    with tab3:
        st.markdown("### Delete Item")

        if len(inventory) == 0:
            show_empty_message("No items available.")
        else:
            selected_name = st.selectbox(
                "Choose Item to Delete",
                options=get_item_names(),
                key="delete_item_name_select"
            )

            delete_item = get_item_by_name(selected_name)

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this item.",
                key="delete_item_confirm_checkbox"
            )

            if st.button("Delete Item", key="delete_item_submit_btn", use_container_width=True, type="primary"):
                if delete_item is None:
                    st.error("Selected item was not found.")
                    return

                if not confirm_delete:
                    st.warning("Please confirm deletion before removing the item.")
                    return

                inventory.remove(delete_item)

                if save_inventory_data():
                    st.success("Item deleted successfully!")
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error("There was a problem saving inventory data.")

def render_restock_inventory():
    require_role(["owner"])
    show_page_header("Restock Bakery Inventory", "Increase stock levels for existing items.")

    if len(inventory) == 0:
        show_empty_message("No bakery items available.")
        return

    selected_name = st.selectbox(
        "Choose Item to Restock",
        options=get_item_names(),
        key="restock_item_name_select"
    )

    selected_item = get_item_by_name(selected_name)

    restock_amount = st.number_input(
        "Restock Amount",
        min_value=1,
        step=1,
        key="restock_amount_value_input"
    )

    if st.button("Restock Item", key="restock_submit_btn", use_container_width=True, type="primary"):
        if selected_item is None:
            st.error("Selected item was not found.")
            return

        selected_item["stock"] += restock_amount

        if save_inventory_data():
            st.success(f"{selected_item['name']} was restocked successfully!")
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("There was a problem saving inventory data.")

def render_sales_records():
    require_role(["owner"])
    show_page_header("Sales Records", "Review all recorded sales transactions.")
    render_sales_table()

def render_low_stock_alerts():
    require_role(["owner"])
    show_page_header("Low Stock Alerts", "Review flags submitted by employees.")
    render_flags_table()

def render_employee_dashboard():
    require_role(["employee"])
    show_page_header("Employee Dashboard", "View the bakery catalog and current inventory status.")

    low_items = get_low_stock_items()

    col1, col2, col3 = st.columns(3)
    col1.metric("Available Items", len(inventory))
    col2.metric("Items Running Low", len(low_items))
    col3.metric("Sales Logged", len(sales))

    st.markdown("### Current Catalog")
    render_inventory_table()

def render_view_catalog():
    require_role(["employee"])
    show_page_header("Bakery Catalog", "A full view of all current bakery items.")
    render_inventory_table()

def render_log_sales():
    require_role(["employee"])
    show_page_header("Log Daily Sale", "Record completed sales and automatically update inventory.")

    if len(inventory) == 0:
        show_empty_message("No inventory items available.")
        return

    selected_name = st.selectbox(
        "Select Item Sold",
        options=get_item_names(),
        key="log_sales_item_name_select"
    )

    selected_item = get_item_by_name(selected_name)

    quantity = st.number_input(
        "Quantity Sold",
        min_value=1,
        step=1,
        key="log_sales_quantity_input"
    )

    if st.button("Record Sale", key="log_sales_submit_btn", use_container_width=True, type="primary"):
        if selected_item is None:
            st.error("Selected item was not found.")
            return

        if selected_item["stock"] == 0:
            st.error("This item is out of stock.")
            return

        if quantity > selected_item["stock"]:
            st.error("Not enough stock available.")
            return

        selected_item["stock"] -= quantity
        total = quantity * selected_item["unit_price"]

        sales.append({
            "sale_id": str(uuid.uuid4()),
            "item_id": selected_item["item_id"],
            "employee_id": st.session_state["user_id"],
            "quantity": quantity,
            "total": total,
            "sale_date": str(datetime.now().date())
        })

        inventory_saved = save_inventory_data()
        sales_saved = save_sales_data()

        if inventory_saved and sales_saved:
            st.success("Sale recorded successfully!")
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("There was a problem saving the sale.")

def render_flag_low_stock():
    require_role(["employee"])
    show_page_header("Flag Low Stock Item", "Send a low stock message to the owner.")

    if len(inventory) == 0:
        show_empty_message("No inventory items available.")
        return

    selected_name = st.selectbox(
        "Select Item to Flag",
        options=get_item_names(),
        key="flag_item_name_select"
    )

    selected_item = get_item_by_name(selected_name)

    message = st.text_area(
        "Message",
        placeholder="Explain why this item needs attention.",
        key="flag_message_textarea"
    )

    if st.button("Submit Low Stock Flag", key="flag_submit_btn", use_container_width=True, type="primary"):
        message = clean_text(message)

        if selected_item is None:
            st.error("Selected item was not found.")
            return

        if message == "":
            st.warning("Please enter a message before submitting.")
            return

        flags.append({
            "flag_id": str(uuid.uuid4()),
            "item_id": selected_item["item_id"],
            "employee_id": st.session_state["user_id"],
            "message": message,
            "date_flagged": str(datetime.now().date())
        })

        if save_flags_data():
            st.success("Low stock flag submitted successfully!")
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("There was a problem saving the flag.")

def render_chatbot():
    require_role(["employee"])
    show_page_header("Bakery Inventory Chatbot", "Ask simple questions about inventory, sales, and alerts.")

    top_left, top_right = st.columns([3, 1])

    with top_left:
        st.caption("Try asking: What items are low on stock?")

    with top_right:
        if st.button("Clear Messages", key="chat_clear_messages_btn", use_container_width=True):
            st.session_state["messages"] = [
                {
                    "role": "assistant",
                    "content": "Hi! I can help with bakery inventory questions."
                }
            ]
            st.rerun()

    with st.container(border=True):
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    user_input = st.chat_input("Ask a question...", key="chat_input_main")

    if user_input:
        cleaned_question = clean_text(user_input)

        st.session_state["messages"].append({
            "role": "user",
            "content": cleaned_question
        })

        question = cleaned_question.lower()

        if "low stock" in question:
            low_items = [item["name"] for item in inventory if item["stock"] < 5]
            if len(low_items) > 0:
                ai_response = "These items are low on stock: " + ", ".join(low_items)
            else:
                ai_response = "No bakery items are currently low on stock."

        elif "how many items" in question or "how many products" in question:
            ai_response = f"There are currently {len(inventory)} bakery items in the inventory."

        elif "how many sales" in question:
            ai_response = f"There are currently {len(sales)} sales records in the system."

        elif "how many flags" in question or "alerts" in question:
            ai_response = f"There are currently {len(flags)} low stock alerts."

        elif "inventory value" in question:
            ai_response = f"The current inventory value is ${get_inventory_value():.2f}."

        elif "help" in question:
            ai_response = (
                "You can ask about low stock items, total inventory items, "
                "sales records, low stock alerts, and inventory value."
            )

        else:
            ai_response = "I can answer simple bakery inventory questions right now."

        st.session_state["messages"].append({
            "role": "assistant",
            "content": ai_response
        })

        time.sleep(0.4)
        st.rerun()


def render_current_page():
    page = st.session_state["page"]

    if page == "login":
        render_login_page()
    elif page == "register":
        render_register_page()
    elif page == "owner_dashboard":
        render_owner_dashboard()
    elif page == "manage_inventory":
        render_manage_inventory()
    elif page == "restock_inventory":
        render_restock_inventory()
    elif page == "sales_records":
        render_sales_records()
    elif page == "low_stock_alerts":
        render_low_stock_alerts()
    elif page == "employee_dashboard":
        render_employee_dashboard()
    elif page == "view_catalog":
        render_view_catalog()
    elif page == "log_sales":
        render_log_sales()
    elif page == "flag_low_stock":
        render_flag_low_stock()
    elif page == "chatbot":
        render_chatbot()
    else:
        st.error("Page not found.")
        go_to_page("login")

render_current_page()