from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Attraction, AttractionStatus, Ticket, Employee, Reservation
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
        User(name="admin", email="admin@disney.com", password=get_password_hash("admin123"), role="admin"),
        User(name="employee", email="employee@disney.com", password=get_password_hash("employee123"), role="employee"),
        User(name="user", email="user@disney.com", password=get_password_hash("user123"), role="user"),
        User(name="Hadil", email="hadil@disney.com", password=get_password_hash("hadil123"), role="user"),
        User(name="John", email="john@disney.com", password=get_password_hash("john123"), role="user"),
        User(name="Sarah", email="sarah@disney.com", password=get_password_hash("sarah123"), role="user"),
        User(name="Tom", email="tom@disney.com", password=get_password_hash("tom123"), role="user"),
        User(name="Alice", email="alice@disney.com", password=get_password_hash("alice123"), role="user"),
        User(name="Bob", email="bob@disney.com", password=get_password_hash("bob123"), role="user"),
        User(name="Charlie", email="charlie@disney.com", password=get_password_hash("charlie123"), role="user"),
        User(name="David", email="david@disney.com", password=get_password_hash("david123"), role="user"), 
        User(name="Eve", email="eve@disney.com", password=get_password_hash("eve123"), role="user"),
        User(name="Frank", email="frank@disney.com", password=get_password_hash("frank123"), role="user"),
        User(name="Grace", email="grace@disney.com", password=get_password_hash("grace123"), role="user"),
        User(name="Henry", email="henry@disney.com", password=get_password_hash("henry123"), role="user"),
        User(name="Isabelle", email="isabelle@disney.com", password=get_password_hash("isabelle123"), role="user"),
        User(name="Jessica", email="jessica@disney.com", password=get_password_hash("jessica123"), role="user"),
        User(name="Karen", email="karen@disney.com", password=get_password_hash("karen123"), role="user"),
        User(name="Lisa", email="lisa@disney.com", password=get_password_hash("lisa123"), role="user"),
        User(name="Maggie", email="maggie@disney.com", password=get_password_hash("maggie123"), role="user"),
        User(name="Nancy", email="nancy@disney.com", password=get_password_hash("nancy123"), role="user"),
        User(name="Oscar", email="oscar@disney.com", password=get_password_hash("oscar123"), role="user"),
        User(name="Peter", email="peter@disney.com", password=get_password_hash("peter123"), role="user"),
        User(name="Quincy", email="quincy@disney.com", password=get_password_hash("quincy123"), role="user"),
        User(name="Rachel", email="rachel@disney.com", password=get_password_hash("rachel123"), role="user"),
        User(name="Steve", email="steve@disney.com", password=get_password_hash("steve123"), role="user"),
    ]
    db.add_all(users)
    db.commit()

    # Retrieve reel IDs
    admin_id = users[0].id
    employee_id = users[1].id
    user_id = users[2].id
    hadil_id = users[3].id
    john_id = users[4].id
    sarah_id = users[5].id
    tom_id = users[6].id
    alice_id = users[7].id
    bob_id = users[8].id
    charlie_id = users[9].id
    david_id = users[10].id
    eve_id = users[11].id
    frank_id = users[12].id
    grace_id = users[13].id
    henry_id = users[14].id
    isabelle_id = users[15].id
    jessica_id = users[16].id
    karen_id = users[17].id
    lisa_id = users[18].id
    maggie_id = users[19].id
    nancy_id = users[20].id
    oscar_id = users[21].id
    peter_id = users[22].id
    quincy_id = users[23].id
    rachel_id = users[24].id
    steve_id = users[25].id

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
    space_mountain_id = attractions[0].id
    pirates_of_the_caribbean_id = attractions[1].id
    its_a_small_world_id = attractions[2].id
    big_thunder_mountain_id = attractions[3].id
    phantom_manor_id = attractions[4].id
    frozen_yogurt_id = attractions[5].id

    # -----------------------------
    # seed tickets
    # -----------------------------

    tickets = [
        Ticket(user_id=user_id, attraction_id=space_mountain_id, date=datetime(2025, 10, 5, 10, 0), qr_code="QR123456"),
        Ticket(user_id=hadil_id, attraction_id=space_mountain_id, date=datetime(2025, 10, 5, 11, 0), qr_code="QR234567"),
        Ticket(user_id=john_id, attraction_id=space_mountain_id, date=datetime(2025, 10, 5, 12, 0), qr_code="QR345678"),
        Ticket(user_id=sarah_id, attraction_id=pirates_of_the_caribbean_id, date=datetime(2025, 10, 6, 13, 0), qr_code="QR456789"),
        Ticket(user_id=tom_id, attraction_id=pirates_of_the_caribbean_id, date=datetime(2025, 10, 6, 14, 0), qr_code="QR567890"),
        Ticket(user_id=alice_id, attraction_id=pirates_of_the_caribbean_id, date=datetime(2025, 10, 6, 15, 0), qr_code="QR678901"),
        Ticket(user_id=bob_id, attraction_id=its_a_small_world_id, date=datetime(2025, 10, 7, 16, 0), qr_code="QR789012"),
        Ticket(user_id=charlie_id, attraction_id=its_a_small_world_id, date=datetime(2025, 10, 7, 17, 0), qr_code="QR890123"),
        Ticket(user_id=david_id, attraction_id=its_a_small_world_id, date=datetime(2025, 10, 7, 18, 0), qr_code="QR901234"),
        Ticket(user_id=eve_id, attraction_id=big_thunder_mountain_id, date=datetime(2025, 10, 8, 19, 0), qr_code="QR012345"),
        Ticket(user_id=frank_id, attraction_id=big_thunder_mountain_id, date=datetime(2025, 10, 8, 20, 0), qr_code="QR123456"),
        Ticket(user_id=grace_id, attraction_id=big_thunder_mountain_id, date=datetime(2025, 10, 8, 21, 0), qr_code="QR234567"),
        Ticket(user_id=henry_id, attraction_id=phantom_manor_id, date=datetime(2025, 10, 9, 22, 0), qr_code="QR345678"),
        Ticket(user_id=isabelle_id, attraction_id=phantom_manor_id, date=datetime(2025, 10, 9, 23, 0), qr_code="QR456789"),
        Ticket(user_id=jessica_id, attraction_id=phantom_manor_id, date=datetime(2025, 10, 10, 0, 0), qr_code="QR567890"),
        Ticket(user_id=karen_id, attraction_id=frozen_yogurt_id, date=datetime(2025, 10, 11, 1, 0), qr_code="QR678901"),
        Ticket(user_id=lisa_id, attraction_id=frozen_yogurt_id, date=datetime(2025, 10, 11, 2, 0), qr_code="QR789012"),
        Ticket(user_id=maggie_id, attraction_id=frozen_yogurt_id, date=datetime(2025, 10, 11, 3, 0), qr_code="QR890123"),
    ]
    db.add_all(tickets)
    db.commit()

    # -----------------------------
    # seed reservations
    # -----------------------------

    reservations = [
        Reservation(user_id=user_id, resource_type="Agrabah Cafe Restaurant", date=datetime(2025, 10, 5, 10, 0), nb_persons=2, status="confirmed"),
        Reservation(user_id=hadil_id, resource_type="Alice and the Queen of Hearts : Return in Wonderland", date=datetime(2025, 10, 5, 11, 0), nb_persons=4, status="pending"),
        Reservation(user_id=john_id, resource_type="Annette's Diner", date=datetime(2025, 10, 5, 12, 0), nb_persons=2, status="cancelled"),
        Reservation(user_id=sarah_id, resource_type="Animation Academy", date=datetime(2025, 10, 6, 13, 0), nb_persons=2, status="confirmed"),
        Reservation(user_id=tom_id, resource_type="At the Puppet Chalet", date=datetime(2025, 10, 6, 14, 0), nb_persons=4, status="pending"),
        Reservation(user_id=alice_id, resource_type="Heroic Ceremony", date=datetime(2025, 10, 6, 15, 0), nb_persons=2, status="confirmed"),
        Reservation(user_id=bob_id, resource_type="Cinderella Inn", date=datetime(2025, 10, 7, 16, 0), nb_persons=4, status="pending"),
        Reservation(user_id=charlie_id, resource_type="Disney Music Hits Concert", date=datetime(2025, 10, 7, 17, 0), nb_persons=2, status="confirmed"),
        Reservation(user_id=david_id, resource_type="Billy Bob's Buffet", date=datetime(2025, 10, 7, 18, 0), nb_persons=4, status="pending"),
    ]
    db.add_all(reservations)
    db.commit()

    # -----------------------------
    # seed employees
    # -----------------------------

    employees = [
        Employee(name="Mickey Mouse", job="manager", assignment="Disneyland Resort"),
        Employee(name="Minnie Mouse", job="assistant", assignment="Disneyland Resort"),
        Employee(name="Donald Duck", job="sales", assignment="Disneyland Resort"),
        Employee(name="Daisy Duck", job="assistant", assignment="Disneyland Resort"),
        Employee(name="Pluto", job="marketing", assignment="Disneyland Resort"),
        Employee(name="Goofy", job="security", assignment="Disneyland Resort"),
    ]
    db.add_all(employees)
    db.commit()
    
    db.close()
    print("Seeding complete successfully !")

if __name__ == "__main__":
    seed()