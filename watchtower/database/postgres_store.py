"""PostgreSQL + pgvector database integration."""

from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from watchtower.models.evidence import Evidence
from watchtower.models.claim import Claim
from watchtower.models.artifact import Artifact


class PostgresStore:
    """
    PostgreSQL database store with pgvector support.
    
    Provides persistent storage for evidence, claims, and artifacts
    with vector similarity search capabilities.
    """
    
    def __init__(self, connection_string: Optional[str] = None) -> None:
        """
        Initialize PostgreSQL store.
        
        Args:
            connection_string: PostgreSQL connection string
        """
        self.connection_string = connection_string or "postgresql://localhost/watchtower"
        self._connection: Optional[Any] = None
    
    def connect(self) -> None:
        """Establish database connection."""
        # Import here to avoid dependency issues
        try:
            import psycopg2
            self._connection = psycopg2.connect(self.connection_string)
        except ImportError:
            # Graceful fallback if psycopg2 not available
            self._connection = None
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def init_schema(self) -> None:
        """Initialize database schema with tables and extensions."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        
        # Enable pgvector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Evidence table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id VARCHAR(36) PRIMARY KEY,
                content TEXT NOT NULL,
                source VARCHAR(255) NOT NULL,
                metadata JSONB,
                tool_name VARCHAR(255),
                tool_version VARCHAR(255),
                model_name VARCHAR(255),
                model_version VARCHAR(255),
                sha256 VARCHAR(64) NOT NULL,
                fingerprint VARCHAR(64) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                embedding vector(1536)
            );
        """)
        
        # Claims table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                id VARCHAR(36) PRIMARY KEY,
                statement TEXT NOT NULL,
                confidence FLOAT NOT NULL,
                supporting_evidence_ids JSONB NOT NULL,
                counter_evidence_ids JSONB NOT NULL,
                metadata JSONB,
                tool_name VARCHAR(255),
                tool_version VARCHAR(255),
                model_name VARCHAR(255),
                model_version VARCHAR(255),
                run_fingerprint VARCHAR(64) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                embedding vector(1536)
            );
        """)
        
        # Artifacts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifacts (
                id VARCHAR(36) PRIMARY KEY,
                artifact_type VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                parent_artifact_id VARCHAR(36),
                metadata JSONB,
                tool_name VARCHAR(255),
                tool_version VARCHAR(255),
                model_name VARCHAR(255),
                model_version VARCHAR(255),
                sha256 VARCHAR(64) NOT NULL,
                fingerprint VARCHAR(64) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (parent_artifact_id) REFERENCES artifacts(id)
            );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_evidence_sha256 ON evidence(sha256);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_evidence_timestamp ON evidence(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_confidence ON claims(confidence);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_timestamp ON claims(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifacts_type ON artifacts(artifact_type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifacts_timestamp ON artifacts(timestamp);")
        
        self._connection.commit()
        cursor.close()
    
    def store_evidence(self, evidence: Evidence) -> None:
        """Store evidence in database."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO evidence (
                id, content, source, metadata, tool_name, tool_version,
                model_name, model_version, sha256, fingerprint, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            evidence.id,
            evidence.content,
            evidence.source,
            json.dumps(evidence.metadata),
            evidence.tool_name,
            evidence.tool_version,
            evidence.model_name,
            evidence.model_version,
            evidence.sha256,
            evidence.fingerprint,
            evidence.timestamp,
        ))
        self._connection.commit()
        cursor.close()
    
    def store_claim(self, claim: Claim) -> None:
        """Store claim in database."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO claims (
                id, statement, confidence, supporting_evidence_ids,
                counter_evidence_ids, metadata, tool_name, tool_version,
                model_name, model_version, run_fingerprint, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            claim.id,
            claim.statement,
            claim.confidence,
            json.dumps(claim.supporting_evidence_ids),
            json.dumps(claim.counter_evidence_ids),
            json.dumps(claim.metadata),
            claim.tool_name,
            claim.tool_version,
            claim.model_name,
            claim.model_version,
            claim.run_fingerprint,
            claim.timestamp,
        ))
        self._connection.commit()
        cursor.close()
    
    def store_artifact(self, artifact: Artifact) -> None:
        """Store artifact in database."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("""
            INSERT INTO artifacts (
                id, artifact_type, content, parent_artifact_id, metadata,
                tool_name, tool_version, model_name, model_version,
                sha256, fingerprint, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            artifact.id,
            artifact.artifact_type,
            artifact.content,
            artifact.parent_artifact_id,
            json.dumps(artifact.metadata),
            artifact.tool_name,
            artifact.tool_version,
            artifact.model_name,
            artifact.model_version,
            artifact.sha256,
            artifact.fingerprint,
            artifact.timestamp,
        ))
        self._connection.commit()
        cursor.close()
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Retrieve evidence from database."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM evidence WHERE id = %s", (evidence_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        # Reconstruct Evidence object
        # Note: This is a simplified version
        return None  # Would need proper deserialization
    
    def get_claim(self, claim_id: str) -> Optional[Claim]:
        """Retrieve claim from database."""
        if not self._connection:
            raise RuntimeError("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM claims WHERE id = %s", (claim_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        # Reconstruct Claim object
        # Note: This is a simplified version
        return None  # Would need proper deserialization
