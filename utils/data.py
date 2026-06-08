class ApiData:
    base_url = "https://qa-scooter.praktikum-services.ru"

    # endpoints
    courier_endpoint = "/api/v1/courier"
    courier_login_endpoint = "/api/v1/courier/login"
    orders_endpoint = "/api/v1/orders"
    cancel_order = "/api/v1/orders/cancel"

    # messages
    ok_message = {"ok": True}
    login_already_used = "Этот логин уже используется. Попробуйте другой."
    no_courier_with_that_id = "Курьера с таким id нет."
    not_enough_data_to_create_account = (
        "Недостаточно данных для создания учетной записи"
    )
    not_enough_data_to_login = "Недостаточно данных для входа"
    user_not_found = "Учетная запись не найдена"
