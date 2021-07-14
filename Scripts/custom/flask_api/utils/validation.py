from flask import request


def get_jwt(jwt_name='token', decoded=False, algorithms=['HS512']):
    import jwt

    token = None
    try:
        if request.method in ['POST', 'PATCH']:
            # Check for json
            token = request.json.get(jwt_name, None)
        elif request.method in ['GET']:
            # Check the request args
            token = request.args.get(jwt_name, None)
    except Exception:
        return None

    if not decoded:
        return token

    try:
        return jwt.decode(
            token, verify=False, algorithms=algorithms
        )
    except Exception:
        return None
