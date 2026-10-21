

QUESTIONS = [
    {
        "id": "q1",
        "title": "Filter customers by city",
        "points": 4,
        "prompt": (
            "Find all customers who live in Boston. Display "
            "customer_id, customer_name, and city, ordered by "
            "customer_id in ascending order."
        ),
        "hint": (
            "SQL hint: Use WHERE to filter rows and ORDER BY to sort them.\n\n"
            "Expected result: Only Boston customers, with columns "
            "customer_id, customer_name, and city, sorted from the "
            "smallest customer_id to the largest."
        ),
        "solution": """
            SELECT customer_id, customer_name, city
            FROM public.customers
            WHERE city = 'Boston'
            ORDER BY customer_id ASC
        """,
    },
    {
        "id": "q2",
        "title": "Sort products by price",
        "points": 4,
        "prompt": (
            "Display product_name and price for all products, from "
            "most expensive to least expensive. If prices tie, sort "
            "by product_name alphabetically."
        ),
        "hint": (
            "SQL hint: ORDER BY can sort by more than one column. "
            "Use descending order for price and ascending order "
            "for product_name.\n\n"
            "Expected result: All five products, with the highest "
            "price first and product names alphabetically when prices tie."
        ),
        "solution": """
            SELECT product_name, price
            FROM public.products
            ORDER BY price DESC, product_name ASC
        """,
    },
    {
        "id": "q3",
        "title": "Total quantity by product",
        "points": 4,
        "prompt": (
            "For each product_id in the orders table, calculate "
            "the total quantity ordered. Display product_id and "
            "a calculated column named total_quantity. Sort by "
            "product_id in ascending order."
        ),
        "hint": (
            "SQL hint: Use GROUP BY to combine rows with the same "
            "product_id, and SUM to add their quantities.\n\n"
            "Expected result: One row per product_id appearing in "
            "orders, with its total quantity across all orders, "
            "sorted by product_id."
        ),
        "solution": """
            SELECT product_id, SUM(quantity) AS total_quantity
            FROM public.orders
            GROUP BY product_id
            ORDER BY product_id ASC
        """,
    },
    {
        "id": "q4",
        "title": "Join customers and orders",
        "points": 4,
        "prompt": (
            "Show each customer's name and the order ID for every "
            "order belonging to that customer. Name the columns "
            "customer_name and order_id. Sort by order_id ascending."
        ),
        "hint": (
            "SQL hint: Join customers and orders using their shared "
            "customer_id column.\n\n"
            "Expected result: One row per order, showing the "
            "customer who placed it and its order ID, in ascending "
            "order_id order."
        ),
        "solution": """
            SELECT c.customer_name, o.order_id
            FROM public.customers AS c
            JOIN public.orders AS o
                ON c.customer_id = o.customer_id
            ORDER BY o.order_id ASC
        """,
    },
    {
        "id": "q5",
        "title": "Calculate order value",
        "points": 4,
        "prompt": (
            "For every order, display order_id and its total value, "
            "calculated by multiplying the product price by quantity. "
            "Name the calculated column order_value. Sort by order_id "
            "in ascending order."
        ),
        "hint": (
            "SQL hint: Join orders with products using product_id. "
            "Multiply the price by the quantity for each order.\n\n"
            "Expected result: One row per order, with order_id and "
            "order_value, sorted by order_id from smallest to largest."
        ),
        "solution": """
            SELECT
                o.order_id,
                p.price * o.quantity AS order_value
            FROM public.orders AS o
            JOIN public.products AS p
                ON o.product_id = p.product_id
            ORDER BY o.order_id ASC
        """,
    },
]
