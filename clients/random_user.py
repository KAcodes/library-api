from requests import get

USER_URL = "https://randomuser.me/api/"


def retrieve_api_users(user_count: str):
    response = get(USER_URL, params={
            "results": user_count,
            "nat": "gb",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])


def transform_users(users: list) -> list[tuple[str, str, str, str, str | None]]:

    cleaned_users = []

    for user in users:
        login = user.get("login", {})
        name = user.get("name", {})

        user_id = login.get("uuid")
        first_name = name.get("first")
        last_name = name.get("last")
        email = user.get("email")
        phone = user.get("phone")

        if not all([
            user_id,
            first_name,
            last_name,
            email,
        ]):
            continue

        cleaned_users.append(
            (
                user_id,
                first_name,
                last_name,
                email,
                phone,
            )
        )
    return cleaned_users