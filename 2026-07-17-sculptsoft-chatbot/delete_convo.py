from database.crud import get_db, get_all_conversations
from database.db import Conversation


def list_conversations(db):
    convos = get_all_conversations(db)
    if not convos:
        print("No conversations found.")
        return []
    print("\n── Conversations ─────────────────────────────")
    for i, c in enumerate(convos, 1):
        print(f"  [{i}] (id={c.id}) {c.title}  —  {c.created_at.strftime('%Y-%m-%d %H:%M')}")
    print("──────────────────────────────────────────────\n")
    return convos


def delete_by_id(db, conversation_id: int):
    convo = db.query(Conversation).filter_by(id=conversation_id).first()
    if not convo:
        print(f"No conversation with id={conversation_id}.")
        return
    confirm = input(f"Delete '{convo.title}' (id={convo.id})? [y/N]: ").strip().lower()
    if confirm == "y":
        db.delete(convo)
        db.commit()
        print(f"Deleted '{convo.title}'.")
    else:
        print("Cancelled.")


def delete_all(db):
    convos = get_all_conversations(db)
    if not convos:
        print("Nothing to delete.")
        return
    confirm = input(f"Delete ALL {len(convos)} conversations? This cannot be undone. [y/N]: ").strip().lower()
    if confirm == "y":
        db.query(Conversation).delete()
        db.commit()
        print(f"Deleted {len(convos)} conversations.")
    else:
        print("Cancelled.")


def main():
    db = get_db()
    try:
        while True:
            convos = list_conversations(db)
            if not convos:
                break

            print("Options:")
            print("  Enter a number to delete that conversation")
            print("  'a'  — delete all")
            print("  'q'  — quit")
            choice = input("\n> ").strip().lower()

            if choice == "q":
                break
            elif choice == "a":
                delete_all(db)
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(convos):
                    delete_by_id(db, convos[idx].id)
                else:
                    print("Invalid number.")
            else:
                print("Invalid input.")
            print()
    finally:
        db.close()


if __name__ == "__main__":
    main()
