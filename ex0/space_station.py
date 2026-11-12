from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.00)
    oxygen_level: float = Field(..., ge=0.0, le=100.00)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def print_space_station(station: SpaceStation) -> None:
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status_text = "Operational" if station.is_operational else "Offline"
    print(f"Status: {status_text}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="All systems nominal."
        )
        print("Valid station created:")
        print_space_station(valid_station)
    except ValidationError as e:
        print("Validation Error: ", e)
    except Exception as e:
        print("Unknown Error: ", e)

    print("========================================")
    print("Expected validation error:")

    try:
        invalid_station = SpaceStation(
            station_id="ISS999",
            name="Overloaded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now(),
        )
        print("Invalid station created:")
        print_space_station(invalid_station)
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
