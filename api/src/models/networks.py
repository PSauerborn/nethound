
from typing import Optional

from pydantic import BaseModel


class NewNetworkRequest(BaseModel):
    """Data class containing fields used to
    store new network requests"""

    network_name: str
    network_description: Optional[str]