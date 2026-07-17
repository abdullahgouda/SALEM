from fastapi import FastAPI

app = FastAPI(
    title="SALEM AI API"
)

# Import Routers
from Duplicate_Incident_API.main import app as duplicate_app
from Citizen_Trust_API.main import app as trust_app
from Image_Authenticity_API.main import app as image_app
from Incident_Severity_API.main import app as severity_app
from Priority_Allocation_API.main import app as priority_app
from Road_Damage_API.main import app as road_app

app.mount("/duplicate", duplicate_app)
app.mount("/trust", trust_app)
app.mount("/image", image_app)
app.mount("/severity", severity_app)
app.mount("/priority", priority_app)
app.mount("/road", road_app)