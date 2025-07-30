### 1. `users` collection
```json
{
  "_id": ObjectId("..."),
  "username": "nguyentrinh",
  "email": "nguyen@example.com",
  "notifications_enabled": true,
}
```
### 2. `medications` collection
```json
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),   // reference to users._id

  "medication_name": "Amoxicillin",
  "dosage": "500 mg",
  "form": "tablet",
  "route": "oral",
  "instructions": "Take with food",

  "frequency": "every 8 hours",
  "times_per_day": 3,
  "reminder_times": ["08:00", "16:00", "00:00"],

  "start_date": ISODate("2025-07-30T00:00:00Z"),
  "end_date": ISODate("2025-08-06T00:00:00Z"),

  "image_url": "https://example.com/prescription.jpg",
  "parsed_by_ocr": true,
  "raw_ocr_text": "Take 1 tablet of Amoxicillin 500mg every 8 hours for 7 days",
  
  "created_at": ISODate("2025-07-30T10:00:00Z")
}
```

### 3. `logs` collection
```json
{
  "_id": ObjectId("..."),
  "medication_id": ObjectId("..."),  // reference to medications._id
  "user_id": ObjectId("..."),        // optional for fast lookup

  "taken_time": ISODate("2025-07-30T08:00:00Z"),
  "scheduled_time": ISODate("2025-07-30T08:00:00Z"), // dispensed time
  "taken": true,
}
```

