from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember]
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_space_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_commander_or_captain = any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        )
        if not has_commander_or_captain:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )

        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5
                )
            required_count = len(self.crew) / 2
            if experienced_count < required_count:
                raise ValueError(
                    "Long missions (> 365 days) need 50% "
                    "experienced crew (5+ years)"
                    )

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="M001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=42,
                    specialization="Mission Command",
                    years_experience=15,
                    is_active=True
                ),
                CrewMember(
                    member_id="M002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=8,
                    is_active=True
                ),
                CrewMember(
                    member_id="M003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True
                )
            ]
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank}) - {member.specialization}")
    except ValidationError as e:
        print(e)

    print("=========================================")
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="M999_TEST",
            mission_name="Failed Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=30,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Bob Rookie",
                    rank=Rank.CADET,
                    age=20,
                    specialization="Cleaning",
                    years_experience=0,
                    is_active=True
                )
            ]
        )
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
