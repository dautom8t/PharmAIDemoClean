"""
Bladnir Demo Hub

Central landing page that makes the project feel like a platform.

Provides:
- /demo → one link that launches packs
- Dropdown for Industry Pack
- Redirect to scenario UIs (Kroger Retail currently)

Future packs plug in easily.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["demo"])


@router.get("/demo", response_class=HTMLResponse)
def demo_home():
    return """
<!doctype html>
<html>
<head>
  <title>Bladnir Tech Demo Hub</title>
  <style>
    body { font-family: Arial; padding: 40px; }
    h1 { margin-bottom: 5px; }
    select, button {
      width: 320px;
      padding: 12px;
      margin-top: 12px;
      font-size: 14px;
    }
    button {
      background: black;
      color: white;
      border: none;
      cursor: pointer;
      border-radius: 8px;
    }
    .card {
      border: 1px solid #ddd;
      border-radius: 12px;
      padding: 20px;
      max-width: 420px;
    }
    .muted { color: #666; font-size: 13px; }
  </style>
</head>

<body>
  <h1>Bladnir Tech</h1>
  <p class="muted">Cross-System Workflow Orchestration Middleware</p>

  <div class="card">
    <h2>Scenario Demo Hub</h2>

    <p>Select an industry pack to launch a workflow simulation.</p>

    <select id="pack">
      <option value="">Choose Industry Pack…</option>
      <option value="/kroger">Kroger Retail Pharmacy Pack</option>
    </select>

    <button onclick="launchPack()">Launch Demo</button>
  </div>

  <script>
    function launchPack(){
      const pack = document.getElementById("pack").value;
      if(!pack){
        alert("Select a pack first.");
        return;
      }
      window.location.href = pack;
    }
  </script>

</body>
</html>
    """
