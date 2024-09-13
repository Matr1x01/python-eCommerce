# Django Dockerized Project

This project is a Django application that runs in a Docker container using Docker Compose. It uses SQLite as the database and runs on port 8080.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create a `.env` File**

   Create a `.env` file in the root of the project and add the following environment variables:

   ```bash
   SECRET_KEY=<your_secret_key>
   ```

3. **Build and Run the Containers**

   Build and run the containers using Docker Compose:

   ```bash
   docker-compose up --build
   ```

4. **Create a Superuser**

   To create a Django superuser, run the following command:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the Application**

   The Django application will be available at:

   ```
   http://localhost:8080
   ```

## Project Structure

- **Dockerfile**: Defines the environment setup for the Django app.
- **docker-compose.yml**: Manages the `web` and `db` services.
- **requirements.txt**: Python dependencies.
- **db.sqlite3**: SQLite database file, mounted as a volume to persist data.

## Docker Compose Services

- **web**: Django application container, accessible at `localhost:8080`.
- **db**: SQLite container, data persisted in the `db.sqlite3` file.

## Running Migrations

To apply Django database migrations:

```bash
docker-compose exec web python manage.py migrate
```

## Debug Mode

By default, the project is in debug mode. To disable debug mode, update the `.env` file and rebuild the container:

```bash
DEBUG=0
```

## Stopping the Containers

To stop and remove the containers, run:

```bash
docker-compose down
```
# Django Ecommerce API Documentation

## Base URL: `http://20.189.115.60:80`

## Authentication
Bearer Token: `Authorization: Bearer <your_token>`

## Global Headers
- `Accept: application/json`
- `X-Requested-With: XMLHttpRequest`

## Endpoints

### Products

1. **Product List**
   - `GET /api/products?per_page=10&page=1`
   - Response:
     ```json
     {
       "count": 100,
       "next": "http://20.189.115.60:80/api/products?page=2",
       "previous": null,
       "results": [
         {
           "id": 1,
           "name": "iPhone 13",
           "slug": "iphone-13",
           "price": 999.99,
           "image": "http://example.com/iphone13.jpg"
         },
         // ... more products
       ]
     }
     ```

2. **Product Search**
   - `GET /api/products-search/?query=iphone`
   - Response: Similar to Product List

3. **Product Details**
   - `GET /api/products/:slug`
   - Response:
     ```json
     {
       "id": 1,
       "name": "iPhone 13",
       "slug": "iphone-13",
       "description": "Latest iPhone model",
       "price": 999.99,
       "image": "http://example.com/iphone13.jpg",
       "brand": "Apple",
       "category": "Smartphones"
     }
     ```

4. **Brand List**
   - `GET /api/brands/`
   - Response:
     ```json
     [
       {
         "id": 1,
         "name": "Apple",
         "slug": "apple"
       },
       // ... more brands
     ]
     ```

5. **Category List**
   - `GET /api/category/`
   - Response: Similar to Brand List

### Customer

1. **Register**
   - `POST /api/register`
   - Body:
     ```json
     {
       "phone": "01765393016",
       "password": "12345678",
       "name": "Mozharul Haq",
       "confirm_password": "12345678"
     }
     ```
   - Response:
     ```json
     {
       "token": "e6cbd8b3b649cf8c17dff12f2f7cd04119db0f98",
       "user": {
         "id": 1,
         "name": "Mozharul Haq",
         "phone": "01765393016"
       }
     }
     ```

2. **Login**
   - `POST /api/login`
   - Body:
     ```json
     {
       "phone": "01765393016",
       "password": "12345678"
     }
     ```
   - Response: Similar to Register response

3. **Customer Details**
   - `GET /api/profile`
   - Response:
     ```json
     {
       "id": 1,
       "name": "Mozharul Haq",
       "phone": "01765393016",
       "email": "mozharul@example.com",
       "gender": "M"
     }
     ```

4. **Customer Update**
   - `PUT /api/profile/update`
   - Body:
     ```json
     {
       "gender": "M"
     }
     ```
   - Response: Updated customer details

### Address

1. **Address List**
   - `GET /api/addresses`
   - Response:
     ```json
     [
       {
         "id": "ad94c51d-4c90-4019-b3cb-14396d96e00e",
         "address": "123 Main Street",
         "area": "Downtown",
         "city": "Metropolis",
         "state": "StateName",
         "country": "CountryName",
         "postal_code": "12345"
       },
       // ... more addresses
     ]
     ```

2. **Create Address**
   - `POST /api/addresses/`
   - Body:
     ```json
     {
       "address": "123 Main Street",
       "area": "Downtown",
       "city": "Metropolis",
       "state": "StateName",
       "country": "CountryName",
       "postal_code": "12345"
     }
     ```
   - Response: Created address object

3. **Update Address**
   - `PUT /api/addresses/:slug/`
   - Body: Same as Create Address
   - Response: Updated address object

### Cart and Wishlist

1. **Get Cart**
   - `GET /api/cart/`
   - Response:
     ```json
     {
       "items": [
         {
           "id": 1,
           "product": "iPhone 13",
           "quantity": 2,
           "price": 1999.98
         }
       ],
       "total": 1999.98
     }
     ```

2. **Add to Cart**
   - `POST /api/cart/`
   - Body:
     ```json
     {
       "product": "iphone-13",
       "quantity": 1
     }
     ```
   - Response: Updated cart object

3. **Remove from Cart**
   - `DELETE /api/cart/`
   - Body:
     ```json
     {
       "product": "iphone-13"
     }
     ```
   - Response: Updated cart object

4. **Get/Add/Remove Wishlist**
   - Similar to Cart operations, use `/api/wishlist/` endpoint

### Order

1. **Get Orders**
   - `GET /api/orders/`
   - Response:
     ```json
     [
       {
         "id": "2b1eccd2-729a-411a-a07b-fe3a18d1e86b",
         "status": "Pending",
         "total": 1999.98,
         "created_at": "2023-09-14T10:30:00Z"
       },
       // ... more orders
     ]
     ```

2. **Create Order**
   - `POST /api/orders/`
   - Body:
     ```json
     {
       "payment_method": "cash_on_delivery",
       "delivery_method": "home_delivery",
       "address": "2b954aaf-638c-47eb-9444-ef44a4175090"
     }
     ```
   - Response: Created order object

### Coupon

1. **Apply Coupon**
   - `POST /api/apply-coupon/`
   - Body:
     ```json
     {
       "code": "abc"
     }
     ```
   - Response:
     ```json
     {
       "message": "Coupon applied successfully",
       "discount": 10.00
     }
     ```
