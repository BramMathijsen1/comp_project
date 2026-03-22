import json
import sqlite3

from src.base.handler import UploadHandler
from src.models.bibliographic_entity import BibliographicEntity


class BibliographicEntityUploadHandler(UploadHandler):
    def pushDataToDb(self, path: str) -> bool:
        db_path = self.getDbPathOrUrl()
        if not db_path:
            return False

        try:
            with open(path, "r", encoding="utf-8") as source:
                records = json.load(source)

            with sqlite3.connect(db_path) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                self._create_schema(connection)

                for record in records:
                    entity = self._build_entity(record)
                    self._insert_entity(connection, entity)

                connection.commit()

            return True
        except (OSError, json.JSONDecodeError, sqlite3.DatabaseError, ValueError):
            return False

    def _create_schema(self, connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS bibliographic_entities (
                omid TEXT PRIMARY KEY,
                title TEXT,
                pub_date TEXT,
                venue TEXT
            );

            CREATE TABLE IF NOT EXISTS entity_authors (
                omid TEXT NOT NULL,
                author_name TEXT NOT NULL,
                author_order INTEGER NOT NULL,
                PRIMARY KEY (omid, author_name),
                FOREIGN KEY (omid) REFERENCES bibliographic_entities(omid) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS entity_identifiers (
                identifier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                omid TEXT NOT NULL,
                identifier_type TEXT,
                identifier_value TEXT NOT NULL,
                UNIQUE (omid, identifier_value),
                FOREIGN KEY (omid) REFERENCES bibliographic_entities(omid) ON DELETE CASCADE
            );
            """
        )

    def _build_entity(self, record: dict) -> BibliographicEntity:
        entity = BibliographicEntity()
        entity.title = (record.get("title") or "").strip()
        entity.author = [
            author_name.strip()
            for author_name in record.get("author", [])
            if author_name and author_name.strip()
        ]
        entity.publication_date = (record.get("pub_date") or "").strip()
        entity.venue = record.get("venue")
        entity.id = [value.strip() for value in record.get("id", []) if value and value.strip()]
        return entity

    def _insert_entity(self, connection: sqlite3.Connection, entity: BibliographicEntity) -> None:
        identifiers = entity.getIds()
        omid = self._extract_omid(identifiers)
        if not omid:
            raise ValueError("Each bibliographic record must include an OMID identifier.")

        connection.execute(
            """
            INSERT INTO bibliographic_entities (omid, title, pub_date, venue)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(omid) DO UPDATE SET
                title = excluded.title,
                pub_date = excluded.pub_date,
                venue = excluded.venue
            """,
            (
                omid,
                entity.getTitle(),
                entity.getPublicationDate(),
                entity.getVenue(),
            ),
        )

        for order_index, author_name in enumerate(entity.getAuthors(), start=1):
            connection.execute(
                """
                INSERT INTO entity_authors (omid, author_name, author_order)
                VALUES (?, ?, ?)
                ON CONFLICT(omid, author_name) DO UPDATE SET
                    author_order = excluded.author_order
                """,
                (omid, author_name, order_index),
            )

        for identifier in identifiers:
            id_type = identifier.split(":", 1)[0] if ":" in identifier else None
            connection.execute(
                """
                INSERT OR IGNORE INTO entity_identifiers (omid, identifier_type, identifier_value)
                VALUES (?, ?, ?)
                """,
                (omid, id_type, identifier),
            )

    def _extract_omid(self, identifiers: list[str]) -> str | None:
        for identifier in identifiers:
            if identifier.startswith("omid:br/"):
                return identifier
        return None
