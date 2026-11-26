from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional
from src.seguridad.password_hasher import SecurityValidator
from src.seguridad.input_sanitizer import InputSanitizer

@dataclass
class Destination:
    name: str
    country: str
    base_cost: float
    active: bool = True
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del destino es obligatorio.")
        if not self.country or not self.country.strip():
            raise ValueError("El país del destino es obligatorio.")
        if self.base_cost < 0:
            raise ValueError("El costo base no puede ser negativo.")

        self.name = self.name.strip()
        self.country = self.country.strip()

    def retire(self) -> None:
        if not self.active:
            raise ValueError("El destino ya se encuentra retirado.")
        self.active = False


@dataclass
class ItineraryStop:
    destination: Destination
    visit_order: int
    id: Optional[int] = None

    def change_order(self, new_order: int) -> None:
        if new_order < 1:
            raise ValueError("El orden de visita debe ser mayor o igual a 1.")
        self.visit_order = new_order


@dataclass
class TravelPackage:
    name: str
    stops: List[ItineraryStop] = field(default_factory=list)
    active: bool = True
    id: Optional[int] = None

    def add_stop(self, destination: Destination, visit_order: int) -> None:
        if not destination.active:
            raise ValueError(
                f"El destino '{destination.name}' está retirado y no puede agregarse."
            )
        if visit_order < 1:
            raise ValueError("El orden de visita debe ser mayor o igual a 1.")
        if any(s.visit_order == visit_order for s in self.stops):
            raise ValueError(f"Ya existe una etapa con el orden {visit_order}.")
        if any(s.destination.id == destination.id for s in self.stops):
            raise ValueError(
                f"El destino '{destination.name}' ya está incluido en el itinerario."
            )

        self.stops.append(ItineraryStop(destination=destination, visit_order=visit_order))
        self.stops.sort(key=lambda s: s.visit_order)

    def validate_itinerary(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del paquete turístico es obligatorio.")
        if len(self.stops) < 2:
            raise ValueError("Un paquete turístico debe combinar al menos 2 destinos.")
        self.name = self.name.strip()

    def calculate_base_cost(self) -> float:
        return sum(stop.destination.base_cost for stop in self.stops)


@dataclass
class PackageDeparture:
    package_id: int
    start_date: date
    end_date: date
    price: float
    capacity: int
    booked_seats: int = 0
    package_name: str = ""
    id: Optional[int] = None

    def validate(self) -> None:
        if self.end_date < self.start_date:
            raise ValueError(
                "La fecha de término no puede ser anterior a la fecha de inicio."
            )
        if self.price < 0:
            raise ValueError("El precio de la salida no puede ser negativo.")
        if self.capacity <= 0:
            raise ValueError("La cantidad de cupos debe ser mayor a cero.")

    def available_seats(self) -> int:
        return max(0, self.capacity - self.booked_seats)


@dataclass
class UserAccount:
    email: str
    password_hash: str
    role: str = "CLIENT"
    id: Optional[int] = None

    @classmethod
    def register(
        cls, email: str, plain_password: str, role: str = "CLIENT"
    ) -> "UserAccount":
        valid_email = SecurityValidator.validate_email(email)
        SecurityValidator.validate_password_strength(plain_password)
        if role not in ("ADMIN", "CLIENT"):
            raise ValueError("Rol de usuario inválido.")
        hashed = SecurityValidator.hash_password(plain_password)
        return cls(email=valid_email, password_hash=hashed, role=role)

    def validate_credentials(self) -> bool:
        SecurityValidator.validate_email(self.email)
        return bool(self.password_hash)

    def authenticate(self, plain_password: str) -> bool:
        return SecurityValidator.verify_password(plain_password, self.password_hash)


@dataclass
class StageProgress:
    stop_id: int
    stop_order: int = 0
    destination_name: str = ""
    status: str = "PENDING"
    updated_at: datetime = field(default_factory=datetime.now)
    updated_by_email: str = ""
    id: Optional[int] = None

    def mark_status(self, new_status: str, admin: UserAccount) -> None:
        if admin.role != "ADMIN":
            raise ValueError("Solo un administrador puede actualizar etapas del viaje.")
        if new_status not in ("PENDING", "IN_PROGRESS", "COMPLETED"):
            raise ValueError("Estado de etapa inválido.")
        self.status = new_status
        self.updated_at = datetime.now()


@dataclass
class Passenger:
    full_name: str
    document_id: str
    stages: List[StageProgress] = field(default_factory=list)
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise ValueError("El nombre completo del pasajero es obligatorio.")
        if not self.document_id or not self.document_id.strip():
            raise ValueError("El documento de identidad del pasajero es obligatorio.")
        self.full_name = self.full_name.strip()
        self.document_id = self.document_id.strip().upper()

    def get_trip_status(self) -> str:
        if not self.stages or all(s.status == "PENDING" for s in self.stages):
            return "Pendiente"
        if all(s.status == "COMPLETED" for s in self.stages):
            return "Finalizado"
        return "Viajando"


@dataclass
class Reservation:
    user_id: int
    departure_id: int
    unit_price: float
    passengers: List[Passenger] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    total_price: float = 0.0
    status: str = "CONFIRMED"
    package_name: str = ""
    start_date: str = ""
    end_date: str = ""
    user_email: str = ""
    id: Optional[int] = None

    def calculate_total(self) -> float:
        if not self.passengers:
            raise ValueError("La reserva debe incluir al menos un pasajero.")
        self.total_price = round(self.unit_price * len(self.passengers), 2)
        return self.total_price

    def confirm(self) -> None:
        self.calculate_total()
        self.status = "CONFIRMED"

    def cancel(self) -> None:
        if self.status == "CANCELLED":
            raise ValueError("La reserva ya se encuentra cancelada.")
        self.status = "CANCELLED"