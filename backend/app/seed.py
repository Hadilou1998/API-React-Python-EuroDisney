from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Attraction, AttractionStatus, Ticket, Employee, Reservation, ReservationStatus
from app.core.security import get_password_hash

# create all tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()

    # Delete all data exists
    db.query(Ticket).delete()
    db.query(Reservation).delete()
    db.query(Employee).delete()
    db.query(Attraction).delete()
    db.query(User).delete()
    db.commit()
    
    # -----------------------------
    # seed users
    # -----------------------------
    users = [
        # Admin
        User(name="admin", email="admin@disney.com", password=get_password_hash("admin123"), role="admin"),

        # Employees
        User(name="Mickey Mouse", email="mickey@disney.com", password=get_password_hash("employee123"), role="employee"),
        User(name="Minnie Mouse", email="minnie@disney.com", password=get_password_hash("employee123"), role="employee"),
        User(name="Donald Duck", email="donald@disney.com", password=get_password_hash("employee123"), role="employee"),
        User(name="Pluto", email="pluto@disney.com", password=get_password_hash("employee123"), role="employee"),
        User(name="Goofy", email="goofy@disney.com", password=get_password_hash("employee123"), role="employee"),

        # Users
        User(name="Hadil", email="hadil@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="John", email="john@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Sarah", email="sarah@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Tom", email="tom@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Alice", email="alice@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Bob", email="bob@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Charlie", email="charlie@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="David", email="david@disney.com", password=get_password_hash("user123"), role="user"), 
        User(name="Eve", email="eve@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Frank", email="frank@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Grace", email="grace@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Henry", email="henry@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Isabelle", email="isabelle@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Jessica", email="jessica@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Karen", email="karen@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Lisa", email="lisa@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Maggie", email="maggie@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Nancy", email="nancy@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Oscar", email="oscar@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Peter", email="peter@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Quincy", email="quincy@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Rachel", email="rachel@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Steve", email="steve@disney.com", password=get_password_hash("user123"), role="user"),
    ]
    db.add_all(users)
    db.commit()

    # Retrieve reel IDs
    user_dict = {u.name: u.id for u in db.query(User).all()}
    user_ids = [u.id for u in db.query(User).filter(User.role == "user").all()]
    employee_ids = [u.id for u in db.query(User).filter(User.role == "employee").all()]

    # -----------------------------
    # seed attractions
    # -----------------------------

    attractions = [
        Attraction(name="Space Mountain", description="A beautiful mountain with a lot of space for people to explore", capacity=20, status=AttractionStatus.open),
        Attraction(name="Pirates of the Caribbean", description="A fun ride with pirates", capacity=15, status=AttractionStatus.open),
        Attraction(name="It's a Small World", description="A fun ride with a small world", capacity=25, status=AttractionStatus.open),
        Attraction(name="Big Thunder Mountain", description="A fun ride with a big thunder", capacity=18, status=AttractionStatus.maintenance),
        Attraction(name="Phantom Manor", description="A beautiful manor with a lot of phantoms", capacity=12, status=AttractionStatus.closed),
        Attraction(name="Frozen Yogurt", description="A frozen treat with yogurt", capacity=10, status=AttractionStatus.closed),
    ]
    db.add_all(attractions)
    db.commit()

    # Retrieve real IDs
    attraction_ids = [attr.id for attr in attractions]

    # -----------------------------
    # seed tickets
    # -----------------------------

    tickets = []
    base_date = datetime(2025, 12, 6)

    # Generate tickets for a lot of days
    for day_offset in range(7):
        current_date = datetime(base_date.year, base_date.month, base_date.day + day_offset)

        # A lot of timeslots for each day
        for hour in [9, 11, 14, 16, 19]:
            ticket_date = current_date.replace(hour=hour, minute=0, second=0)

            # A lot of tickets for each timeslot
            for i in range(min(5, len(user_ids))):
                user_id = user_ids[i % len(user_ids)]
                attraction_id = attraction_ids[i % len(attraction_ids)]
                qr_code = f"QR{day_offset}{hour}{i:02d}{attraction_id}"

                tickets.append(Ticket(user_id=user_id, attraction_id=attraction_id, date=ticket_date, qr_code=qr_code))

    db.add_all(tickets)
    db.commit()

    # -----------------------------
    # seed reservations
    # -----------------------------

    restaurants = [
        "Agrabah Cafe Restaurant",
        "Alice and the Queen of Hearts : Return in Wonderland",
        "Annette's Diner",
        "Animation Academy",
        "At the Puppet Chalet",
        "Heroic Ceremony",
        "Cinderella Inn",
        "Disney Music Hits Concert",
        "Billy Bob's Buffet",
    ]

    reservations = []
    for day_offset in range(10): # 10 days of reservations
        current_date = datetime(base_date.year, base_date.month, base_date.day + day_offset)

        for hour in [12, 13, 19, 20]: # 4 timeslots for lunch and dinner
            reservation_date = current_date.replace(hour=hour, minute=0, second=0)

            for i, user_id in enumerate(user_ids): # 3 reservations for each timeslot
                resource_type = restaurants[i % len(restaurants)]
                nb_persons = 2 + i % 4
                status = [ReservationStatus.confirmed, ReservationStatus.pending, ReservationStatus.cancelled][i % 3]

                reservations.append(Reservation(user_id=user_id, resource_type=resource_type, date=reservation_date, nb_persons=nb_persons, status=status))

    db.add_all(reservations)
    db.commit()

    # -----------------------------
    # seed employees
    # -----------------------------

    employees = [
        Employee(name="Mickey Mouse", job="General Manager", assignment="Central Administration"),
        Employee(name="Minnie Mouse", job="Operations Manager", assignment="Park Management"),
        Employee(name="Goofy", job="Attractions Manager", assignment="Space Mountain"),
        Employee(name="Donald Duck", job="Attraction Operator", assignment="Pirates of the Caribbean"),
        Employee(name="Daisy Duck", job="Receptionist", assignment="Big Thunder Mountain"),
        Employee(name="Pluto", job="Maintenance Technician", assignment="Phantom Manor"),
        Employee(name="Chef Remy", job="Chef", assignment="Bistrot Chez Remy"),
        Employee(name="Light", job="Butler", assignment="Blue Lagoon Restaurant"),
        Employee(name="Mrs. Potts", job="Service Manager", assignment="Plaza Gardens Restaurant"),
        Employee(name="Simba", job="Main Performer", assignment="The Lion King and the Rhythms of the Earth"),
        Employee(name="Elsa", job="Main Performer", assignment="Frozen"),
        Employee(name="Woody", job="Security Guard", assignment="Central Zone Patrol"),
        Employee(name="Buzz Lightyear", job="Security Guard", assignment="Patrol Attractions Zone"),
        Employee(name="Wall-E", job="Maintenance Technician", assignment="General Maintenance"),
        Employee(name="Eve", job="Electronic Technician", assignment="Computer Systems"),
        Employee(name="Belle", job="Customer Advisor", assignment="Main Home"),
        Employee(name="Cendrillon", job="Tourist Guide", assignment="Guided Tours"),
        Employee(name="Ariel", job="Animator", assignment="Children's Activities"),
    ]
    db.add_all(employees)
    db.commit()
    
    db.close()
    print("Seeding complete successfully !")
    print(f"- {len(users)} users created")
    print(f"- {len(attractions)} attractions created")
    print(f"- {len(tickets)} tickets created")
    print(f"- {len(reservations)} reservations created")
    print(f"- {len(employees)} employees created")

if __name__ == "__main__":
    seed()