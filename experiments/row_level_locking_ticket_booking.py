import threading
import time
from enum import Enum
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class TicketStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    seat_number: str
    event_name: str
    price: float
    status: TicketStatus = TicketStatus.AVAILABLE


def book_ticket_without_lock(engine, ticket_id: int, customer_name: str):
    """Simulates booking without lock - race condition possible"""
    with Session(engine) as session:
        try:
            ticket = session.get(Ticket, ticket_id)
            if ticket.status != TicketStatus.AVAILABLE:
                print(f"❌ {customer_name}: Ticket {ticket.seat_number} not available")
                return

            print(
                f"🔍 {customer_name}: Found ticket {ticket.seat_number}, processing payment..."
            )
            time.sleep(0.5)  # Simulate payment processing

            ticket.status = TicketStatus.SOLD
            session.add(ticket)
            session.commit()
            print(f"✅ {customer_name}: Booked ticket {ticket.seat_number}")
        except Exception as e:
            session.rollback()
            print(f"❌ {customer_name}: Booking failed - {e}")


def book_ticket_with_lock(
    engine, ticket_id: int, customer_name: str, nowait: bool = False
):
    """Simulates booking with lock - prevents double booking"""
    with Session(engine) as session:
        try:
            statement = (
                select(Ticket)
                .where(Ticket.id == ticket_id, Ticket.status == TicketStatus.AVAILABLE)
                .with_for_update(nowait=nowait)
            )

            ticket = session.exec(statement).first()
            if not ticket:
                print(f"❌ {customer_name}: Ticket not available or already locked")
                return

            print(
                f"🔒 {customer_name}: Locked ticket {ticket.seat_number}, processing payment..."
            )
            time.sleep(0.5)  # Simulate payment processing

            ticket.status = TicketStatus.SOLD
            session.add(ticket)
            session.commit()
            print(
                f"✅ {customer_name}: Successfully booked ticket {ticket.seat_number}"
            )
        except Exception as e:
            session.rollback()
            print(f"❌ {customer_name}: Booking failed - {e}")


def ticket_booking_demo():
    engine = create_engine("postgresql://develop:develop_secret@localhost:5432/develop")
    SQLModel.metadata.create_all(engine)

    # Create test ticket
    with Session(engine) as session:
        ticket = Ticket(seat_number="A15", event_name="Concert", price=99.99)
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        ticket_id = ticket.id

    print("=" * 60)
    print("Scenario 1: WITHOUT LOCK (Double Booking Risk)")
    print("=" * 60)

    threads = [
        threading.Thread(
            target=book_ticket_without_lock, args=(engine, ticket_id, "Alice")
        ),
        threading.Thread(
            target=book_ticket_without_lock, args=(engine, ticket_id, "Bob")
        ),
        threading.Thread(
            target=book_ticket_without_lock, args=(engine, ticket_id, "Charlie")
        ),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n" + "=" * 60)
    print("Scenario 2: WITH LOCK (Safe Booking)")
    print("=" * 60)

    # Reset ticket
    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)
        ticket.status = TicketStatus.AVAILABLE
        session.commit()

    threads = [
        threading.Thread(
            target=book_ticket_with_lock, args=(engine, ticket_id, "Alice")
        ),
        threading.Thread(target=book_ticket_with_lock, args=(engine, ticket_id, "Bob")),
        threading.Thread(
            target=book_ticket_with_lock, args=(engine, ticket_id, "Charlie")
        ),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n" + "=" * 60)
    print("Scenario 3: WITH NOWAIT (Fail Fast)")
    print("=" * 60)

    # Reset ticket
    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)
        ticket.status = TicketStatus.AVAILABLE
        session.commit()

    threads = [
        threading.Thread(
            target=book_ticket_with_lock, args=(engine, ticket_id, "Alice", True)
        ),
        threading.Thread(
            target=book_ticket_with_lock, args=(engine, ticket_id, "Bob", True)
        ),
        threading.Thread(
            target=book_ticket_with_lock, args=(engine, ticket_id, "Charlie", True)
        ),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    ticket_booking_demo()
