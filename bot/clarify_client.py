import httpx
import logging

logger = logging.getLogger(__name__)


class ClarifyClient:
    def __init__(self, workspace_slug: str, api_key: str):
        self.base_url = f"https://api.clarify.ai/v1/workspaces/{workspace_slug}"
        self.headers = {
            "Authorization": f"api-key {api_key}",
            "Content-Type": "application/json",
        }
        self.enabled = bool(workspace_slug and api_key)

    def _build_person_payload(self, name: str, email: str, **extra) -> dict:
        attrs = {"name": name, "email_addresses": [email]}
        if "phone" in extra and extra["phone"]:
            attrs["phone_numbers"] = [extra["phone"]]
        if "title" in extra and extra["title"]:
            attrs["title"] = extra["title"]
        return {"data": {"type": "person", "attributes": attrs}}

    def _build_company_payload(self, name: str, domain: str, **extra) -> dict:
        attrs = {"name": name, "domains": [domain]}
        return {"data": {"type": "company", "attributes": attrs}}

    async def create_person(self, name: str, email: str, **extra) -> dict | None:
        """Create or upsert a person in Clarify. Returns response or None on failure."""
        if not self.enabled:
            logger.warning("Clarify not configured, skipping person creation")
            return None
        payload = self._build_person_payload(name, email, **extra)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/objects/person/records",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify create_person failed: {resp.status_code} {resp.text}")
                return None
            return resp.json()

    async def create_company(self, name: str, domain: str) -> dict | None:
        """Create or upsert a company in Clarify. Returns response or None on failure."""
        if not self.enabled:
            logger.warning("Clarify not configured, skipping company creation")
            return None
        payload = self._build_company_payload(name, domain)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/objects/company/records",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify create_company failed: {resp.status_code} {resp.text}")
                return None
            return resp.json()

    async def link_person_to_company(self, person_id: str, company_id: str) -> bool:
        """Link a person to a company. Returns True on success."""
        if not self.enabled:
            return False
        payload = {"data": [{"id": company_id, "type": "company"}]}
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.base_url}/objects/person/records/{person_id}/relationships/company",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify link failed: {resp.status_code} {resp.text}")
                return False
            return True
