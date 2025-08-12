# API Views for Listings and Bookings

## 📌 Overview
This project implements API endpoints for managing **Listings** and **Bookings** in the `alx_travel_app_0x01` application.  
The API is built with Django REST Framework using **ModelViewSet** to provide full CRUD capabilities and is documented with **Swagger**.

---

## 🛠 Implementation Summary

### ViewSets
- Created `ListingViewSet` and `BookingViewSet` in `listings/views.py`.
- Both viewsets inherit from **DRF’s `ModelViewSet`** to automatically handle:
  - Listing all records (`GET`)
  - Retrieving a single record (`GET`)
  - Creating new records (`POST`)
  - Updating records (`PUT` / `PATCH`)
  - Deleting records (`DELETE`)

---

### URL Configuration
- Configured a **DRF router** in `listings/urls.py` to register:
  - `/api/listings/`
  - `/api/bookings/`
- The router automatically maps each endpoint to its respective viewset.

---

### API Documentation
- Integrated **Swagger UI** for automatic API documentation.
- Endpoints are accessible and documented at `/swagger/`.
- Each API route includes its parameters, request body schema, and example responses.

---

### Testing
- Verified all CRUD endpoints using **Postman**.
- Tested with valid and invalid data to ensure proper validation and error handling.
- Confirmed correct HTTP status codes for each operation.

---

