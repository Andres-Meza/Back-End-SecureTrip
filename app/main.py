from fastapi import FastAPI
from app.api import AuditPayments, Cities, Collaborators, Countries, Languages, Logins, Payments, TravelPlannings, Promotions, Reviews, Services, TransportServices, Clients, ClientPromotions, ServicePlannings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Registrar los routers
app.include_router(Cities.router, prefix="/cities", tags=["cities"])
app.include_router(Collaborators.router, prefix="/collaborators", tags=["collaborators"])
app.include_router(Countries.router, prefix="/countries", tags=["countries"])
app.include_router(Languages.router, prefix="/languages", tags=["languages"])
app.include_router(Payments.router, prefix="/payments", tags=["payments"])
app.include_router(TravelPlannings.router, prefix="/travelplannings", tags=["travelplannings"])
app.include_router(Promotions.router, prefix="/promotions", tags=["promotions"])
app.include_router(Reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(Services.router, prefix="/services", tags=["services"])
app.include_router(TransportServices.router, prefix="/transportservices", tags=["transportservices"])
app.include_router(Clients.router, prefix="/clients", tags=["clients"])
app.include_router(ClientPromotions.router, prefix="/clientpromotions", tags=["clientpromotions"])
app.include_router(ServicePlannings.router, prefix="/serviceplannings", tags=["serviceplannings"])
app.include_router(Logins.router, prefix="/logins", tags=["logins"])
app.include_router(AuditPayments.router, prefix="/auditpayments", tags=["auditpayments"])


# Configuración de CORS
app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

