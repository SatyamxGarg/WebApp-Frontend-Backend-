from fastapi import Request, HTTPException

ALLOWED_HOSTS = {"localhost", "127.0.0.1", "*"}

def get_base_url(request: Request) -> str:
    """
    Dependency to extract the base URL (protocol + host) from the request headers.
    Allows all hosts if '*' is in ALLOWED_HOSTS.
    """
    host = request.headers.get("host")
    if not host:
        raise HTTPException(status_code=400, detail="Host header is missing")

    # Check if all hosts are allowed
    if "*" not in ALLOWED_HOSTS and not any(allowed_host in host for allowed_host in ALLOWED_HOSTS):
        raise HTTPException(status_code=400, detail="Invalid host")

    # Extract protocol, defaulting to HTTP if not provided
    protocol = request.headers.get("x-forwarded-proto", "http")
    return f"{protocol}://{host}"
