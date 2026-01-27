from fastapi import Header, HTTPException, Depends
from dataclasses import dataclass

@dataclass
class UserContext:
    api_key: str
    role: str


ENTERPRISE_KEYS = {
    "demo-admin-key": "admin",
    "demo-operator-key": "operator",
    "demo-auditor-key": "auditor",
}


def require_auth(x_api_key: str = Header(...)) -> UserContext:
    if x_api_key not in ENTERPRISE_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    role = ENTERPRISE_KEYS[x_api_key]
    return UserContext(api_key=x_api_key, role=role)


def require_role(required: str):
    def checker(user: UserContext = Depends(require_auth)):
        if user.role != required:
            raise HTTPException(
                status_code=403,
                detail=f"Requires role: {required}"
            )
        return user
    return checker
