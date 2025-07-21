from backend.app.db.db_client import get_client, close_client, create_user, get_user, add_prescription, update_user, delete_user
import datetime
client = get_client()
try:
    # 1. Create user
    user_id = create_user(client, "Test User", dob=datetime.datetime(1990, 1, 1), email="test@example.com")
    print("Created user:", user_id)

    # 2. Get user
    user = get_user(client, user_id)
    print("Fetched user:", user)


    # 3. Add three prescriptions
    presc_id1 = add_prescription(client, user_id, medication="Aspirin", dosage="2 pills", instructions="After meal")
    print("Added prescription 1:", presc_id1)
    presc_id2 = add_prescription(client, user_id, medication="Ibuprofen", dosage="1 pill", instructions="Before bed")
    print("Added prescription 2:", presc_id2)
    presc_id3 = add_prescription(client, user_id, medication="Vitamin D", dosage="1 tablet", instructions="Morning")
    print("Added prescription 3:", presc_id3)

    # 4. Query prescriptions (optional)
    prescriptions = list(client.PillReminder.prescriptions.find({"user_id": user_id}))
    print(f"Prescriptions for user {user_id}:")
    for p in prescriptions:
        print(p)

    # 5. Update user
    updated = update_user(client, user_id, name="Updated Name")
    print("User updated:", updated)

    # 6. Delete user
    # deleted = delete_user(client, user_id)
    # print("User deleted:", deleted)
finally:
    close_client(client)